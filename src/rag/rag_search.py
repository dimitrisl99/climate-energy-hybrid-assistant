from src.rag.retriever import retrieve_documents

def format_source(doc, index: int) -> str:
    metadata = doc.metadata

    title = metadata.get("title", "Unknown title")
    source = metadata.get("source", "Unknown source")
    page = metadata.get("page_label", metadata.get("page", "Unknown page"))

    return f"[{index}] {title} — page {page} — {source}"


def search_rag(query: str, k: int = 5) -> None:
    docs = retrieve_documents(query, k=k)

    print(f"\nQUERY: {query}")
    print("\nRetrieved sources:")

    for i, doc in enumerate(docs, start=1):
        print(format_source(doc, i))

    print("\nRetrieved passages:")

    for i, doc in enumerate(docs, start=1):
        print(f"\n--- Passage [{i}] ---")
        print(doc.page_content[:1000])


if __name__ == "__main__":
    test_queries = [
        "What are the EU climate neutrality targets?",
        "What are the main climate risks in Europe?",
        "How is the EU reducing greenhouse gas emissions?",
    ]

    for q in test_queries:
        search_rag(q, k=3)