from fastapi import APIRouter, Body
from gtts import gTTS

router = APIRouter()

@router.post("/tts")
def tts(text: str = Body(...)):
    tts = gTTS(text)
    tts.save("response.mp3")
    return {"audio_path": "response.mp3"}
