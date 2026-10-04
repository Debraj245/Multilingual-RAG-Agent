from app.config import EMBEDDING_MODEL
from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

_embedding_model = get_embedding_model()
def embed_texts(
    texts: list[str],
    task_type: str = "retrieval_document"
) -> list[list[float]]:
    return _embedding_model.embed_documents(texts)


def embed_query(query: str) -> list[float]:
    return _embedding_model.embed_query(query)