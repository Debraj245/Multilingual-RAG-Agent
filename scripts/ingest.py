import os
import sys
import time
from app.document_loader import list_documents
from app.text_extractor import extract_text
from app.text_cleaner import clean_text
from app.chunker import chunk_text
from app.metadata import detect_language, build_metadata
from app.embeddings import embed_texts
from app.vector_store import add_chunks

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def timed(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timed
def ingest_all():
    documents = list_documents()

    if not documents:
        print("No documents found in data/documents/pdf, /docx, or /txt.")
        return

    total_chunks = 0
    for path in documents:
        filename = os.path.basename(path)
        print(f"Processing {filename}...")

        raw_text = extract_text(path)
        if not raw_text.strip():
            print(f"  Skipped (no extractable text): {filename}")
            continue

        cleaned = clean_text(raw_text)
        language = detect_language(cleaned)
        chunks = chunk_text(cleaned)

        if not chunks:
            print(f"  Skipped (produced zero chunks): {filename}")
            continue

        metadatas = [
            build_metadata(source=filename, chunk_index=i, language=language)
            for i in range(len(chunks))
        ]

        vectors = embed_texts(chunks, task_type="retrieval_document")
        count = add_chunks(chunks, vectors, metadatas)

        total_chunks += count
        print(f"  Indexed {count} chunks (language: {language})")

    print(f"\nDone. Total chunks indexed this run: {total_chunks}")


if __name__ == "__main__":
    ingest_all()
