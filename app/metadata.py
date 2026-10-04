import datetime
from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:

    try:
        return detect(text[:1000])
    except LangDetectException:
        return "unknown"


def build_metadata(source: str, chunk_index: int, language: str) -> dict:
    
    return {
        "source": source,
        "chunk_index": chunk_index,
        "language": language,
        "ingested_at": datetime.datetime.utcnow().isoformat(),
    }
