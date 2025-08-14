# Analyst Agent

## 📌 Overview
The **Analyst Agent** processes output from the Researcher Agent and produces structured insights:
- Summaries of each article.
- Named entity extraction (people, places, organizations, dates, etc.).
- Common keywords.

## 🚀 Usage
Run from inside the `analyst_agent` folder:

```bash
python -m src.cli "../researcher_agent/output/research_output_<timestamp>.json"
