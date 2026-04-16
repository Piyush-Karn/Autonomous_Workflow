# Analyst Agent — Deep Dive

The **Analyst Agent** is the core processing unit. It transforms raw text into structured data, identifies hidden connections, and writes a narrative summary.

## 🧠 Key Modules

### 1. NLP Fundamentals
- **`sentiment.py`**: Calculates a sentiment score (-1.0 to 1.0) for every article.
- **`entities.py`**: Uses Spacy's Named Entity Recognition (NER) to pull out Organizations, Products, and People.
- **`summarizer.py`**: Uses the `sumy` library (LexRank) to create a concise, 3-sentence summary of long articles.

### 2. Topic Clustering (`topics.py`)
Instead of manual tagging, the agent uses **Machine Learning** to find themes:
- It uses **TF-IDF Vectorization** to convert text into numbers.
- It applies **K-Means Clustering** to group similar articles together.
- It automatically **labels clusters** by identifying the most mathematically significant words in each group (e.g., *"Range & Km & Features"*).

### 3. Pattern Discovery (`patterns.py`)
This module looks for meta-insights across the entire data bundle:
- **Entity Co-occurrence**: Finds entities that frequently appear in the same context (e.g., identifying that "Ola Electric" and "Charging Infrastructure" are strongly linked).
- **Sentiment Divergence**: Identifies "polarizing" entities where different sources have widely different opinions.
- **Historical Trajectory**: Calculates a growth/stability trend based on article volume overtime.

### 4. Narrative Synthesis (`synthesizer.py`)
This is the final step where the agent "writes" the insights. It takes all the patterns and meta-data and converts them into structured **Executive Highlights** using professional, journalistic prose.

## 📂 Internal Structure

- `src/analyze.py`: The main controller that orchestrates the entire pipeline.
- `src/schema.py`: Defines the `AnalysisBundle` and `ArticleAnalysis` dataclasses, ensuring consistency for the Writer Agent.

## 🛠️ Customization

- **Topic Cluster Count**: You can change the `num_clusters` in `analyze_research_file` (default is 5).
- **Stopword Filtering**: The `topics.py` file contains a dedicated `SEARCH_NOISE` list to filter out generic terms from topic names.
