# Multilingual RAG Knowledge Agent

**Project:** Design of a Multilingual Intelligent AI Agent using LLM and
Retrieval-Augmented Generation for Accurate Information Retrieval

## What this does
Upload documents (PDF, DOCX, TXT) in any language, and ask questions about
them in any language — the system retrieves the most relevant content by
*meaning* (not keyword matching) and generates a grounded answer, citing
exactly which document it came from.

## Pipeline

Documents (PDF/DOCX/TXT)
│
▼
Document Loader app/document_loader.py
│
▼
Text Extraction app/text_extractor.py
│
▼
Text Cleaning app/text_cleaner.py
│
▼
Chunking app/chunker.py
│
▼
Metadata app/metadata.py (source / language / timestamp)
│
▼
Embeddings app/embeddings.py (multilingual sentence-transformers)
│
▼
ChromaDB (Vector DB) app/vector_store.py
│
▼
Retriever app/retriever.py
│
▼
Relevant Context
│
▼
LLM (Groq) app/llm.py
│
▼
Answer + Sources app/rag_pipeline.py


## Project structure

multilingual-rag/
├── data/
│   ├── documents/
│   │   ├── pdf/
│   │   ├── docx/
│   │   └── txt/
│   └── processed/
│       └── chunks/
├── chroma_db/                     # ChromaDB persistent storage (auto-created)
├── app/
│   ├── __init__.py
│   ├── config.py                  # paths, model names, chunk size, API keys
│   ├── document_loader.py         # finds/saves files across pdf/docx/txt
│   ├── text_extractor.py          # extracts text per format
│   ├── text_cleaner.py            # removes noise, extra whitespace
│   ├── chunker.py                 # splits into overlapping chunks
│   ├── metadata.py                # source/language tagging
│   ├── embeddings.py              # multilingual sentence-transformers embeddings
│   ├── vector_store.py            # ChromaDB add/search
│   ├── retriever.py               # query -> embed -> search
│   ├── llm.py                     # Groq LLM calls
│   ├── rag_pipeline.py            # retrieval + LLM answer generation
│   └── utils.py                   # shared helpers
├── scripts/
│   ├── ingest.py                  # CLI: process all documents into the KB
│   └── query.py                   # CLI: ask a question from the terminal
├── tests/
├── app.py                         # Streamlit chat UI (main entry point)
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

## Quick start
```bash
# 1. Create environment
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key
cp .env.example .env
# then edit .env and add: GROQ_API_KEY=your_key_here

# 4. Add documents
# Drop PDF/DOCX/TXT files into data/documents/pdf/, /docx/, or /txt/

# 5a. Ingest via CLI
python scripts/ingest.py

# 5b. Ask via CLI
python scripts/query.py "your question here"

# 5c. Or run the full chat UI (handles upload + ingestion + asking)
streamlit run app.py
```

## Key design choices
- **Embeddings**: `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
  — supports 100+ languages natively, no translation step required. Same-meaning
  sentences across different languages land close together in vector space,
  enabling cross-lingual retrieval.
- **Vector DB**: ChromaDB, running locally in persistent mode — no separate
  server needed, good fit for a single-machine academic project.
- **LLM**: Groq (fast inference), used only to generate the final answer from
  retrieved context — never to search or rank documents.
- **Chunking**: word-based with overlap, kept language-agnostic so it behaves
  consistently across every script in the corpus.

## Known limitations
- No OCR — scanned/image-only PDFs yield no extractable text.
- Language detection can be unreliable on very short documents.
- Groq API calls require network access and count against your quota.

## Status
- **Phase 2 (this phase)**: Document ingestion + multilingual knowledge base — complete.
- **Next**: Improve retrieval (hybrid search, reranking), add evaluation metrics,
  and expand query handling (rewriting, multi-hop questions).
