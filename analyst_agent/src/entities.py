# entities.py
import re
import spacy
from collections import defaultdict

# Load spaCy model only once
nlp = spacy.load("en_core_web_sm")

# Allowed characters pattern:
# - Letters (unicode word chars), spaces
# - Hyphen, apostrophe, period, comma, ampersand, slash (common in org names)
_ALLOWED_PATTERN = re.compile(r"^[\w\s\-\.'&/,]+$", re.UNICODE)

def _is_clean_entity(text: str) -> bool:
    """
    Filter out entities that:
    - contain any digits, OR
    - contain characters outside a conservative allowed set.
    """
    if not text or not text.strip():
        return False
    s = text.strip()
    # No digits
    if any(ch.isdigit() for ch in s):
        return False
    # Must match allowed characters
    if not _ALLOWED_PATTERN.match(s):
        return False
    return True

def extract_entities(text: str):
    """Extract named entities from text using spaCy, then clean/dedup/sort."""
    if not text:
        return {}

    doc = nlp(text)
    entities = defaultdict(set)  # use set to dedupe per label

    for ent in doc.ents:
        ent_text = ent.text.strip()
        if _is_clean_entity(ent_text):
            # Normalize internal whitespace
            norm = re.sub(r"\s+", " ", ent_text)
            entities[ent.label_].add(norm)

    # Convert to sorted lists alphabetically
    return {label: sorted(list(vals), key=lambda x: x.lower()) for label, vals in entities.items()}
