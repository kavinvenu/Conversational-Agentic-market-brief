import requests
from bs4 import BeautifulSoup

def scrape_earnings(symbols):
    results = {}
    for symbol in symbols:
        url = f"https://finance.yahoo.com/quote/{symbol}/analysis"
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, "html.parser")

        # Fallback: Dummy logic – customize with exact parsing if needed
        summary = soup.find("section")
        if summary:
            if "beat" in summary.text.lower():
                results[symbol] = "+4%"
            elif "miss" in summary.text.lower():
                results[symbol] = "-2%"
            else:
                results[symbol] = "0%"
        else:
            results[symbol] = "N/A"

    return results
