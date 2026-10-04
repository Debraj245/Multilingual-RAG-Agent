import uuid
import chromadb
from app.config import CHROMA_DB_DIR, COLLECTION_NAME

_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}, 
)

def add_chunks(chunks: list[str], vectors: list[list[float]], metadatas: list[dict]):
    ids = [str(uuid.uuid4()) for _ in chunks]
    _collection.add(
        ids=ids,
        embeddings=vectors,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(ids)

def search(query_vector: list[float], top_k: int = 5, language_filter: str | None = None) -> list[dict]:
    where = {"language": language_filter} if language_filter else None

    results = _collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where=where,
    )

    hits = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for doc, meta, distance in zip(documents, metadatas, distances):
        hits.append({
            "text": doc,
            "source": meta.get("source"),
            "language": meta.get("language"),
            "score": 1 - distance,
        })
    return hits

def collection_stats() -> dict:
    return {"vectors_count": _collection.count()}
