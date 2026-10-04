import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(Path(BASE_DIR) / ".env")


DOCUMENTS_DIR = os.path.join(BASE_DIR, "data", "documents")

PDF_DIR = os.path.join(DOCUMENTS_DIR, "pdf")
DOCX_DIR = os.path.join(DOCUMENTS_DIR, "docx")
TXT_DIR = os.path.join(DOCUMENTS_DIR, "txt")

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
CHUNKS_DIR = os.path.join(PROCESSED_DIR, "chunks")


for d in (PDF_DIR, DOCX_DIR, TXT_DIR, CHUNKS_DIR):
    os.makedirs(d, exist_ok=True)


CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")
os.makedirs(CHROMA_DB_DIR, exist_ok=True)


COLLECTION_NAME = "multilingual_knowledge_base"

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

GROQ_LLM_MODEL = os.environ.get(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

CHUNK_SIZE_WORDS = 300
CHUNK_OVERLAP_WORDS = 50
TOP_K_DEFAULT = 5