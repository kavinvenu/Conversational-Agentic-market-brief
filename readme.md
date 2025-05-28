# 🧠 Multi-Agent Market Briefing System

A multi-agent architecture for real-time financial intelligence using LLMs, speech interfaces, and live data pipelines.

[Working demo](https://github.com/user-attachments/assets/861800d5-12b4-4b56-bc91-5b445df242bc) 

---

## 🚀 Getting Started

### 1. Set Up Environment
Make sure you have your `.env` file configured with all necessary API keys and settings.

### 2. Run Orchestrator (FastAPI)

uvicorn orchestrator.main:app --reload --host 0.0.0.0 --port 8000
3. Run Frontend (Streamlit)
bash
Copy
Edit
streamlit run streamlit_app/app.py
🧪 Example Use Case
👤 User Input:
"What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"

🤖 AI Response:
vbnet
Copy
Edit
Your investment in Asia tech increased from 18% to 22%. 
TSMC exceeded expectations by 4%, Samsung missed by 2%. 
Regional sentiment is neutral but cautious due to rising yields.
🧰 Tech Stack
FastAPI – Microservice orchestrator for managing agent communication

Streamlit – Interactive frontend for voice and display interface

FAISS – Vector similarity search for retrieval-based querying

SentenceTransformers – Embedding generation for financial text

yfinance – Live financial data collection

BeautifulSoup – Web scraping for earnings reports and financial news

Gemini 3.5 Flash – LLM for synthesis and decision making

🔍 Why Gemini 3.5 Flash?

Lightning-fast responses

Robust dynamic prompt handling

Great synthesis of structured + unstructured data

Designed for Retrieval-Augmented Generation (RAG)

User (Mic Input)
     ↓
📌 1. Voice Agent (STT - Whisper)
     ↓
📌 2. Orchestrator (FastAPI)
     ├──→ 📡 API Agent → Yahoo Finance / Portfolio CSV
     ├──→ 🕷️ Scraping Agent → Yahoo/Earnings Reports
     ├──→ 🧠 Retriever Agent → FAISS + Embedded Docs
     ├──→ 📊 Analysis Agent → AUM calculations
     ↓
📌 3. Language Agent (LLM + LangChain)
     ↓
📌 4. Voice Agent (TTS - pyttsx3/Coqui)
     ↓
Streamlit UI: Text + Audio Output


🚧 Future Improvements
✅ Replace simulated LLM with real Gemini API

✅ Integrate realistic TTS using ElevenLabs or Coqui

✅ Add Pinecone support for persistent vector DB

✅ Enable portfolio import/upload via Excel

🔜 Add automatic .env loader

🔜 Export vector store to disk for persistence

🔜 Add microphone-based voice recording in frontend

🔜 Provide Dockerfile + full deployment guide

📬 Questions?
Feel free to DM, raise an issue, or contribute to the repo!

👨‍💻 Author
Kavin Kumar
Built as part of a real-world challenge to automate financial intelligence using agents.
