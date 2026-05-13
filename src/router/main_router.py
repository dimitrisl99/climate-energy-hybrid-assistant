from src.router.structured_router import route_structured_query
from src.rag.retriever import retrieve_documents

def is_structured_query(user_query: str) -> bool:
    query = user_query.lower()

    structured_keywords = [
        "top emitters",
        "highest emitters",
        "emissions",
        "co2",
        "compare",
        "per capita",
        "greece",
        "germany",
        "france",
        "china",
        "india",
        "united states",
    ]

    return any(keyword in query for keyword in structured_keywords)

def format_rag_results(query: str, k: int = 3) -> str:
    docs = retrieve_documents(query, k=k)

    output = []
    output.append(f"RAG results for: {query}")
    output.append("\nSources:")

    for i, doc in enumerate(docs, start=1):
        metadata = doc.metadata
        title = metadata.get("title", "Unknown title")
        page = metadata.get("page_label", metadata.get("page", "Unknown page"))
        source = metadata.get("source", "Unknown source")

        output.append(f"[{i}] {title} — page {page} — {source}")

    output.append("\nPassages:")

    for i, doc in enumerate(docs, start=1):
        output.append(f"\n--- Passage [{i}] ---")
        output.append(doc.page_content[:700])

    return "\n".join(output)

def route_user_query(user_query: str):
    if is_structured_query(user_query):
        return route_structured_query(user_query)
    return format_rag_results(user_query, k=3)


if __name__ == "__main__":
    test_queries = [
        "show me the top emitters",
        "compare Greece Germany France",
        "What are the main climate risks in Europe?",
        "What are the EU climate neutrality targets?",
    ]

    for query in test_queries:
        print("\n" + "=" * 80)
        print(f"USER QUERY: {query}")
        print("=" * 80)
        print(route_user_query(query))