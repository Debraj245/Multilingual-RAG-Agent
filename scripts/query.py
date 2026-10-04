"""
scripts/query.py

Command-line interface for asking a question against the already-built
knowledge base.

Usage:
    python scripts/query.py "your question here"
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag_pipeline import run_pipeline


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/query.py "your question here"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    result = run_pipeline(question)

    print("\nANSWER:")
    print(result["answer"])

    if result["sources"]:
        print("\nSOURCES:")
        for s in result["sources"]:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
