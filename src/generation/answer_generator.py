import ollama

MODEL_NAME = "qwen2.5:7b-instruct"


def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are a climate and energy transition assistant.

Answer the user's question ONLY using the provided context.

If the answer is not contained in the context, say:
"I could not find the answer in the provided documents."

Be concise, factual, and well-structured.

QUESTION:
{question}

CONTEXT:
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
    sample_context = """
The EU aims to achieve climate neutrality by 2050.
The EU also targets a 55% reduction in greenhouse gas emissions by 2030 compared to 1990 levels.
"""

    question = "What are the EU climate targets?"

    answer = generate_answer(question, sample_context)

    print(answer)