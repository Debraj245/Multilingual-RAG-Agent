import os
from app.config import PDF_DIR, DOCX_DIR, TXT_DIR

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def list_documents() -> list[str]:
    paths = []
    for folder in (PDF_DIR, DOCX_DIR, TXT_DIR):
        if not os.path.isdir(folder):
            continue
        for filename in sorted(os.listdir(folder)):
            ext = os.path.splitext(filename)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                paths.append(os.path.join(folder, filename))
    return paths


def save_uploaded_file(filename: str, content: bytes) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        target_dir = PDF_DIR
    elif ext == ".docx":
        target_dir = DOCX_DIR
    elif ext == ".txt":
        target_dir = TXT_DIR
    else:
        raise ValueError(f"Unsupported file type: {ext}. Supported: .pdf, .docx, .txt")

    save_path = os.path.join(target_dir, filename)
    with open(save_path, "wb") as f:
        f.write(content)
    return save_path
