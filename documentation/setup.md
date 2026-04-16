# Setup & Installation Guide

This guide ensures your environment is correctly configured to run the Autonomous Workflow ecosystem.

## 📋 Prerequisites

- **Python**: 3.9 or higher.
- **Environment**: Virtual environment highly recommended.

## 🛠️ Installation

1.  **Clone the Repository**:
    ```bash
    git clone <repo-url>
    cd Autonomous_Workflow
    ```

2.  **Install Dependencies**:
    The project uses a variety of NLP and data science libraries.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download Required NLP Models**:
    The Analyst Agent requires specific Spacy and NLTK resources.
    ```bash
    # Spacy Model
    python -m spacy download en_core_web_sm

    # NLTK Resources
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
    ```

## 🔍 Required Packages

- `scikit-learn`: For Topic Clustering (K-Means).
- `yake` / `rake-nltk`: For Keyword Extraction.
- `sumy`: For Narrative Summarization.
- `ddgs`: For Web Search.
- `jinja2`: For Report Generation.
- `numpy`: For pattern analysis calculations.

## 🔑 API Keys

Currently, the system is designed to be **free to run**. 
- **Search**: Uses DuckDuckGo (via `ddgs`), which does not require an API key.
- **Analysis**: Local CPU-based NLP (Spacy/NLTK).

## 🚀 Running the Dashboard (Recommended)

The easiest way to use the system is the **Unified Web Interface**:

```bash
python -m interface.server
```
Visit **[http://localhost:8000](http://localhost:8000)** in your browser.

## 🛠️ Manual CLI Execution (Power Users)

If you prefer to run agents individually:

1. **Research**: `python -m researcher_agent.src.cli "Your Topic"`
2. **Analysis**: `python -m analyst_agent.src.analyze --input output/raw.json`
3. **Forecast**: `python -m forecaster_agent.src.cli output/analysis.json`
4. **Writing**: `python -m writer_agent.src.cli --analyst output/analysis.json`

> [!TIP]
> Each agent's CLI supports `--help` for additional arguments like `--limit` or `--take`.
