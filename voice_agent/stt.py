import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe audio bytes using OpenAI Whisper.
    """
    # You can write to temp file or use openai.Audio API directly with bytes buffer
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
        f.write(audio_bytes)
        f.flush()
        transcript = openai.Audio.transcribe("whisper-1", f.name)
        return transcript['text']
