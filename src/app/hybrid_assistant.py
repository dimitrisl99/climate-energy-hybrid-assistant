from src.router.main_router import is_structured_query
from src.router.structured_router import route_structured_query

from src.generation.structured_answer_generator import (
    generate_structured_answer,
)

from src.rag.rag_answerer import answer_with_rag


def run_assistant(user_query: str):
    if is_structured_query(user_query):
        structured_result = route_structured_query(user_query)

        answer = generate_structured_answer(
            user_query,
            structured_result
        )

        return {
            "type": "structured",
            "answer": answer,
            "raw_result": structured_result,
        }

    rag_answer = answer_with_rag(user_query)

    return {
        "type": "rag",
        "answer": rag_answer,
    }


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

        result = run_assistant(query)

        print(f"\nQUERY TYPE: {result['type']}")
        print("\nANSWER:\n")

        print(result["answer"])

        print("\n")