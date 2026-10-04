from app.embeddings import embed_query
from app.vector_store import search
from app.config import TOP_K_DEFAULT


def retrieve(query: str, top_k: int = TOP_K_DEFAULT, language_filter: str | None = None) -> list[dict]:
    query_vector = embed_query(query)
    return search(query_vector, top_k=top_k, language_filter=language_filter)