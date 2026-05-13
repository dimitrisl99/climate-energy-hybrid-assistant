from src.rag.retriever import retrieve_documents
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


def format_sources(docs) -> str:
    sources = []

    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata

        title = metadata.get("title", "Unknown title")
        page = metadata.get("page_label", metadata.get("page", "Unknown page"))
        source = metadata.get("source", "Unknown source")

        sources.append(f"[{i}] {title} — page {page} — {source}")

    return "\n".join(sources)


def answer_with_rag(question: str, k: int = 4) -> str:
    docs = retrieve_documents(question, k=k)
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