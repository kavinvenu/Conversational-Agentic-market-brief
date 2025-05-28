from TTS.api import TTS
import io

# Initialize TTS model (you can use Coqui TTS or other)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def synthesize_speech(text: str) -> bytes:
    """
    Generate speech audio bytes from text using Coqui TTS.
    """
    wav = tts.tts(text)
    # Convert numpy array wav to bytes (WAV format)
    import soundfile as sf

    buf = io.BytesIO()
    sf.write(buf, wav, samplerate=tts.synthesizer.output_sample_rate, format="WAV")
    return buf.getvalue()
