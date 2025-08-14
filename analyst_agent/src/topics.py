from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def assign_topics(texts: list, num_clusters: int = 5):
    clean_texts = [t if t.strip() else "" for t in texts]
    if len(clean_texts) < num_clusters:
        num_clusters = max(1, len(clean_texts))
    vectorizer = TfidfVectorizer(max_df=0.8, min_df=1, stop_words="english")
    X = vectorizer.fit_transform(clean_texts)
    km = KMeans(n_clusters=num_clusters, random_state=42, n_init="auto")
    labels = km.fit_predict(X)
    return labels
