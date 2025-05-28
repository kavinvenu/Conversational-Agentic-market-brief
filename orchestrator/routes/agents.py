from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional

from agents.api_agent import get_market_data
from agents.scraping_agent import get_earnings_surprises
from agents.retriever_agent import RetrieverAgent
from agents.analysis_agent import analyze_risk_exposure
from utils.llm import generate_summary
from voice_agent.stt import transcribe_audio
from voice_agent.tts import synthesize_speech

router = APIRouter()

retriever = RetrieverAgent()
# For demo, dummy docs
dummy_docs = [
    "Regional sentiment is neutral with a cautionary tilt due to rising yields.",
    "Tech stocks in Asia are showing moderate growth amid geopolitical tensions.",
    "Earnings season is volatile, with mixed surprises across companies."
]
retriever.build_index(dummy_docs)

class Query(BaseModel):
    region: str
    sector: str
    date: Optional[str] = None
    voice: Optional[bool] = False

@router.post("/query")
async def process_query(q: Query):
    api_data = get_market_data(q.region, q.sector)
    scraping_data = get_earnings_surprises(q.region, q.sector)
    query_text = f"{q.region} {q.sector} earnings surprises"
    retriever_data = retriever.retrieve(query_text)
    analysis_data = analyze_risk_exposure(api_data)

    aggregated = {
        "api_agent": api_data,
        "scraping_agent": {"earnings_surprises": scraping_data},
        "retriever_agent": {"relevant_docs": retriever_data},
        "analysis_agent": analysis_data
    }

    prompt = "You are a financial assistant.\nSummarize the following market data briefly:\n\n"
    if api_data:
        prompt += f"Portfolio allocation: {api_data.get('asia_tech_allocation', 'N/A')}, change: {api_data.get('change_from_yesterday', 'N/A')}\n"
    if scraping_data:
        for surprise in scraping_data:
            for company, change in surprise.items():
                prompt += f"Earnings surprise: {company} {change}\n"
    if retriever_data:
        prompt += "Relevant documents:\n"
        for doc in retriever_data:
            prompt += f"- {doc}\n"
    if analysis_data:
        prompt += f"Risk commentary: {analysis_data.get('risk_comment', '')}\n"
    prompt += "\nSummarize the above in a concise and professional tone."

    summary = generate_summary(prompt)
    return {"summary": summary, "detail": aggregated}

@router.post("/stt")
async def stt_endpoint(audio: UploadFile = File(...)):
    """
    Receive an audio file and return transcription text.
    """
    audio_bytes = await audio.read()
    text = transcribe_audio(audio_bytes)
    return {"transcription": text}

@router.post("/tts")
async def tts_endpoint(text: str = Form(...)):
    """
    Receive text and return synthesized speech audio bytes.
    """
    audio_bytes = synthesize_speech(text)
    return {"audio_bytes": audio_bytes}
