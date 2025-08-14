# entities.py
import spacy
import re
from collections import defaultdict
from .normalizer import normalize_text

# Single shared spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError("SpaCy English model not installed. Run: python -m spacy download en_core_web_sm")

_ALLOWED_PATTERN = re.compile(r"^[\w\s\-\.'&/,]+$", re.UNICODE)

# Optional alias mapping for normalization (can expand over time)
ALIASES = {
    "u.s.": "United States",
    "usa": "United States",
    "covid": "COVID-19"
}


def _is_clean_entity(text: str) -> bool:
    """Filters out entities with digits or disallowed punctuation."""
    if not text:
        return False
    t = text.strip()
    if any(ch.isdigit() for ch in t):
        return False
    if not _ALLOWED_PATTERN.match(t):
        return False
    return True


def _alias_map(text: str) -> str:
    lower_t = text.lower()
    return ALIASES.get(lower_t, text)


def extract_entities(text: str):
    """
    Run spaCy NER, clean, dedup, normalize, alias-map, and sort.
    """
    if not text:
        return {}

    doc = nlp(text)
    entities = defaultdict(set)

    for ent in doc.ents:
        if not _is_clean_entity(ent.text):
            continue
        norm_text = normalize_text(ent.text)
        norm_text = _alias_map(norm_text)
        entities[ent.label_].add(norm_text)

    return {label: sorted(vals, key=lambda x: x.lower()) for label, vals in entities.items()}
