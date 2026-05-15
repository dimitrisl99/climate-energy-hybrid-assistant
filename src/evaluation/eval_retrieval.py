from src.evaluation.retrieval_test_set import RETRIEVAL_TEST_SET
from src.rag.hybrid_retriever import retrieve_hybrid


def contains_any(text: str, keywords: list[str]) -> bool:
    text = text.lower()

    return any(
        keyword.lower() in text
        for keyword in keywords
    )


def is_relevant(doc, expected_source_keywords, expected_content_keywords) -> bool:
    metadata = doc.metadata

    source = metadata.get("source", "")
    title = metadata.get("title", "")
    content = doc.page_content

    source_text = f"{source} {title}".lower()
    content_text = content.lower()

    source_match = contains_any(source_text, expected_source_keywords)
    content_match = contains_any(content_text, expected_content_keywords)

    return source_match or content_match


def evaluate_retrieval(k: int = 5):
    total = len(RETRIEVAL_TEST_SET)

    hit_at_1 = 0
    hit_at_3 = 0
    hit_at_5 = 0
    reciprocal_ranks = []

    print("\n================ RETRIEVAL EVALUATION ================")

    for item in RETRIEVAL_TEST_SET:
        question = item["question"]
        expected_source_keywords = item["expected_source_keywords"]
        expected_content_keywords = item["expected_content_keywords"]

        docs = retrieve_hybrid(question, final_k=k)

        relevant_rank = None

        for rank, doc in enumerate(docs, start=1):
            if is_relevant(
                doc,
                expected_source_keywords,
                expected_content_keywords
            ):
                relevant_rank = rank
                break

        if relevant_rank is not None:
            if relevant_rank <= 1:
                hit_at_1 += 1
            if relevant_rank <= 3:
                hit_at_3 += 1
            if relevant_rank <= 5:
                hit_at_5 += 1

            reciprocal_ranks.append(1 / relevant_rank)
        else:
            reciprocal_ranks.append(0)

        print("\n------------------------------------------------------")
        print(f"Question: {question}")

        if relevant_rank:
            print(f"Relevant result found at rank: {relevant_rank}")
        else:
            print("No relevant result found")

        print("Top retrieved sources:")
        for i, doc in enumerate(docs, start=1):
            metadata = doc.metadata
            title = metadata.get("title", "Unknown title")
            source = metadata.get("source", "Unknown source")
            page = metadata.get("page_label", metadata.get("page", "N/A"))

            print(f"{i}. {title} | page {page} | {source}")

    mrr = sum(reciprocal_ranks) / total

    print("\n================ SUMMARY ================")
    print(f"Total questions: {total}")
    print(f"Hit@1: {hit_at_1 / total:.2f}")
    print(f"Hit@3: {hit_at_3 / total:.2f}")
    print(f"Hit@5: {hit_at_5 / total:.2f}")
    print(f"MRR@5: {mrr:.2f}")


if __name__ == "__main__":
    evaluate_retrieval(k=5)