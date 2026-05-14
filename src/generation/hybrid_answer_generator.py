import pandas as pd
import ollama

from src.rag.rag_answerer import build_context_from_docs, format_sources
from src.rag.retriever import retrieve_documents
from src.generation.structured_answer_generator import dataframe_to_context


MODEL_NAME = "qwen2.5:7b-instruct"


def generate_hybrid_answer(question: str, structured_result, rag_docs) -> str:
    structured_context = dataframe_to_context(structured_result)
    rag_context = build_context_from_docs(rag_docs)
    sources = format_sources(rag_docs)

    prompt = f"""
You are a climate and energy transition assistant.

Answer the user's question using BOTH:
1. the structured emissions data
2. the retrieved document context

Use the structured data for numbers, rankings, and comparisons.
Use the document context for explanation, interpretation, and climate policy context.

Do not infer country-specific explanations unless they are explicitly supported by the document context.
Use the structured data only for the countries and values shown in the table.
If the document context discusses the EU generally, clearly say that it provides EU-level context, not country-specific causality.
Do not use phrases like "could be attributed to" unless the evidence is directly provided.

QUESTION:
{question}

STRUCTURED DATA:
{structured_context}

DOCUMENT CONTEXT:
{rag_context}

ANSWER:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response["message"]["content"]

    return f"{answer}\n\nSources:\n{sources}"


def answer_with_hybrid(question: str, structured_result, k: int = 4) -> str:
    rag_docs = retrieve_documents(question, k=k)
    return generate_hybrid_answer(question, structured_result, rag_docs)
