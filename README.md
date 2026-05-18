# 🌍 Climate Energy Hybrid Assistant

An enterprise-style hybrid AI assistant for climate and energy intelligence.

This project combines:

- 📊 Structured climate analytics over emissions datasets
- 📚 Retrieval-Augmented Generation (RAG) over climate reports and policy documents
- 🤖 Local open-source LLM generation using Qwen via Ollama
- 🧭 LLM-based intelligent routing between query types
- 🔀 Hybrid answer generation combining structured data + retrieved context
- 🧠 Conversational memory with contextual query rewriting
- 🎯 Hybrid retrieval with reranking and evaluation pipelines

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

## 🧠 Conversational Memory

The assistant supports multi-turn conversations with contextual understanding.

Example:

```text
User: Compare Greece Germany France
User: What about Italy?
```

The system automatically rewrites the second query into a context-aware version before routing and retrieval.

This enables:

- conversational follow-up questions
- memory-aware routing
- context-aware structured querying
- more natural assistant behavior

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
Cross-Encoder Reranking
  ↓
LLM Grounded Answer Generation
```

---

## 🔀 Hybrid Retrieval

The project uses hybrid retrieval combining:

- Dense semantic retrieval
- BM25 keyword retrieval
- Reciprocal Rank Fusion (RRF)
- Cross-encoder reranking

This improves:

- retrieval relevance
- keyword matching
- factual grounding
- robustness for enterprise-style search

---

## 🎯 Cross-Encoder Reranking

After retrieval, results are reranked using a cross-encoder model to improve relevance quality.

Benefits:

- better top-k ranking
- improved retrieval precision
- stronger contextual matching
- reduced noisy retrievals

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

## 🔀 Hybrid Answer Generation

Hybrid queries combine:

- structured emissions analytics
- retrieved climate report context
- grounded LLM explanation

Example:

```text
Compare Greece and Germany emissions and explain what this means
```

The assistant combines:

- numerical emissions data
- contextual climate policy information
- grounded explanation generation

---

## 📎 Citation-Aware Answers

RAG and hybrid responses include inline citations and source attribution.

Example:

```text
The EU is on track to achieve its 2030 emissions target [1].
```

With expandable source metadata in the UI.

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
- Cross-Encoder Rerankers
- Ollama
- Qwen2.5
- Streamlit

---

# 🖥 Streamlit UI

Interactive assistant UI featuring:

- Chat-style interface
- Conversational memory
- Clickable example prompts
- LLM routing visualization
- Source-grounded answers
- Hybrid query support
- Expandable citations & metadata
- Query routing explanations
- Structured result visualization

---

# 📂 Project Structure

```text
src/
├── app/                  # Main assistant orchestration
├── evaluation/           # Retrieval & answer evaluation
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

tests/
├── retrieval/
└── generation/

notebooks/
```

---

# 🔬 Evaluation Pipelines

## 📈 Retrieval Evaluation

The project includes a retrieval evaluation pipeline measuring:

- Hit@1
- Hit@3
- Hit@5
- Mean Reciprocal Rank (MRR)

This enables systematic retrieval quality benchmarking.

---

## ✅ Answer Evaluation

Answer evaluation pipeline for validating:

- groundedness
- citation support
- factual consistency
- answer completeness

This supports enterprise-style RAG validation workflows.

---

# 🔬 Example Capabilities

### Structured Analytics

```text
Compare Germany France Greece
```

### Conversational Structured Querying

```text
Compare Greece Germany France
What about Italy?
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

- Streaming responses
- Citation-aware highlighted UI
- Advanced semantic chunking
- Tool calling / agents
- Text-to-SQL experimentation
- Multi-document conversational RAG memory
- Docker deployment
- Observability & logging
- Production API serving
- Authentication & user sessions

---

# 👨‍💻 Author

Dimitris Loukakis