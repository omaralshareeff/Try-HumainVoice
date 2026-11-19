from __future__ import annotations

import asyncio
import os
import sys
import wave
from pathlib import Path

from humain_voice import stt, tts


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def write_pcm16_wav(path: Path, pcm: bytes, sample_rate: int) -> None:
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm)


def handle_error(error: stt.ErrorResponse | None) -> None:
    if error is not None:
        print("error:", error.code, error.message, file=sys.stderr)


async def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello from HUMAIN Voice"
    output_path = Path(sys.argv[2] if len(sys.argv) > 2 else "speech.wav")
    async with tts.TTSClient(
        api_url=required_env("API_URL"),
        api_key=required_env("API_KEY"),
        api_path=os.environ.get("API_PATH"),
    ) as client:
        voices = await client.list_voices(timeout_seconds=5.0)
        if not voices:
            raise RuntimeError("No TTS voices are available")
        voice = next((item for item in voices if item.get("profile")), voices[0])
        if profile := voice.get("profile"):
            print(
                "status:",
                "voice",
                voice["label"],
                profile["speaker"]["dialect"],
                profile["languages"],
            )

        model = tts.TtsModel.Nebula
        pcm = await client.synthesize(
            text,
            voice_id=voice["id"],
            model=model,
            # Inactivity timeout per audio chunk, not a total deadline.
            timeout_seconds=30.0,
            on_error=handle_error,
        )

    write_pcm16_wav(output_path, pcm, tts.get_sample_rate(model))


if __name__ == "__main__":
    asyncio.run(main())
