# 🌍 Climate Energy Hybrid Assistant

An enterprise-style hybrid AI assistant for climate and energy intelligence.

This project combines:

- 📊 Structured climate analytics over emissions datasets
- 📚 Retrieval-Augmented Generation (RAG) over climate reports and policy documents
- 🤖 Local open-source LLM generation using Qwen via Ollama
- 🧭 LLM-based intelligent routing between query types
- 🔀 Hybrid answer generation combining structured data + retrieved context

The assistant can dynamically decide whether a user query should be answered using:
- structured emissions data
- semantic document retrieval
- or a hybrid combination of both

---

# 🚀 Features

## 📊 Structured Query Engine

Natural language querying over climate and emissions datasets.

Example queries:

```text
show me the top emitters
compare Greece Germany France
show Greece CO2 emissions
```

The assistant retrieves real structured data and generates grounded summaries using a local LLM.

---

## 📚 RAG Pipeline

Retrieval-Augmented Generation over climate and energy reports.

Current document sources include:

- EU Climate Action Progress Reports
- European Climate Risk Assessment (EEA)
- IPCC AR6 Reports
- EU Climate Policy Documents

Pipeline architecture:

```text
PDFs
  ↓
Chunking
  ↓
Embeddings
  ↓
ChromaDB Vector Store
  ↓
Hybrid Retrieval (Dense + BM25)
  ↓
LLM Grounded Answer Generation
```

---

## 🔀 Hybrid Retrieval

The project uses hybrid retrieval combining:

- Dense semantic retrieval
- BM25 keyword retrieval
- Reciprocal Rank Fusion (RRF)

This improves:
- retrieval relevance
- keyword matching
- factual grounding
- robustness for enterprise-style search

---

## 🧭 LLM-Based Routing

An LLM router dynamically classifies queries into:

- `structured`
- `rag`
- `hybrid`

Examples:

| Query | Route |
|---|---|
| `show me the top emitters` | structured |
| `What are the climate risks in Europe?` | rag |
| `Compare Greece and Germany emissions and explain what this means` | hybrid |

---

## 🤖 Local Open-Source LLM

Uses:

```text
Qwen2.5-7B-Instruct
via Ollama
```

Benefits:

- Fully local inference
- No external API calls
- Lower operational cost
- Privacy-friendly deployment

---

# 🛠 Tech Stack

- Python
- Pandas
- ChromaDB
- LangChain
- Sentence Transformers
- BM25 (`rank-bm25`)
- Ollama
- Qwen2.5
- Streamlit

---

# 🖥 Streamlit UI

Interactive assistant UI featuring:

- Chat-style interface
- Clickable example prompts
- LLM routing visualization
- Source-grounded answers
- Hybrid query support
- Expandable citations & metadata

---

# 📂 Project Structure

```text
src/
├── app/                  # Main assistant orchestration
├── generation/           # LLM answer generators
├── ingestion/            # Data ingestion pipeline
├── rag/                  # Retrieval pipeline
├── router/               # LLM routing logic
├── structured_query/     # Structured analytics engine
└── ui/                   # Streamlit frontend

data/
├── raw/
│   ├── csv/
│   └── pdfs/
├── processed/
└── db/
```

---

# 🔬 Example Capabilities

### Structured Analytics

```text
Compare Germany France Greece
```

### RAG over Climate Reports

```text
What are the main climate risks in Europe?
```

### Hybrid Reasoning

```text
Compare Greece and Germany emissions and explain what this means
```

---

# 🔮 Future Improvements

- Cross-encoder reranking
- Retrieval evaluation pipeline
- Answer faithfulness evaluation
- Streaming responses
- Citation-aware UI
- Advanced semantic chunking
- Tool calling / agents
- Text-to-SQL experimentation
- Multi-document conversational memory

---

# 👨‍💻 Author

Dimitris Loukakis