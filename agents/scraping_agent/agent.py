# scraping_agent.py
from fastapi import FastAPI, Query
from yahoo_earnings_calendar import YahooEarningsCalendar
from typing import List

app = FastAPI(title="Scraping Agent - Earnings Surprises")

@app.get("/earnings_surprises")
async def earnings_surprises(tickers: List[str] = Query(...)):
    """
    Returns earnings surprise percentages for the given tickers if available.
    """
    yec = YahooEarningsCalendar()
    surprises = {}
    for ticker in tickers:
        try:
            earnings = yec.get_earnings_of(ticker)
            # Pick most recent earnings release
            if earnings:
                latest = earnings[0]
                surprise = latest.get('epsactual', None) - latest.get('epsestimate', None)
                surprise_pct = None
                if surprise is not None and latest.get('epsestimate') != 0:
                    surprise_pct = (surprise / latest.get('epsestimate')) * 100
                surprises[ticker] = round(surprise_pct, 2) if surprise_pct else None
            else:
                surprises[ticker] = None
        except Exception as e:
            surprises[ticker] = None
    return {"earnings_surprises": surprises}
