import re

def normalize_code_mixed_text(text: str) -> str:
    if not text:
        return ''
    cleaned = text.lower().strip()
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned
