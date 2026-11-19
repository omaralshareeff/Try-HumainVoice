from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from humain_voice import stt
from humain_voice.stt.batchtranscription import BatchDiarization


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


async def main() -> None:
    input_path = Path(sys.argv[1] if len(sys.argv) > 1 else "recording.wav")
    output_path = Path(sys.argv[2] if len(sys.argv) > 2 else "recording.vtt")
    if not input_path.is_file():
        raise SystemExit(f"Audio file not found: {input_path.resolve()}")

    async with stt.BatchTranscribeClient(
        api_url=required_env("API_URL"),
        api_key=required_env("API_KEY"),
        api_version=os.environ.get("API_VERSION", "v1"),
    ) as client:
        result = await client.transcribe(
            input_path,
            lang=stt.Language.ArEn,
            asr=stt.BatchTranscriptionModel.BayanArEn,
            diarization=BatchDiarization.On,
            save_result=True,
            poll_interval=2.0,
            timeout_seconds=300.0,
            on_progress=lambda response: print("status:", response.status.value),
        )

    print(result.results.transcript if result.results else "")
    output_path.write_text(
        stt.Subtitles.from_response(result).to_vtt(),
        encoding="utf-8",
    )


if __name__ == "__main__":
    asyncio.run(main())
