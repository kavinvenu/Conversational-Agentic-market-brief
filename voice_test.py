import requests

# 1. Upload recorded audio (ensure it's a .wav file)
audio_path = "question.wav"

# 2. STT → Get query text
with open(audio_path, "rb") as f:
    stt_resp = requests.post("http://localhost:8000/stt", files={"audio": f})
text = stt_resp.json()["text"]
print("🗣️ Recognized:", text)

# 3. QUERY → Ask question to agents or LLM
resp = requests.post("http://localhost:8000/query", json={"query": text})
response_text = resp.json()["response"]
print("🤖 Response:", response_text)

# 4. TTS → Convert back to audio
tts_resp = requests.post("http://localhost:8000/tts", json={"text": response_text})
print("🔊 Audio file saved as:", tts_resp.json()["audio_path"])
