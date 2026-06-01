from fastapi import FastAPI
from pydantic import BaseModel
import csv
from datetime import datetime
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from src.app.hybrid_assistant import run_assistant
import json
import time
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import uuid


app = FastAPI(
    title="Climate Energy Assistant API",
    version="1.0.0",
)

app.mount(
    "/files",
    StaticFiles(directory="data/raw/pdfs"),
    name="files",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

class ReportRequest(BaseModel):
    question: str
    answer: str
    route: str = ""
    sources: list[dict] = []
    visual_data: list[dict] = []


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

@app.post("/export-report")
def export_report(request: ReportRequest):
    reports_dir = Path("data/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    filename = f"climate_report_{uuid.uuid4().hex[:8]}.pdf"
    filepath = reports_dir / filename

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Climate Energy Assistant Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Generated: {datetime.now().isoformat(timespec='seconds')}", styles["Normal"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("Question", styles["Heading2"]))
    story.append(Paragraph(request.question, styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("AI Analysis", styles["Heading2"]))
    story.append(Paragraph(request.answer.replace("\n", "<br/>"), styles["Normal"]))
    story.append(Spacer(1, 12))

    if request.visual_data:
        story.append(Paragraph("Visual Analytics", styles["Heading2"]))

        table_data = [["Country/Year", "CO2", "CO2 per capita", "GHG"]]

        for item in request.visual_data:
            table_data.append([
                str(item.get("country") or item.get("year") or "N/A"),
                str(item.get("co2", "N/A")),
                str(item.get("co2_per_capita", "N/A")),
                str(item.get("ghg", "N/A")),
            ])

        table = Table(table_data, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))

        story.append(table)
        story.append(Spacer(1, 12))

    if request.sources:
        story.append(Paragraph("Sources", styles["Heading2"]))

        for index, source in enumerate(request.sources, start=1):
            source_text = f"{index}. {source.get('title', 'Unknown source')} — Page {source.get('page', 'N/A')}"
            story.append(Paragraph(source_text, styles["Normal"]))

    doc.build(story)

    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type="application/pdf",
    )

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
        "visual_data": result.get("visual_data", []),
        "metadata": {
            "backend": "FastAPI",
            "assistant": "Climate Energy Hybrid Assistant",
            "model": "Qwen2.5-7B-Instruct via Ollama",
        },
    }


@app.post("/ask/stream")
def ask_question_stream(request: QuestionRequest):

    def generate():
        chat_history = [
            message.model_dump()
            for message in request.chat_history
        ]

        yield json.dumps({
            "type": "status",
            "message": "Routing query..."
        }) + "\n"

        result = run_assistant(
            request.question,
            chat_history=chat_history,
        )

        yield json.dumps({
            "type": "status",
            "message": "Preparing response..."
        }) + "\n"

        answer = result.get("answer", "")
        sources = result.get("sources")

        if not sources and "Sources:" in answer:
            clean_answer, extracted_sources = answer.split("Sources:", 1)
            answer = clean_answer.strip()
            sources = extracted_sources.strip()

        metadata = {
            "type": "metadata",
            "route": result.get("type"),
            "router_reason": result.get("router_reason"),
            "rewritten_query": result.get("rewritten_query"),
            "sources": sources,
            "visual_data": result.get("visual_data", []),
            "chart_type": result.get("chart_type", "bar"),
            "follow_ups": result.get("follow_ups", []),
        }

        yield json.dumps(metadata) + "\n"

        yield json.dumps({
            "type": "status",
            "message": "Generating answer..."
        }) + "\n"

        words = answer.split(" ")

        for word in words:
            chunk = {
                "type": "token",
                "content": word + " ",
            }

            yield json.dumps(chunk) + "\n"
            time.sleep(0.025)

        yield json.dumps({"type": "done"}) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
    )