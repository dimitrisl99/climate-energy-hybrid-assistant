import sys
import requests
from pathlib import Path
import streamlit as st
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

API_URL = "http://127.0.0.1:8000/ask"
FEEDBACK_API_URL = "http://127.0.0.1:8000/feedback"

st.set_page_config(
    page_title="Climate Energy Assistant",
    page_icon="🌍",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        background-color: #eef6f0;
        color: #276749;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.35rem;
    }
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("🌍 Climate Assistant")

    st.markdown("### What it can do")
    st.markdown(
        """
        - 📊 Structured CO₂ analytics  
        - 📚 RAG over climate reports  
        - 🤖 Local Qwen LLM via Ollama  
        - 🧭 LLM-based routing  
        - 🔀 Hybrid answers  
        """
    )

    st.markdown("### Example questions")

    examples = [
        "Which countries emit the most CO2?",
        "Compare Greece Germany France",
        "What are the main climate risks in Europe?",
        "What are the EU climate neutrality targets?",
        "Compare Greece and Germany emissions and explain what this means.",
    ]

    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.example_prompt = example

    st.markdown("### Model")
    st.caption("Qwen2.5 7B Instruct via Ollama")

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_result = None
        st.rerun()

st.markdown('<div class="main-title">Climate Energy Hybrid Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Ask questions about emissions data, climate risks, EU climate targets, and energy transition reports.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <span class="badge">Structured Data</span>
    <span class="badge">RAG</span>
    <span class="badge">Local LLM</span>
    <span class="badge">Hybrid Routing</span>
    """,
    unsafe_allow_html=True,
)

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_query = st.chat_input("Ask a question about climate or energy...")

if "example_prompt" in st.session_state:
    user_query = st.session_state.example_prompt
    del st.session_state.example_prompt

if user_query:
    previous_messages = st.session_state.messages.copy()

    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Routing query and generating answer..."):
            payload = {
                "question": user_query,
                "chat_history": previous_messages,
            }

            response = requests.post(API_URL, json=payload, timeout=120)
            response.raise_for_status()

            result = response.json()
            if not result.get("success", False):
                st.error("The API returned an unsuccessful response.")
                st.stop()

        st.session_state.last_result = result

        answer = result["answer"]
        st.markdown(answer)

        feedback_col1, feedback_col2 = st.columns(2)

        with feedback_col1:
            useful = st.button(
                "👍 Useful",
                key=f"useful_{len(st.session_state.messages)}"
            )

        with feedback_col2:
            not_useful = st.button(
                "👎 Not useful",
                key=f"not_useful_{len(st.session_state.messages)}"
            )

        feedback_comment = st.text_area(
            "Optional feedback comment",
            key=f"comment_{len(st.session_state.messages)}"
        )

        if useful or not_useful:
            feedback_payload = {
                "question": user_query,
                "answer": answer,
                "route": result["route"],
                "rating": "useful" if useful else "not_useful",
                "comment": feedback_comment,
            }

            feedback_response = requests.post(
                FEEDBACK_API_URL,
                json=feedback_payload,
                timeout=30,
            )

            feedback_response.raise_for_status()

            st.success("Feedback submitted successfully!")

        if "sources" in result and result["sources"]:
            with st.expander("Sources"):
                st.markdown(result["sources"])

        if result["route"] == "structured":
            st.warning("Structured Query")

        elif result["route"] == "rag":
            st.info("RAG Query")

        elif result["route"] == "hybrid":
            st.success("Hybrid Query")

        if "router_reason" in result:
            with st.expander("Router explanation"):
                st.write(result["router_reason"])

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )


