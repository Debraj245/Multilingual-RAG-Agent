import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from app.config import GROQ_LLM_MODEL

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                f"GROQ_API_KEY is not set. Expected .env at: {BASE_DIR / '.env'}"
            )
        _client = Groq(api_key=api_key)
    return _client


def generate_answer(prompt: str) -> str:
    client = _get_client()

    response = client.chat.completions.create(
        model=GROQ_LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_completion_tokens=2048,
    )

    return response.choices[0].message.content