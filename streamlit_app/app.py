import streamlit as st
import httpx
import asyncio

ORCHESTRATOR_URL = "http://localhost:8000"   

# Async wrappers for agents
async def get_market_data(region, sector):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ORCHESTRATOR_URL}/api_agent/market-data", params={"region": region, "sector": sector})
        return resp.json()

async def get_earnings_surprises(region, sector):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ORCHESTRATOR_URL}/scraping_agent/earnings-surprises", params={"region": region, "sector": sector})
        return resp.json()

async def retrieve_docs(query):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ORCHESTRATOR_URL}/retriever_agent/retrieve-docs", params={"query": query})
        return resp.json()

async def analyze_risk():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ORCHESTRATOR_URL}/analysis_agent/analyze-risk")
        return resp.json()

async def call_gemini_llm(prompt):
    # Replace with real Gemini LLM API call
    # Here we simulate response
    return f"Gemini 3.5 Flash LLM generated response:\n\n{prompt[:200]}..."

# Full workflow
async def generate_market_brief(query):
    region = "Asia"
    sector = "Technology"

    market_data = await get_market_data(region, sector)
    earnings = await get_earnings_surprises(region, sector)
    retrieved = await retrieve_docs(query)
    analysis = await analyze_risk()

    # Compose prompt for LLM
    prompt = f"""
    Query: {query}

    Market Data: {market_data['market_data']}
    Earnings Surprises: {earnings['earnings_surprises']}
    Retrieved Docs: {retrieved['top_docs']}
    Risk Analysis: {analysis['risk_comment']}
    """

    response = await call_gemini_llm(prompt)
    return response

st.title("Multi-Agent Finance Assistant")

user_query = st.text_input("Ask your finance question:", 
                           value="What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?")

if st.button("Get Market Brief"):
    with st.spinner("Generating market brief..."):
        result = asyncio.run(generate_market_brief(user_query))
        st.markdown(f"### Assistant Response:\n{result}")
