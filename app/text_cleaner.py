import re

_MULTI_SPACE = re.compile(r"[ \t]+")
_MULTI_NEWLINE = re.compile(r"\n{3,}")
_PAGE_NUMBER_LINE = re.compile(r"^\s*(page\s*)?\d{1,4}\s*$", re.IGNORECASE)
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def clean_text(text: str) -> str:
    if not text:
        return 

    text = _CONTROL_CHARS.sub("", text)

    lines = text.split("\n")
    cleaned_lines = [line for line in lines if not _PAGE_NUMBER_LINE.match(line)]
    text = "\n".join(cleaned_lines)

    text = _MULTI_SPACE.sub(" ", text)
    text = _MULTI_NEWLINE.sub("\n\n", text)

    return text.strip()
