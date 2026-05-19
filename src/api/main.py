from fastapi import FastAPI
from pydantic import BaseModel
import csv
from datetime import datetime
from pathlib import Path

from src.app.hybrid_assistant import run_assistant


app = FastAPI(
    title="Climate Energy Assistant API",
    version="1.0.0",
)
FEEDBACK_FILE = Path("data/feedback/feedback.csv")

class ChatMessage(BaseModel):
    role: str
    content: str


class QuestionRequest(BaseModel):
    question: str
    chat_history: list[ChatMessage] = []

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    route: str
    rating: str
    comment: str = ""

@app.get("/")
def root():
    return {
        "success": True,
        "message": "Climate Assistant API is running",
    }


@app.get("/health")
def health_check():
    return {
        "success": True,
        "status": "healthy",
    }


@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = FEEDBACK_FILE.exists()

    with FEEDBACK_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "question",
                "answer",
                "route",
                "rating",
                "comment",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "question": request.question,
                "answer": request.answer,
                "route": request.route,
                "rating": request.rating,
                "comment": request.comment,
            }
        )

    return {
        "success": True,
        "message": "Feedback submitted successfully",
    }

@app.post("/ask")
def ask_question(request: QuestionRequest):
    chat_history = [
        message.model_dump()
        for message in request.chat_history
    ]

    result = run_assistant(
        request.question,
        chat_history=chat_history,
    )

    return {
        "success": True,
        "query": request.question,
        "route": result.get("type"),
        "router_reason": result.get("router_reason"),
        "rewritten_query": result.get("rewritten_query"),
        "answer": result.get("answer"),
        "sources": result.get("sources"),
        "metadata": {
            "backend": "FastAPI",
            "assistant": "Climate Energy Hybrid Assistant",
            "model": "Qwen2.5-7B-Instruct via Ollama",
        },
    }