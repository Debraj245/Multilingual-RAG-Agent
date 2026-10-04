"""
Basic unit tests for the text-processing modules.
Run with: python -m pytest tests/
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.text_cleaner import clean_text
from app.chunker import chunk_text


def test_clean_text_removes_page_numbers():
    raw = "Some content.\n42\nMore content."
    cleaned = clean_text(raw)
    assert "42" not in cleaned.split("\n")


def test_clean_text_collapses_whitespace():
    raw = "Too    many     spaces"
    assert clean_text(raw) == "Too many spaces"


def test_chunk_text_empty_input():
    assert chunk_text("") == []
    assert chunk_text("   ") == []


def test_chunk_text_respects_overlap():
    text = " ".join(str(i) for i in range(1000))  # 1000 words
    chunks = chunk_text(text, chunk_size=300, overlap=50)
    assert len(chunks) > 1
    # Overlap: last words of chunk 1 should reappear at the start of chunk 2
    first_chunk_words = chunks[0].split()
    second_chunk_words = chunks[1].split()
    assert first_chunk_words[-1] in second_chunk_words[:60]


if __name__ == "__main__":
    test_clean_text_removes_page_numbers()
    test_clean_text_collapses_whitespace()
    test_chunk_text_empty_input()
    test_chunk_text_respects_overlap()
    print("All tests passed.")
