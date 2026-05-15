from src.rag.hybrid_retriever import retrieve_hybrid
from src.generation.answer_generator import generate_answer


def build_context_from_docs(docs) -> str:
    context_parts = []

    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata

        title = metadata.get("title", "Unknown title")
        page = metadata.get("page_label", metadata.get("page", "Unknown page"))

        context_parts.append(
            f"[Source {i}] {title}, page {page}\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(context_parts)


def format_sources(docs):
    seen = set()
    formatted = []

    source_number = 1

    for doc in docs:
        metadata = doc.metadata

        source = metadata.get("source", "Unknown source")
        page = metadata.get("page_label", metadata.get("page", "N/A"))
        title = metadata.get("title", "Unknown title")

        key = (source, page)

        if key in seen:
            continue

        seen.add(key)

        formatted.append(
            f"[{source_number}] {title} — page {page} — {source}"
        )

        source_number += 1

    return "\n".join(formatted)


def answer_with_rag(question: str, k: int = 4) -> str:
    docs = retrieve_hybrid(question, final_k=k)
    context = build_context_from_docs(docs)

    answer = generate_answer(question, context)
    sources = format_sources(docs)

    return f"{answer}\n\nSources:\n{sources}"


if __name__ == "__main__":
    test_questions = [
        "What are the main climate risks in Europe?",
        "What are the EU climate neutrality targets?",
        "How is the EU reducing greenhouse gas emissions?",
    ]

    for question in test_questions:
        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")
        print("=" * 80)
        print(answer_with_rag(question, k=4))