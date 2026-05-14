import json #Χρησιμοποιείται για parsing του JSON response
import ollama #Χρησιμοποιείται για local LLM classification


MODEL_NAME = "qwen2.5:7b-instruct"

#χτίζει classifier prompt
def classify_query_with_llm(user_query: str) -> dict:
    prompt = f"""
You are a routing classifier for a Climate & Energy AI assistant.

Your job is to decide which system should answer the user's question.

Available routes:

1. "structured"
Use this when the question asks for:
- CO2 emissions data
- top emitters
- country comparisons
- rankings
- numeric values
- trends from datasets
- per-capita emissions
- greenhouse gas statistics

2. "rag"
Use this when the question asks for:
- explanations
- climate risks
- policy descriptions
- EU climate targets
- report-based information
- definitions
- qualitative answers from documents

3. "hybrid"
Use this when the question needs BOTH:
- structured emissions data
- document-based explanation

Examples:

Question: "show me the top emitters"
Answer:
{{"route": "structured", "reason": "The question asks for a ranking based on emissions data."}}

Question: "What are the main climate risks in Europe?"
Answer:
{{"route": "rag", "reason": "The question asks for information from climate reports."}}

Question: "Compare Greece and Germany emissions and explain what this means for climate transition."
Answer:
{{"route": "hybrid", "reason": "The question needs both emissions data and explanatory context."}}

Now classify this question.

USER QUESTION:
{user_query}

Return ONLY valid JSON with this format:
{{"route": "structured" | "rag" | "hybrid", "reason": "..."}}
"""
    #καλεί το local classifier model
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response["message"]["content"].strip()

    def extract_json(text: str) -> dict | None:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1 and end > start:
            json_text = text[start:end + 1]

            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                return None

        return None

    parsed = extract_json(content)

    if parsed is None:
        parsed = {
            "route": "rag",
            "reason": "Fallback route because the LLM did not return valid JSON."
        }

    if parsed.get("route") not in ["structured", "rag", "hybrid"]:
        parsed["route"] = "rag"

    return parsed


if __name__ == "__main__":
    test_queries = [
        "show me the top emitters",
        "compare Greece Germany France",
        "What are the main climate risks in Europe?",
        "What are the EU climate neutrality targets?",
        "Compare Greece and Germany emissions and explain what this means.",
    ]

    for query in test_queries:
        print("\nQUESTION:", query)
        print(classify_query_with_llm(query))