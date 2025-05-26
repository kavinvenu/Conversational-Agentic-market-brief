from faster_whisper import WhisperModel
import io

model = WhisperModel("base")

def transcribe_audio(audio_bytes: bytes) -> str:
    audio_file = io.BytesIO(audio_bytes)
    segments, info = model.transcribe(audio_file)
    text = " ".join([segment.text for segment in segments])
    return text
