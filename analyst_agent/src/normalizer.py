# normalizer.py
import re
import unicodedata
from typing import List

def normalize_text(text: str) -> str:
    """Clean whitespace, normalize Unicode, strip."""
    if not text:
        return ""
    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize_list(items: List[str]) -> List[str]:
    """Normalize, deduplicate while preserving order."""
    seen = set()
    output = []
    for item in items:
        norm = normalize_text(item)
        low = norm.lower()
        if norm and low not in seen:
            seen.add(low)
            output.append(norm)
    return output
