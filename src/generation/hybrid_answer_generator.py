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

    Rules:
    - Use the structured data for exact numbers, rankings, and country comparisons.
    - Use the document context only for explanations that are explicitly supported.
    - Do not invent values.
    - Do not infer country-specific causes unless the document context explicitly supports them.
    - If the document context is EU-level, say it provides EU-level context, not country-specific causality.
    - Avoid speculative phrases like "could be attributed to" unless the evidence is directly provided.
    - If something is not supported by the provided data or documents, say so clearly.
    - Do not provide general explanations after saying that evidence is not available.
    - End the answer after clearly stating what is supported and what is not supported.

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
