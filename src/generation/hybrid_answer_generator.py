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
    - Keep the answer concise and well structured.
    - Start with the key comparison from the structured data.
    - Use bullet points where helpful.
    - Use the structured data for exact numbers, rankings, and country comparisons.
    - Use the document context only for explanations that are explicitly supported.
    - If the document context is EU-level, clearly say that it provides EU-level context, not country-specific causality.
    - Do not invent values.
    - Do not infer country-specific causes unless the document context explicitly supports them.
    - Avoid speculative phrases such as "could be attributed to", "may be due to", or "likely because".
    - If something is not supported by the provided data or documents, state it clearly.
    - Do not provide general explanations after saying that evidence is not available.
    - End the answer after summarizing what is supported and what is not supported.
    - Maximum length: 180 words.
    - Avoid long report-style sections.
    - Prefer short assistant-style responses.
    - Use at most 3 section headings.

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

    return {
        "answer": answer,
        "sources": sources,
    }


def answer_with_hybrid(question: str, structured_result, k: int = 4) -> dict:
    rag_docs = retrieve_documents(question, k=k)
    return generate_hybrid_answer(question, structured_result, rag_docs)
