from functools import lru_cache
from typing import List

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from src.rag.chunk_documents import chunk_documents
from src.rag.retriever import retrieve_documents


def tokenize(text: str) -> list[str]:
    return text.lower().split()


@lru_cache(maxsize=1)
def load_chunks_for_bm25():
    print("Loading chunks for BM25...")
    chunks = chunk_documents()

    tokenized_corpus = [
        tokenize(chunk.page_content)
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    return chunks, bm25


def retrieve_bm25(query: str, k: int = 10) -> List[Document]:
    chunks, bm25 = load_chunks_for_bm25()

    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    return [chunks[i] for i in ranked_indices]


def document_key(doc: Document) -> tuple:
    metadata = doc.metadata
    source = metadata.get("source", "")
    page = metadata.get("page", "")
    text_preview = doc.page_content[:120]

    return source, page, text_preview


def reciprocal_rank_fusion(
    dense_docs: List[Document],
    bm25_docs: List[Document],
    k: int = 60,
    final_k: int = 5,
) -> List[Document]:
    scores = {}
    doc_map = {}

    for rank, doc in enumerate(dense_docs, start=1):
        key = document_key(doc)
        scores[key] = scores.get(key, 0) + 1 / (k + rank)
        doc_map[key] = doc

    for rank, doc in enumerate(bm25_docs, start=1):
        key = document_key(doc)
        scores[key] = scores.get(key, 0) + 1 / (k + rank)
        doc_map[key] = doc

    ranked_keys = sorted(
        scores.keys(),
        key=lambda key: scores[key],
        reverse=True
    )

    return [doc_map[key] for key in ranked_keys[:final_k]]


def retrieve_hybrid(query: str, dense_k: int = 8, bm25_k: int = 8, final_k: int = 5):
    dense_docs = retrieve_documents(query, k=dense_k)
    bm25_docs = retrieve_bm25(query, k=bm25_k)

    hybrid_docs = reciprocal_rank_fusion(
        dense_docs=dense_docs,
        bm25_docs=bm25_docs,
        final_k=final_k,
    )

    return hybrid_docs


if __name__ == "__main__":
    test_queries = [
        "What are the main climate risks in Europe?",
        "What are the EU climate neutrality targets?",
        "How does climate change affect agriculture?",
    ]

    for query in test_queries:
        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        docs = retrieve_hybrid(query, final_k=5)

        for i, doc in enumerate(docs, start=1):
            print(f"\n--- RESULT {i} ---")
            print(doc.page_content[:600])
            print(doc.metadata)