import streamlit as st

from src.app.hybrid_assistant import run_assistant #main orchestrator

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
    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Routing query and generating answer..."):
            result = run_assistant(user_query)

        st.session_state.last_result = result

        answer = result["answer"]
        st.markdown(answer)

        if "sources" in result and result["sources"]:
            with st.expander("Sources"):
                st.markdown(result["sources"])

        if result["type"] == "structured":
            st.warning("Structured Query")

        elif result["type"] == "rag":
            st.info("RAG Query")

        elif result["type"] == "hybrid":
            st.success("Hybrid Query")

        if "router_reason" in result:
            with st.expander("Router explanation"):
                st.write(result["router_reason"])

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )


