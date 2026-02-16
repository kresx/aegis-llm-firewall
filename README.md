# Aegis-LAF (LLM Access Firewall)
An industry-grade security middleware for LLM applications.

###  Features
* **Hybrid Defense:** Combined Regex-based pattern matching and Semantic Intent detection.
* **Semantic Guard:** Powered by Sentence-Transformers and FAISS.
* **Audit Logging:** High-concurrency SQLite (WAL mode) logging.
* **Analytics Dashboard:** Real-time SOC monitoring with Streamlit.

###  Installation
1. `pip install -r requirements.txt`
2. Create `.env` with `OPENAI_API_KEY`
3. `uvicorn app.main:app --reload`