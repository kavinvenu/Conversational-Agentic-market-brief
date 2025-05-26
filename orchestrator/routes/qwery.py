from fastapi import APIRouter, Body
from utils.llm import query_ollama
from agents.scraping_agent.agent import scrape_earnings
from agents.analysis_agent.analyze import analyze_portfolio
from agents.retriever_agent.agent import get_relevant_chunks

router = APIRouter()

@router.post("/query")
def query_agent(query: str = Body(...)):
    if "earning" in query.lower():
        data = scrape_earnings(["TSM", "SSNLF"])
        earnings_summary = " ".join([f"{k} {v}" for k, v in data.items()])
        return {"response": earnings_summary}

    elif "exposure" in query.lower() or "asia tech" in query.lower():
        summary = analyze_portfolio("data/portfolio_today.csv")
        return {
            "response": f"Asia Tech exposure is {summary['asia_tech_pct']}% of total AUM"
        }

    elif "report" in query.lower() or "sentiment" in query.lower():
        chunks = get_relevant_chunks(query)
        return {"response": "\n".join(chunks)}

    else:
        final = query_ollama(query)
        return {"response": final}
