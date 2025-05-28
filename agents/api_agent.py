import yfinance as yf

def get_market_data(region: str, sector: str):
    """
    Simple Yahoo Finance fetch: get % change for a list of tickers in Asia tech.
    """
    # For demo, hardcoded tickers for Asia tech sector
    tickers = {
        "TSMC": "2330.TW",
        "Samsung": "005930.KS",
        "Sony": "SONY",
    }

    data = {}
    for name, ticker in tickers.items():
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")
        if hist.empty or len(hist) < 2:
            continue
        prev_close = hist['Close'][-2]
        last_close = hist['Close'][-1]
        pct_change = ((last_close - prev_close) / prev_close) * 100
        data[name] = round(pct_change, 2)

    # Dummy portfolio allocation data:
    portfolio_allocation = {
        "asia_tech_allocation": "22%",
        "change_from_yesterday": "up 4%"
    }

    return {"price_changes": data, **portfolio_allocation}
