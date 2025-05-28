# 📘 AI Tool Usage Log — Conversational Market Brief Assistant

This document tracks all AI tool interactions, prompts used, and parameter configurations during the development of the voice-enabled multi-agent financial assistant.

---

## 🧠 LLM: Gemini 1.5 Flash / Gemini 3.5 Flash (Google)

### 🔧 Use Cases:

* Intent extraction from natural queries.
* Synthesis of final financial brief.
* Prompt planning and routing decisions for agents.

### ✅ Example Prompt:

```txt
You are a financial summarization assistant. Based on the structured data below, generate a concise and professional market brief.

Input:
- Asia Tech Allocation: 22% of AUM
- Change from Yesterday: Up 4%
- TSMC Earnings: Beat estimates by 4%
- Samsung Earnings: Missed by 2%
- Regional Sentiment: Neutral with cautionary tilt due to rising yields

Output:
Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday...
```

### ⚙️ Parameters:

* Model: `gemini-1.5-flash` or `gemini-3.5-flash`
* Temperature: `0.4`
* Max tokens: `1024`

---

## 🎙️ Whisper (STT)

### 🔧 Use Cases:

* Transcribing user’s spoken queries.

### Configuration:

* Model: `openai/whisper` or `faster-whisper` (optional for speed)
* Language: English

### Example Output:

Input audio (5s): “What’s our risk exposure in Asia tech today?”
Transcription: `"What’s our risk exposure in Asia tech today?"`

---

## 🗣️ Coqui / Piper (TTS)

### 🔧 Use Cases:

* Speaking the final LLM-generated response.

### Configuration:

* Voice: Default (or select `en_us_male.glow_tts` if available)
* Format: WAV or MP3
* Sampling rate: 22050 Hz

---

## 📡 FAISS (Vector DB for RAG)

### 🔧 Use Cases:

* Retrieval of semantically similar documents or earnings commentary.

### Configuration:

* Embedding Model: `all-MiniLM-L6-v2` via `sentence-transformers`
* Index: FlatL2 (for simplicity)
* Dimensions: 384

### Retrieval Prompt:

```txt
Relevant documents retrieved from RAG system:
- "Regional sentiment remains cautious due to high yields."
- "TSMC earnings beat, Samsung underperforms."

Include these insights in the final response.
```

---

## 🔍 BeautifulSoup + Requests (Scraping Agent)

### 🔧 Use Cases:

* Extracting real-time earnings data or headlines from Yahoo Finance, MarketWatch, etc.

### Sample Endpoint:

```python
from bs4 import BeautifulSoup
import requests
url = "https://finance.yahoo.com/quote/TSM/"
soup = BeautifulSoup(requests.get(url).content, "html.parser")
earnings = soup.find("td", text="EPS actual").find_next_sibling("td").text
```

---

## 📈 yfinance (API Agent)

### 🔧 Use Cases:

* Pulling portfolio allocation, prices, AUM data.

### Sample Code:

```python
import yfinance as yf
stock = yf.Ticker("TSM")
data = stock.history(period="2d")
price_change = data["Close"].iloc[-1] - data["Close"].iloc[-2]
```

---

## 🔗 LangChain or CrewAI (RAG Agent Wrapping)

### 🔧 Use Cases:

* Chain retrieval with summarization.
* Interface between query → retriever → LLM response.

### Example Flow:

```python
retriever = FAISS.load_local("index")
docs = retriever.similarity_search(query)
prompt = PromptTemplate(input_variables=["docs"], template="Summarize this:
{docs}")
```

---

## 📋 Summary

| Tool                 | Role           | Configured Parameters      |
| -------------------- | -------------- | -------------------------- |
| Gemini 1.5/3.5 Flash | LLM            | temp=0.4, max\_tokens=1024 |
| Whisper              | STT            | language=en                |
| Coqui / Piper        | TTS            | voice=default, format=wav  |
| FAISS + MiniLM       | RAG            | dims=384, index=FlatL2     |
| yfinance             | API Agent      | real-time historical data  |
| BeautifulSoup        | Scraping Agent | earnings, news, filings    |

This document helps in auditing all AI usage, tools, and parameters per evaluation guidelines.
