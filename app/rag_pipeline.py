from app.retriever import retrieve
from app.llm import generate_answer
from app.config import TOP_K_DEFAULT


def _build_prompt(question: str, chunks: list[dict]) -> str:
    context_blocks = []

    for i, c in enumerate(chunks, start=1):
        context_blocks.append(
            f"[Source {i}: {c['source']} | "
            f"language: {c['language']}]\n"
            f"{c['text']}"
        )

    context = "\n\n".join(context_blocks)

    return f"""


{context}

{question}

"""

def run_pipeline(
    question: str,
    top_k: int = TOP_K_DEFAULT,
    language_filter: str | None = None,
) -> dict:

    chunks = retrieve(
        question,
        top_k=top_k,
        language_filter=language_filter,
    )

    if not chunks:
        return {
            "answer": (
                
            ),
            "sources": [],
            "chunks_used": [],
        }

    prompt = _build_prompt(question, chunks)

    answer = generate_answer(prompt)

    sources = sorted(
        {c["source"] for c in chunks}
    )

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": chunks,
    }