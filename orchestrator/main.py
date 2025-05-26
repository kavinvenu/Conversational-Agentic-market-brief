from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import JSONResponse
import uvicorn

from voice_agent.stt import transcribe_audio
from voice_agent.tts import synthesize_speech
from agents.api_agent.agent import analyze_portfolio
from agents.scraping_agent.agent import scrape_earnings
from agents.retriever_agent.agent import get_relevant_chunks
from utils.llm import query_ollama  # <-- For fallback LLM generation

app = FastAPI()

@app.post("/stt")
async def stt_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    text = transcribe_audio(audio_bytes)
    return {"text": text}


@app.post("/query")
async def query_endpoint(payload: dict = Body(...)):
    text = payload.get("text", "")

    # Intent-based routing
    if "portfolio" in text.lower() or "exposure" in text.lower():
        result = analyze_portfolio("data/portfolio.csv")
        return JSONResponse(content={"result": f"Asia Tech exposure is {result['asia_tech_pct']}% of AUM."})

    elif "earnings" in text.lower() or "beat" in text.lower():
        result = scrape_earnings(["TSM", "SSNLF"])
        response = " ".join([f"{symbol} {change}" for symbol, change in result.items()])
        return JSONResponse(content={"result": response})

    elif "report" in text.lower() or "sentiment" in text.lower():
        chunks = get_relevant_chunks(text)
        return JSONResponse(content={"result": "\n".join(chunks)})

    else:
        # Fallback to LLM
        llm_response = query_ollama(text)
        return JSONResponse(content={"result": llm_response})


@app.post("/tts")
async def tts_endpoint(payload: dict = Body(...)):
    content = payload.get("text", "")
    audio = synthesize_speech(content)
    return JSONResponse(content={"audio": audio.hex()})  # audio as hex string


if __name__ == "__main__":
    uvicorn.run("orchestrator.main:app", host="0.0.0.0", port=8000, reload=True)
