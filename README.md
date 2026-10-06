# 🌍 Multilingual RAG Knowledge Agent

> **A multilingual AI knowledge agent that uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from documents and generate grounded, source-aware answers.**

**Project:** Design of a Multilingual Intelligent AI Agent using LLM and Retrieval-Augmented Generation for Accurate Information Retrieval.

---

## 🚀 Overview

The **Multilingual RAG Knowledge Agent** allows users to upload documents and ask questions about their content using natural language.

The system supports **PDF, DOCX, and TXT** documents and is designed for multilingual and cross-lingual retrieval.

Instead of relying only on keyword matching, the system converts document content and queries into semantic embeddings, retrieves relevant context from a vector database, and passes that context to an LLM to generate a grounded response.

### ✨ What makes it different?

- 🌐 Multilingual semantic retrieval
- 🔎 Meaning-based document search
- 📚 PDF, DOCX, and TXT support
- 🧠 Retrieval-Augmented Generation
- 🗃️ Persistent local vector database
- 🤖 Groq-powered LLM generation
- 📌 Source-aware answers

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   PDF / DOCX / TXT  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Document Loader   │
                    │ app/document_loader  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Extraction   │
                    │ app/text_extractor  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Text Cleaning    │
                    │  app/text_cleaner   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Chunking       │
                    │    app/chunker      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Metadata       │
                    │    app/metadata     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Embeddings      │
                    │    app/embeddings   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      ChromaDB       │
                    │    Vector Store     │
                    └──────────┬──────────┘
                               │
                         Semantic Search
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Retriever      │
                    │    app/retriever    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Relevant Context   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Groq LLM        │
                    │      app/llm        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Answer + Sources    │
                    │ app/rag_pipeline    │
                    └─────────────────────┘
```

---

## 🔄 RAG Pipeline

The application follows a standard Retrieval-Augmented Generation workflow:

### 1. Document ingestion

Users provide documents in:

- PDF
- DOCX
- TXT

### 2. Text extraction

Text is extracted from the uploaded documents and normalized for processing.

### 3. Text cleaning

Unnecessary formatting and noisy content are removed before chunking.

### 4. Chunking

Large documents are divided into smaller overlapping chunks so that relevant sections can be retrieved efficiently.

### 5. Metadata generation

Each chunk contains metadata such as:

```text
source
language
timestamp
```

This allows retrieved information to be associated with its original document.

### 6. Embedding generation

The chunks are converted into semantic vectors using:

```text
sentence-transformers/paraphrase-multilingual-mpnet-base-v2
```

This allows the system to perform semantic retrieval across supported languages without requiring a translation step.

### 7. Vector storage

Embeddings and metadata are stored in **ChromaDB**.

### 8. Retrieval

When a user asks a question, the query is embedded and the most semantically relevant document chunks are retrieved.

### 9. Generation

The retrieved context is passed to the **Groq LLM**, which generates an answer based on the available context.

### 10. Source attribution

The final response includes the source information associated with the retrieved context.

---

## 🧠 Key Design Decisions

### Multilingual Embeddings

The project uses:

```text
sentence-transformers/paraphrase-multilingual-mpnet-base-v2
```

This provides multilingual semantic embeddings and enables cross-lingual retrieval without translating every document before indexing.

For example:

```text
Document: "Machine learning is a subset of artificial intelligence."

Query: "What is machine learning?"
```

The system can retrieve the relevant content based on semantic similarity rather than exact keyword matching.

---

### 🗃️ ChromaDB

ChromaDB is used as the local vector database.

**Why ChromaDB?**

- Easy local setup
- Persistent storage
- Python-friendly
- Suitable for academic and prototype applications
- No separate database server required

---

### ⚡ Groq LLM

Groq is used for final response generation.

The LLM is intentionally used **after retrieval** rather than as the document search mechanism.

```text
User Query
    ↓
Embedding
    ↓
Semantic Retrieval
    ↓
Relevant Context
    ↓
Groq LLM
    ↓
Grounded Answer
```

This separation helps keep retrieval and generation as distinct components.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| RAG | Custom RAG Pipeline |
| Embeddings | Sentence Transformers |
| Embedding Model | `paraphrase-multilingual-mpnet-base-v2` |
| Vector Database | ChromaDB |
| LLM | Groq |
| UI | Streamlit |
| Document Formats | PDF, DOCX, TXT |
| Environment | Python Virtual Environment |

---

## 📁 Project Structure

```text
multilingual-rag/
│
├── app/
│   ├── document_loader.py
│   ├── text_extractor.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── metadata.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── llm.py
│   └── rag_pipeline.py
│
├── data/
│   └── documents/
│       ├── pdf/
│       ├── docx/
│       └── txt/
│
├── scripts/
│   ├── ingest.py
│   └── query.py
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd multilingual-rag
```

### 2. Create a virtual environment

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your `.env` file:

```bash
cp .env.example .env
```

Then add your API key:

```env
GROQ_API_KEY=your_key_here
```

> ⚠️ Never commit your `.env` file or API keys to GitHub.

---

## 📚 Add Documents

Place your documents inside:

```text
data/documents/
├── pdf/
├── docx/
└── txt/
```

Example:

```text
data/documents/pdf/
├── artificial_intelligence.pdf
└── machine_learning.pdf
```

---

## ▶️ Running the Project

### Ingest documents

```bash
python scripts/ingest.py
```

### Query through CLI

```bash
python scripts/query.py "What is machine learning?"
```

### Run the Streamlit application

```bash
streamlit run app.py
```

The Streamlit interface allows you to upload documents and interact with the knowledge agent.

---

## 💬 Example

### Query

```text
What is the main purpose of retrieval augmented generation?
```

### Pipeline

```text
Question
   ↓
Query Embedding
   ↓
Semantic Search
   ↓
Top Relevant Chunks
   ↓
Context Construction
   ↓
Groq LLM
   ↓
Grounded Answer
   ↓
Source Information
```

---

## 🌐 Multilingual Retrieval

The system is designed to support multilingual document collections.

For example, a user can ask a question in one supported language while relevant information may exist in another language.

```text
User Query
    │
    ▼
Multilingual Embedding
    │
    ▼
ChromaDB Semantic Search
    │
    ▼
Relevant Cross-Lingual Context
    │
    ▼
LLM
    │
    ▼
Answer
```

The effectiveness of cross-lingual retrieval depends on the embedding model and the language being used, so multilingual performance should be evaluated with representative test data.

---

## 🔐 Security

API keys and secrets should be stored in environment variables.

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
chroma/
```

Never upload API keys, tokens, or credentials to the repository.

---

## ⚠️ Current Limitations

- Scanned/image-only PDFs are not currently supported because OCR is not implemented.
- Very short documents may produce unreliable language detection.
- Retrieval quality depends on document quality, chunking, and embedding performance.
- Groq API usage requires network access and is subject to API limits.
- The current retriever is primarily semantic/vector-based.

---

## 🗺️ Roadmap

### ✅ Completed

- [x] PDF/DOCX/TXT document ingestion
- [x] Text extraction
- [x] Text cleaning
- [x] Document chunking
- [x] Metadata handling
- [x] Multilingual embeddings
- [x] ChromaDB vector storage
- [x] Semantic retrieval
- [x] Groq LLM integration
- [x] CLI querying
- [x] Streamlit interface

### 🚧 In Progress / Planned

- [ ] Hybrid retrieval — BM25 + vector search
- [ ] Reranking retrieved documents
- [ ] Query rewriting
- [ ] Multi-hop question answering
- [ ] Retrieval evaluation
- [ ] Answer quality evaluation
- [ ] RAGAS-based evaluation
- [ ] OCR for scanned documents
- [ ] Improved source citation
- [ ] Conversation memory

---

## 📊 Evaluation

A future evaluation module will measure retrieval and generation quality using metrics such as:

- **Context Precision**
- **Context Recall**
- **Faithfulness**
- **Answer Relevance**
- **Retrieval Recall@K**

This will make it possible to compare different retrieval strategies and measure improvements objectively.

---

## 🎯 Project Goals

The long-term goal is to build a reliable multilingual knowledge agent capable of:

```text
        Documents
            ↓
   Multilingual Retrieval
            ↓
      Relevant Context
            ↓
       LLM Reasoning
            ↓
   Grounded Response
            ↓
    Source Attribution
```

The project focuses on reducing unsupported LLM responses by grounding generation in retrieved document context.

