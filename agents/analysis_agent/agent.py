# analysis_agent.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Optional

app = FastAPI(title="Analysis Agent")

class PortfolioData(BaseModel):
    allocations: Dict[str, float]  # e.g. {"TSM": 10.5, "Samsung": 8.2}
    earnings_surprises: Optional[Dict[str, float]] = None

@app.post("/risk_exposure")
async def risk_exposure(data: PortfolioData):
    """
    Simple risk analysis based on portfolio allocations and earnings surprises.
    """
    total_allocation = sum(data.allocations.values())
    high_surprise_stocks = []
    low_surprise_stocks = []
    
    if data.earnings_surprises:
        for ticker, surprise in data.earnings_surprises.items():
            if surprise is not None:
                if surprise > 0:
                    high_surprise_stocks.append(ticker)
                elif surprise < 0:
                    low_surprise_stocks.append(ticker)

    summary = f"Your total portfolio allocation in selected stocks is {total_allocation:.2f}% of AUM."
    if high_surprise_stocks:
        summary += f" Stocks with positive earnings surprises: {', '.join(high_surprise_stocks)}."
    if low_surprise_stocks:
        summary += f" Stocks with negative earnings surprises: {', '.join(low_surprise_stocks)}."
    
    # Placeholder for risk comment
    risk_comment = "Overall risk is moderate with some positive earnings momentum."
    
    return {"summary": summary, "risk_comment": risk_comment}
