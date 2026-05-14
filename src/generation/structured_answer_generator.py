import pandas as pd
import ollama


MODEL_NAME = "qwen2.5:7b-instruct"

def dataframe_to_context(result) -> str:
    if isinstance(result, pd.DataFrame):
        return result.to_markdown(index=False)

    if isinstance(result, pd.Series):
        return result.to_frame().to_markdown()

    return str(result)


def generate_structured_answer(question: str, structured_result) -> str:
    context = dataframe_to_context(structured_result)

    prompt = f"""
    You are a climate and energy data assistant.

    Answer the user's question using ONLY the structured data provided below.

    Rules:
    - Do not invent values.
    - Do not use external knowledge.
    - Mention the year if it appears in the data.
    - Preserve all countries shown in the structured data.
    - When comparing numeric values, check the ordering carefully.
    - Do not say that a country has the highest value unless it is numerically the highest.
    - If the data contains multiple metrics, compare each metric separately.
    - Be concise and factual.
    - Include units when possible:
      - CO2 values are in million tonnes.
      - CO2 per capita values are in tonnes per person.
      - total_ghg values are in million tonnes CO2-equivalent.

    QUESTION:
    {question}

    STRUCTURED DATA:
    {context}

    ANSWER:
    """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    from src.router.structured_router import route_structured_query

    question = "show me the top emitters"
    result = route_structured_query(question)

    answer = generate_structured_answer(question, result)

    print(answer)