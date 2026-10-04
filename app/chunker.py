from app.config import CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE_WORDS,
               overlap: int = CHUNK_OVERLAP_WORDS) -> list[str]:
    if not text or not text.strip():
        return []

    words = text.split()
    n = len(words)
    if n == 0:
        return []

    chunks = []
    start = 0
    while start < n:
        end = min(start + chunk_size, n)
        chunk_str = " ".join(words[start:end]).strip()
        if chunk_str:
            chunks.append(chunk_str)
        if end == n:
            break
        start = end - overlap  

    return chunks
