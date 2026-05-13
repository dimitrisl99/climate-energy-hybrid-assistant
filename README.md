# 🌍 Climate Energy Hybrid Assistant

A hybrid AI assistant that combines:

- **Structured querying** over climate & emissions datasets
- **Retrieval-Augmented Generation (RAG)** over climate reports and policy PDFs
- **Local open-source LLM generation** using Qwen via Ollama

The project demonstrates a more realistic enterprise-style GenAI architecture where the assistant can intelligently route between:
- structured analytics queries
- semantic document retrieval
- grounded answer generation

---

# 🚀 Features

## 📊 Structured Query Layer
Query climate and emissions datasets using natural language.

Example queries:
- `show me the top emitters`
- `compare Greece Germany France`
- `show Greece CO2 emissions`

The assistant retrieves real data from structured datasets and generates grounded summaries using an LLM.

---

## 📚 RAG Pipeline
Semantic retrieval over climate and energy reports.

Current document sources include:
- EU Climate Action reports
- European Climate Risk Assessment
- IPCC reports

Pipeline:

```text
PDFs → Chunking → Embeddings → ChromaDB → Retrieval → LLM Answer
```

## 🤖 Local Open-Source LLM

Uses:
```
Qwen2.5-7B-Instruct
via Ollama
```
No external API required.

## 🛠 Tech Stack
- Python
- Pandas
- ChromaDB
- LangChain
- Sentence Transformers
- Ollama
- Qwen2.5
- Streamlit (coming soon)

## 📂 Project Structure

```commandline
src/
├── app/
├── generation/
├── ingestion/
├── rag/
├── router/
└── structured_query/

data/
├── raw/
├── processed/
└── db/
```

## 🔮 Future Improvements

- Semantic chunking
- Hybrid BM25 + dense retrieval
- Reranking
- LLM-based routing
- Text-to-SQL
- Streamlit UI
- Streaming responses
- Retrieval evaluation pipeline
- Citation-aware answer generation
- Tool calling / agents

## Author 

Dimitris Loukakis