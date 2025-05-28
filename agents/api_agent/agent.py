# api_agent.py
from fastapi import FastAPI, Query
import yfinance as yf
from typing import List

app = FastAPI(title="API Agent - Market Data")

@app.get("/market_data")
async def market_data(
    tickers: List[str] = Query(..., description="List of stock tickers"),
    start_date: str = Query(None, description="Start date YYYY-MM-DD"),
    end_date: str = Query(None, description="End date YYYY-MM-DD")
):
    """
    Fetches historical stock data for tickers.
    Example: /market_data?tickers=TSM,005930.KS&start_date=2023-05-01&end_date=2023-05-27
    """
    response = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        if hist.empty:
            response[ticker] = "No data found"
        else:
            close_price = hist['Close'].iloc[-1]
            change = None
            if len(hist) > 1:
                change = ((close_price - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100
            response[ticker] = {
                "close_price": close_price,
                "percent_change": round(change, 2) if change is not None else None
            }
    return {"data": response}
