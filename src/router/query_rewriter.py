from ollama import chat


def rewrite_query_with_context(
    user_query: str,
    conversation_context: str,
) -> str:

    prompt = f"""
You are a query rewriting assistant.

Your task:
Rewrite the user's latest question into a fully self-contained query.

Use the previous conversation only when needed.

Rules:
- Preserve the original meaning.
- Keep the rewritten query concise.
- If the latest question already makes sense alone, return it unchanged.
- If the user refers to previous entities (countries, metrics, reports, etc),
  include them explicitly.
- Do not answer the question.
- Only return the rewritten query.

Conversation:
{conversation_context}

Latest user question:
{user_query}

Rewritten query:
"""

    response = chat(
        model="qwen2.5:7b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    rewritten_query = response["message"]["content"].strip()

    return rewritten_query