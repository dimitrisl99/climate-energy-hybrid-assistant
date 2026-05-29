from src.router.llm_router import classify_query_with_llm
from src.router.query_rewriter import rewrite_query_with_context
from src.router.structured_router import route_structured_query

from src.generation.hybrid_answer_generator import answer_with_hybrid
from src.generation.structured_answer_generator import generate_structured_answer

from src.rag.rag_answerer import answer_with_rag

def build_visual_data(structured_result):
    if structured_result is None:
        return []

    rows = []

    if isinstance(structured_result, list):
        rows = structured_result

    elif isinstance(structured_result, dict):
        for key in ["results", "data", "rows", "records"]:
            value = structured_result.get(key)

            if value is None:
                continue

            if hasattr(value, "to_dict"):
                rows = value.to_dict(orient="records")
            elif isinstance(value, list):
                rows = value
            elif isinstance(value, dict):
                rows = [value]

            break

    elif hasattr(structured_result, "to_dict"):
        rows = structured_result.to_dict(orient="records")

    visual_data = []

    for row in rows[:6]:
        if not isinstance(row, dict):
            continue

        visual_data.append({
            "country": row.get("country") or row.get("Country"),
            "co2": row.get("co2") or row.get("co2_emissions") or row.get("CO2"),
            "co2_per_capita": row.get("co2_per_capita") or row.get("CO2 per capita"),
            "ghg": row.get("ghg") or row.get("ghg_emissions") or row.get("GHG"),
        })

    return visual_data


def detect_chart_type(query: str):
    query = query.lower()

    trend_keywords = [
        "trend",
        "over time",
        "history",
        "historical",
        "evolution",
        "change over time",
        "over the years",
    ]

    if any(keyword in query for keyword in trend_keywords):
        return "line"

    return "bar"

def build_conversation_context(chat_history: list[dict], max_turns: int = 4) -> str:
    recent_messages = chat_history[-max_turns:]
    context_lines = []

    for message in recent_messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")

        if content:
            context_lines.append(f"{role.upper()}: {content}")

    return "\n".join(context_lines)


def build_routing_query(user_query: str, chat_history: list[dict]) -> str:
    conversation_context = build_conversation_context(chat_history)

    if not conversation_context:
        return user_query

    return f"""
Conversation so far:
{conversation_context}

Current user question:
{user_query}
"""


def run_assistant(user_query: str, chat_history: list[dict] | None = None):
    chat_history = chat_history or []

    conversation_context = build_conversation_context(chat_history)

    routing_query = build_routing_query(
        user_query=user_query,
        chat_history=chat_history,
    )

    classification = classify_query_with_llm(routing_query)
    route = classification["route"]

    rewritten_query = user_query

    if conversation_context and route in ["structured", "rag", "hybrid"]:
        rewritten_query = rewrite_query_with_context(
            user_query=user_query,
            conversation_context=conversation_context,
        )

        print("\nREWRITTEN QUERY:")
        print(rewritten_query)

    if route == "structured":
        structured_result = route_structured_query(rewritten_query)

        print("\nSTRUCTURED RESULT TYPE:")
        print(type(structured_result))

        print("\nSTRUCTURED RESULT:")
        print(structured_result)

        answer = generate_structured_answer(
            rewritten_query,
            structured_result,
        )

        return {
            "type": "structured",
            "router_reason": classification["reason"],
            "rewritten_query": rewritten_query,
            "answer": answer,
            "raw_result": structured_result,
            "visual_data": build_visual_data(structured_result),
            "chart_type": detect_chart_type(rewritten_query),
        }

    if route == "rag":
        rag_answer = answer_with_rag(rewritten_query)

        return {
            "type": "rag",
            "router_reason": classification["reason"],
            "rewritten_query": rewritten_query,
            "answer": rag_answer,
        }

    if route == "hybrid":
        structured_result = route_structured_query(rewritten_query)

        print("\nHYBRID STRUCTURED RESULT TYPE:")
        print(type(structured_result))

        print("\nHYBRID STRUCTURED RESULT:")
        print(structured_result)

        hybrid_response = answer_with_hybrid(
            rewritten_query,
            structured_result,
            k=4,
        )

        return {
            "type": "hybrid",
            "router_reason": classification["reason"],
            "rewritten_query": rewritten_query,
            "answer": hybrid_response["answer"],
            "sources": hybrid_response["sources"],
            "raw_result": structured_result,
            "visual_data": build_visual_data(structured_result),
            "chart_type": detect_chart_type(rewritten_query),
        }

    rag_answer = answer_with_rag(rewritten_query)

    return {
        "type": "rag",
        "router_reason": "Fallback route.",
        "rewritten_query": rewritten_query,
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
        print(f"REWRITTEN QUERY: {result.get('rewritten_query')}")
        print("\nANSWER:\n")
        print(result["answer"])