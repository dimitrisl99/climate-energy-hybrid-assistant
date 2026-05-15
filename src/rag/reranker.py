from functools import lru_cache
from typing import List

from langchain_core.documents import Document
from sentence_transformers import CrossEncoder


RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


@lru_cache(maxsize=1)
def load_reranker() -> CrossEncoder:
    print("Loading reranker model...")
    return CrossEncoder(RERANKER_MODEL)


def rerank_documents(
    query: str,
    docs: List[Document],
    top_k: int = 5,
) -> List[Document]:
    if not docs:
        return []

    reranker = load_reranker()

    pairs = [
        (query, doc.page_content)
        for doc in docs
    ]

    scores = reranker.predict(pairs)

    scored_docs = list(zip(docs, scores))

    scored_docs = sorted(
        scored_docs,
        key=lambda x: x[1],
        reverse=True
    )

    reranked_docs = [
        doc for doc, score in scored_docs[:top_k]
    ]

    return reranked_docs


if __name__ == "__main__":
    from src.rag.hybrid_retriever import retrieve_hybrid

    query = "What are the main climate risks in Europe?"

    docs = retrieve_hybrid(
        query,
        dense_k=10,
        bm25_k=10,
        final_k=10,
    )

    reranked_docs = rerank_documents(
        query,
        docs,
        top_k=5,
    )

    for i, doc in enumerate(reranked_docs, start=1):
        print(f"\n--- RERANKED RESULT {i} ---")
        print(doc.page_content[:600])
        print(doc.metadata)