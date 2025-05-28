import os
from typing import List

# Dummy import example, replace with your Gemini 2.0 Flash SDK or REST client
# from google.generativeai import Client

# For demonstration, let's assume Gemini 2.0 Flash is accessible via an API endpoint,
# and you use HTTP requests with an API key.

import requests

GEMINI_API_URL = "https://gemini.googleapis.com/v1/models/gemini-2.0-flash/generateText"
API_KEY = os.getenv("AIzaSyA7ZmjqgqyNjb1JmjlcLgFM1XPO2Rx32gs")  # Set your Gemini API key in environment variable

def generate_text(prompt: str, max_tokens: int = 256) -> str:
    """
    Generate text using Gemini 2.0 Flash LLM.

    Args:
        prompt (str): The input prompt text.
        max_tokens (int): Maximum tokens to generate.

    Returns:
        str: Generated text from the model.
    """
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": {
            "text": prompt
        },
        "maxTokens": max_tokens,
        "temperature": 0.7,
        "topP": 0.95,
        "candidateCount": 1,
        "stopSequences": ["\n"]
    }

    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error from Gemini API: {response.status_code} {response.text}")

    resp_json = response.json()

    # Extract the generated text from response - depends on API format
    try:
        generated_text = resp_json["candidates"][0]["output"]
        return generated_text.strip()
    except (KeyError, IndexError):
        raise Exception(f"Unexpected response format: {resp_json}")

# Optional: function to generate a summary from structured data input
def generate_summary(data: dict) -> str:
    """
    Convert aggregated data dict to a formatted prompt and call Gemini to generate narrative.

    Args:
        data (dict): Aggregated info from agents.

    Returns:
        str: Narrative summary.
    """
    # Build prompt text (you can customize)
    prompt = "You are a financial assistant.\nSummarize the following market data briefly:\n\n"

    if "api_agent" in data:
        api = data["api_agent"]
        prompt += f"Portfolio allocation: {api.get('asia_tech_allocation', 'N/A')}, change: {api.get('change_from_yesterday', 'N/A')}\n"

    if "scraping_agent" in data:
        scraping = data["scraping_agent"].get("earnings_surprises", [])
        for surprise in scraping:
            for company, change in surprise.items():
                prompt += f"Earnings surprise: {company} {change}\n"

    if "retriever_agent" in data:
        docs = data["retriever_agent"].get("relevant_docs", [])
        prompt += "Relevant documents:\n"
        for doc in docs:
            prompt += f"- {doc}\n"

    if "analysis_agent" in data:
        risk = data["analysis_agent"].get("risk_comment", "")
        prompt += f"Risk commentary: {risk}\n"

    prompt += "\nSummarize the above in a concise and professional tone."

    return generate_text(prompt)
