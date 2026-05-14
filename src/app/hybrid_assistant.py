from src.router.llm_router import classify_query_with_llm
from src.router.structured_router import route_structured_query

from src.generation.structured_answer_generator import (
    generate_structured_answer,
)

from src.rag.rag_answerer import answer_with_rag


def run_assistant(user_query: str):
    classification = classify_query_with_llm(user_query)
    route = classification["route"]

    if route == "structured":
        structured_result = route_structured_query(user_query)

        answer = generate_structured_answer(
            user_query,
            structured_result
        )

        return {
            "type": "structured",
            "router_reason": classification["reason"],
            "answer": answer,
            "raw_result": structured_result,
        }

    if route == "rag":
        rag_answer = answer_with_rag(user_query)

        return {
            "type": "rag",
            "router_reason": classification["reason"],
            "answer": rag_answer,
        }

    if route == "hybrid":
        rag_answer = answer_with_rag(user_query)

        return {
            "type": "hybrid",
            "router_reason": classification["reason"],
            "answer": rag_answer,
        }

    rag_answer = answer_with_rag(user_query)

    return {
        "type": "rag",
        "router_reason": "Fallback route.",
        "answer": rag_answer,
    }


if __name__ == "__main__":

    test_queries = [
        "show me the top emitters",
        "compare Greece Germany France",
        "What are the main climate risks in Europe?",
        "What are the EU climate neutrality targets?",
        "Compare Greece and Germany emissions and explain what this means.",
    ]

    for query in test_queries:

        print("\n" + "=" * 80)
        print(f"USER QUERY: {query}")
        print("=" * 80)

        result = run_assistant(query)

        print(f"\nQUERY TYPE: {result['type']}")
        print(f"ROUTER REASON: {result['router_reason']}")
        print("\nANSWER:\n")
        print(result["answer"])