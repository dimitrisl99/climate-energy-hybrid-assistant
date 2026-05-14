import streamlit as st

from src.app.hybrid_assistant import run_assistant #main orchestrator

st.set_page_config(
    page_title="Climate Energy Assistant",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 Climate Energy Hybrid Assistant")

st.markdown(
    """
    Ask questions about climate risks, energy transition, emissions data, and climate reports.

    This assistant combines structured data analysis, RAG retrieval, and local open-source LLM generation.
    """
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

if user_query:
    st.session_state.messages.append(
        {"role": "user", "content": user_query}
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = run_assistant(user_query)

        st.session_state.last_result = result
        answer = result["answer"]

        st.markdown(answer)
        if "router_reason" in result:
            st.caption(f"Router reason: {result['router_reason']}")

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )


if st.session_state.last_result:
    result = st.session_state.last_result

    st.divider()

    st.subheader("Details")

    st.caption(f"Last query type: `{result['type']}`")

    if result["type"] == "structured" and "raw_result" in result:
        with st.expander("Show raw structured result"):
            raw_result = result["raw_result"]

            if hasattr(raw_result, "shape"):
                st.dataframe(raw_result)
            else:
                st.write(raw_result)

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.session_state.last_result = None
        st.rerun()