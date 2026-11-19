# HUMAIN Voice

Set the API settings in the terminal, then run either command from this folder. Use `.venv/bin/python`.

```bash
export API_URL="https://api.voice.humain.com"
export API_KEY="YOUR_API_KEY"
```

## Transcribe a recording

```bash
.venv/bin/python batch_transcription.py recording.wav
```

Prints the transcript and writes `recording.vtt`.

## Text to speech

```bash
.venv/bin/python tts_to_wav.py "Hello my name is Omar Alshareef" speech.wav
afplay speech.wav
```

The first command writes `speech.wav`. The second plays it.
