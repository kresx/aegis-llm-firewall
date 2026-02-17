from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import time

# Core Security Imports
from app.core.input_engine import inspect_input
from app.core.embedding_detector import EmbeddingDetector
from app.core.scoring_engine import calculate_risk
from app.core.output_filter import filter_output  # New: DLP Layer
from app.llm.client import LLMClient
from app.llm.prompt_manager import PromptManager 
from app.utils.logger import log_event

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Aegis-LAF: Initializing Production Security Engines")
    app.state.detector = EmbeddingDetector()
    app.state.llm = LLMClient()
    app.state.prompts = PromptManager()
    print("System Hardened and Ready.")
    yield
    print("Shutting down.")

app = FastAPI(lifespan=lifespan, title="Aegis-LAF | Secure Gateway")

class ChatRequest(BaseModel):
    user_input: str

@app.post("/chat")
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    start_time = time.perf_counter()
    user_text = request.user_input.strip()

    pattern_result = inspect_input(user_text)
    embedding_result = app.state.detector.analyze(user_text)

    risk_score = calculate_risk(pattern_result, embedding_result)

    def get_latency():
        return round((time.perf_counter() - start_time) * 1000, 2)

    if risk_score >= 25:
        background_tasks.add_task(log_event, {
            "input": user_text, 
            "risk_score": risk_score, 
            "action": "blocked",
            "latency_ms": get_latency(),
            "patterns": pattern_result.flags,
            "semantic_similarity": embedding_result["similarity_score"]
        })

        raise HTTPException(
            status_code=403,
            detail={
                "status": "blocked",
                "risk_score": risk_score,
                "reason": "Security Policy Violation",
                "details": {
                    "detected_patterns": pattern_result.flags,
                    "semantic_intent": round(embedding_result["similarity_score"], 4)
                }
            }
        )

    system_prompt = app.state.prompts.get_system_prompt()
    raw_response = await app.state.llm.query(user_text, system_message=system_prompt)

    safe_response = filter_output(raw_response)

    background_tasks.add_task(log_event, {
        "input": user_text, 
        "risk_score": risk_score, 
        "action": "allowed",
        "latency_ms": get_latency()
    })

    return {
        "status": "allowed",
        "risk_score": risk_score,
        "response": safe_response,
        "latency_ms": get_latency()
    }