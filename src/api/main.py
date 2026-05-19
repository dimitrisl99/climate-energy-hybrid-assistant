from fastapi import FastAPI
from pydantic import BaseModel

from src.app.hybrid_assistant import run_assistant


app = FastAPI()


class ChatMessage(BaseModel):
    role: str
    content: str


class QuestionRequest(BaseModel):
    question: str
    chat_history: list[ChatMessage] = []


@app.get("/")
def root():
    return {"message": "Climate Assistant API is running"}


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
        "query": request.question,
        "route": result.get("type"),
        "router_reason": result.get("router_reason"),
        "rewritten_query": result.get("rewritten_query"),
        "answer": result.get("answer"),
        "sources": result.get("sources"),
    }