import os
from dotenv import load_dotenv
from app.document_loader import save_uploaded_file, list_documents
from app.text_extractor import extract_text
from app.text_cleaner import clean_text
from app.chunker import chunk_text
from app.metadata import detect_language, build_metadata
from app.embeddings import embed_texts
from app.vector_store import add_chunks, collection_stats
from app.rag_pipeline import run_pipeline

load_dotenv()


def index_file(path: str):
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return

    filename = os.path.basename(path)
    with open(path, "rb") as f:
        content = f.read()

    try:
        saved_path = save_uploaded_file(filename, content)
        raw_text = extract_text(saved_path)
        cleaned = clean_text(raw_text)

        if not cleaned.strip():
            print(f"⚠️  No extractable text: {filename}")
            return

        language = detect_language(cleaned)
        chunks = chunk_text(cleaned)
        metadatas = [
            build_metadata(source=filename, chunk_index=idx, language=language)
            for idx in range(len(chunks))
        ]
        vectors = embed_texts(chunks, task_type="retrieval_document")
        add_chunks(chunks, vectors, metadatas)

        print(f"Indexed {filename} ({language}, {len(chunks)} chunks)")
    except Exception as e:
        print(f"⚠️  Failed to index {filename}: {e}")


def ask_question(question: str, top_k: int = 5):
    stats = collection_stats()
    if stats["vectors_count"] == 0:
        print("You haven't added any documents yet. Use '/add <file_path>' first.")
        return

    try:
        result = run_pipeline(question, top_k=top_k)
    except RuntimeError as error:
        print(f"{error}")
        return

    print(f"\n{result['answer']}\n")
    if result["sources"]:
        print("Sources:")
        for s in result["sources"]:
            print(f" {s}")
    print()


def print_help():
    print()


def main():
    print("Multilingual Knowledge Agent")
    print_help()

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input in ("/quit", "/exit"):
            print("Goodbye.")
            break
        elif user_input == "/help":
            print_help()
        elif user_input == "/stats":
            print(collection_stats())
        elif user_input == "/list":
            docs = list_documents()
            if not docs:
                print("No documents found yet.")
            else:
                for d in docs:
                    print(f"  {d}")
        elif user_input.startswith("/add "):
            path = user_input[len("/add "):].strip()
            index_file(path)
        else:
            ask_question(user_input)


if __name__ == "__main__":
    main()