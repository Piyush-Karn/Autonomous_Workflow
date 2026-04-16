from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

def assign_topics(texts: list, num_clusters: int = 5):
    clean_texts = [t if t.strip() else "" for t in texts]
    if len(clean_texts) < num_clusters:
        num_clusters = max(1, len(clean_texts))
    
    if not clean_texts or all(not t for t in clean_texts):
        return [0] * len(texts), {0: "General"}

    # Specialized noise words for scraping-derived clusters
    SEARCH_NOISE = {
        "com", "bikedekho", "lakh", "crore", "indian", "india", "sales", "electric", 
        "scooter", "scooters", "market", "units", "year", "news", "updates", "times",
        "india", "daily", " Jagran", "Jagran", "bikewale", "hindustan", "hindustantimes"
    }
    
    vectorizer = TfidfVectorizer(
        max_df=0.8, 
        min_df=1, 
        stop_words=list(set(list(TfidfVectorizer(stop_words="english").get_stop_words()) + list(SEARCH_NOISE))),
        max_features=1000
    )
    X = vectorizer.fit_transform(clean_texts)
    
    km = KMeans(n_clusters=num_clusters, random_state=42, n_init="auto")
    labels = km.fit_predict(X)
    
    # Generate descriptive names for each cluster
    cluster_names = {}
    feature_names = vectorizer.get_feature_names_out()
    
    for i in range(num_clusters):
        # Get indices of articles in this cluster
        indices = np.where(labels == i)[0]
        if len(indices) == 0:
            cluster_names[i] = "Miscellaneous"
            continue
            
        # Compute mean TF-IDF vector for this cluster
        cluster_center = X[indices].mean(axis=0).A1
        top_indices = cluster_center.argsort()[::-1][:3]
        top_terms = [feature_names[idx] for idx in top_indices if cluster_center[idx] > 0]
        
        if top_terms:
            cluster_names[i] = " & ".join(t.capitalize() for t in top_terms)
        else:
            cluster_names[i] = f"Cluster {i+1}"
            
    return labels, cluster_names
