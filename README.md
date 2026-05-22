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
- ⚡ Modern React frontend with enterprise-style UI
- 🌊 Streaming AI responses
- 🐳 Dockerized multi-container architecture

The assistant can dynamically decide whether a user query should be answered using:

- structured emissions data
- semantic document retrieval
- or a hybrid combination of both

---

# 🚀 Features

## 📊 Structured Query Engine

Natural language querying over climate and emissions datasets.

### Example Queries

```text
show me the top emitters
compare Greece Germany France
show Greece CO2 emissions
```

The assistant retrieves real structured data and generates grounded summaries using a local LLM.

---

## 🧠 Conversational Memory

The assistant supports multi-turn conversations with contextual understanding.

### Example Conversation

```bash
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

### Pipeline Architecture

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

### Benefits

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

### Examples

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

### Example Hybrid Query

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

### Example

```text
The EU is on track to achieve its 2030 emissions target [1].
```

The frontend includes expandable source cards and metadata visualization.

---

## 🌊 Streaming Responses

The frontend supports real-time streaming AI responses for a ChatGPT-style experience.

Instead of waiting for the full response, answers appear progressively while the model generates output.

### Streaming Stack

- FastAPI `StreamingResponse`
- NDJSON streaming
- Incremental frontend rendering
- Token-style UI updates

This creates a significantly more interactive and production-style user experience.

---

## 🤖 Local Open-Source LLM

### Model

```text
Qwen2.5-7B-Instruct
via Ollama
```

### Benefits

- Fully local inference
- No external API calls
- Lower operational cost
- Privacy-friendly deployment

---

# 🖥 Modern React Frontend

The project includes a redesigned enterprise-style React frontend built with:

- React
- Vite
- Modern CSS
- Responsive dashboard layout
- Chat-style assistant experience

### Frontend Features

- 💬 Chat-based interface
- 🧠 Conversational memory visualization
- 📚 Expandable source cards
- ⚡ Streaming responses
- 🎯 Example prompt shortcuts
- 🧭 Query routing badges
- 🔀 Hybrid response rendering
- 🌌 Enterprise-style animated UI
- 📱 Responsive layout

---

# 🐳 Dockerized Architecture

The project is fully containerized using Docker and Docker Compose.

### Services

- Frontend container
- Backend container

### Run Entire Project

```bash
docker compose up --build
```

### Benefits of Dockerization

- consistent environments
- easier deployment
- simplified onboarding
- production-style architecture
- frontend/backend isolation

---

# 🛠 Tech Stack

## Backend

- Python
- FastAPI
- Pandas
- ChromaDB
- LangChain
- Sentence Transformers
- BM25 (`rank-bm25`)
- Cross-Encoder Rerankers
- Ollama
- Qwen2.5

## Frontend

- React
- Vite
- JavaScript
- Modern CSS

## DevOps

- Docker
- Docker Compose

---

# 📂 Project Structure

```text
climate-energy-assistant/
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
│
├── src/
│   ├── api/
│   ├── generation/
│   ├── rag/
│   ├── router/
│   ├── structured_query/
│   └── memory/
│
├── data/
│   ├── raw/
│   │   ├── csv/
│   │   └── pdfs/
│   └── db/
│
├── notebooks/
├── screenshots/
├── Dockerfile.backend
├── docker-compose.yml
├── requirements.txt
└── README.md
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

## Structured Analytics

```text
Compare Germany France Greece
```

---

## Conversational Structured Querying

```bash
User: Compare Greece Germany France
User: What about Italy?
```

---

## RAG over Climate Reports

```text
What are the main climate risks in Europe?
```

---

## Hybrid Reasoning

```text
Compare Greece and Germany emissions and explain what this means
```

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone https://github.com/dimitrisl99/climate-energy-hybrid-assistant.git
cd climate-energy-hybrid-assistant
```

---

## Run with Docker

Make sure Docker Desktop is running.

```bash
docker compose up --build
```

---

# 🌐 Application URLs

## Frontend

```text
http://localhost:5173
```

## Backend API Docs

```text
http://localhost:8000/docs
```

---

# 📸 Screenshots

![Frontend REACT.png](screenshots/Frontend%20REACT.png)

![Answer.png](screenshots/Answer.png)

---

# 🔮 Future Improvements

- Clickable PDF citations
- Advanced semantic chunking
- Tool calling / agents
- Text-to-SQL experimentation
- Multi-document conversational RAG memory
- Authentication system
- Persistent chat history
- Observability & tracing
- Kubernetes deployment
- Production monitoring
- Cloud deployment pipelines

---

# 🎯 Project Goals

This project was designed to demonstrate:

- production-style AI architecture
- hybrid retrieval systems
- enterprise RAG pipelines
- conversational AI engineering
- local LLM deployment
- modern frontend/backend integration
- Dockerized AI application deployment

---

# 👨‍💻 Author

Dimitris Loukakis

