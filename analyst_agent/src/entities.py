import spacy
from collections import defaultdict

# Load spaCy model only once
nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str):
    """Extract named entities from text using spaCy."""
    doc = nlp(text)
    entities = defaultdict(list)
    for ent in doc.ents:
        entities[ent.label_].append(ent.text)
    # Remove duplicates while keeping lists
    return {k: list(set(v)) for k, v in entities.items()}
