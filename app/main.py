from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import time

from app.core.input_engine import inspect_input
from app.core.embedding_detector import EmbeddingDetector
from app.core.scoring_engine import calculate_risk
from app.llm.client import LLMClient
from app.utils.logger import log_event

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Aegis-LAF: Initializing Security Engines")
    app.state.detector = EmbeddingDetector()
    app.state.llm = LLMClient()
    print("System Ready.")
    yield
    print("Shutting down.")

app = FastAPI(lifespan=lifespan)

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

    if risk_score >= 35:
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
                    "semantic_vibe": round(embedding_result["similarity_score"], 4)
                }
            }
        )

    response = await app.state.llm.query(user_text)

    background_tasks.add_task(log_event, {
        "input": user_text, 
        "risk_score": risk_score, 
        "action": "allowed",
        "latency_ms": get_latency()
    })

    return {
        "status": "allowed",
        "risk_score": risk_score,
        "response": response
    }