from fastapi import APIRouter, File, UploadFile
import whisper

router = APIRouter()
model = whisper.load_model("base",device = "cuda" if torch.cuda.is_available() else "cpu")

@router.post("/stt")
async def stt(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    result = model.transcribe("temp.wav")
    return {"text": result["text"]}
