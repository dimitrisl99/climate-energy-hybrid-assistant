import ollama

from src.rag.rag_answerer import build_context_from_docs, format_sources
from src.rag.hybrid_retriever import retrieve_hybrid
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
    - NEVER speculate about causes or explanations not explicitly supported by the provided context.
    - Do not use phrases like:
      "could be attributed to",
      "may be due to",
      "likely because",
      "possibly because".
    - If the reason is not explicitly stated in the context, say:
      "The provided documents do not explain the reasons for this difference."
    - Inline citations must only be used for claims supported by retrieved documents.
    - Do not cite structured data claims with document citations unless the document explicitly supports them.
    - If something is not supported by the provided data or documents, state it clearly.
    - Do not provide general explanations after saying that evidence is not available.
    - End the answer after summarizing what is supported and what is not supported.
    - Maximum length: 180 words.
    - Avoid long report-style sections.
    - Prefer short assistant-style responses.
    - Use at most 3 section headings.
    - Treat retrieved report context as EU-level unless it explicitly names the country being discussed.
    - Do not assign sectoral trends to Germany, Greece, or any country unless that country name appears in the same retrieved passage.
    - Add inline citations using the source ids, like [1] or [2], when using document context.
    - Structured data values do not need document citations.
    - Every explanation based on retrieved documents should include an inline citation.
    
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
    rag_docs = retrieve_hybrid(question, final_k=k)
    return generate_hybrid_answer(question, structured_result, rag_docs)
