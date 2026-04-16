# 🌌 Autonomous Workflow

<div align="center">
  <img src="assets/banner.png" alt="Autonomous Workflow Banner" width="100%">
  <br/>
  <i>Intelligent Multi-Agent Pipeline for Automated Research, Analysis, and Reporting</i>
  <br/>
  <br/>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-F7931E?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Architecture-Modular-blueviolet?style=for-the-badge" alt="Architecture">
  <img src="https://img.shields.io/badge/AI_Agents-4-FF6F61?style=for-the-badge" alt="AI Agents">
</div>

---

## 🎯 Vision
**Autonomous Workflow** is a state-of-the-art suite of AI agents designed to automate the heavy lifting of market research, technical analysis, and strategic forecasting. Whether you need to track emerging trends or synthesize large volumes of web data, this pipeline delivers high-fidelity reports with zero manual intervention.

## 🤖 The Agent Ecosystem

The project is built on a modular "Chain of Thought" architecture where specialized agents collaborate to process information:

| Agent | Icon | Role | Key Technologies |
| :--- | :---: | :--- | :--- |
| **Researcher** | 🔍 | **Data Discovery**: Searches the web, scrapes articles, and extracts core content. | `DuckDuckGo`, `Newspaper3k`, `BeautifulSoup` |
| **Analyst** | 🧠 | **Semantic Intelligence**: Extracts keywords, calculates sentiment, and summarizes findings. | `SpaCy`, `NLTK`, `Gensim`, `Sumy` |
| **Forecaster** | 📈 | **Predictive Modeling**: Identifies patterns and projects future trends using ML. | `Scikit-learn`, `LightGBM`, `XGBoost`, `Statsmodels` |
| **Writer** | ✍️ | **Professional Delivery**: Generates cinematic reports in HTML, Markdown, or PDF format. | `Jinja2`, `Matplotlib`, `WeasyPrint` |

## 🔄 Workflow Architecture

```mermaid
graph LR
    User([User Prompt]) ---|Query| R[<b>Researcher</b>]
    R ---|Raw Articles| A[<b>Analyst</b>]
    A ---|Insights| F[<b>Forecaster</b>]
    F ---|Predictions| W[<b>Writer</b>]
    W ---|Report| Output([Polished Report])

    style R fill:#1e293b,stroke:#3b82f6,color:#fff
    style A fill:#1e293b,stroke:#8b5cf6,color:#fff
    style F fill:#1e293b,stroke:#ec4899,color:#fff
    style W fill:#1e293b,stroke:#10b981,color:#fff
    style User fill:#0f172a,stroke:#fff,color:#fff
    style Output fill:#0f172a,stroke:#fff,color:#fff
```

## ✨ Key Features
- **🚀 One-Touch Pipeline**: Go from a topic to a 10-page report with a single command.
- **🛡️ Quality Assurance**: Built-in validators ensure data integrity across agent transitions.
- **📊 Interactive Visuals**: Automatic generation of trend charts and sentiment maps.
- **📄 Multi-Format Output**: Export results to high-end **HTML5**, **Github-Flavored Markdown**, or **Print-Ready PDF**.
- **🔌 Highly Extensible**: Easily swap out extraction logic or ML models for your specific needs.

## 🚀 Getting Started

### 📋 Prerequisites
- **Python 3.9+**
- (Optional) **Cairo/Pango** (Required for PDF export via WeasyPrint)

### ⚙️ Installation
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/Piyush-Karn/Autonomous_Workflow.git
   cd Autonomous_Workflow
   ```

2. **Setup Venv & Dependencies**:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate

   # Install all agent requirements
   pip install -r researcher_agent/requirements.txt
   pip install -r analyst_agent/requirements.txt
   pip install -r forecaster_agent/requirements.txt
   pip install -r writer_agent/requirements.txt
   ```

## 🛠️ Usage Guide

Run the pipeline sequentially to see the agents in action:

### 1. Research
Gather data on any topic.
```bash
python -m researcher_agent.src.cli "Quantum Computing Trends 2024" --limit 10
```

### 2. Analyze
Process the gathered data into structured insights.
```bash
python -m analyst_agent.src.cli researcher_agent/output/research_output_...json
```

### 3. Forecast
Generate predictions based on analysis.
```bash
python -m forecaster_agent.src.cli analyst_agent/output/analysis_output_...json
```

### 4. Report
Synthesize everything into a beautiful report.
```bash
python -m writer_agent.src.cli forecaster_agent/output/forecast_output_...json --format html
```

## 🏗️ Technical DNA
- **Core Orchestration**: `LangChain` & `CLI-first` design
- **Machine Learning**: `RandomForest`, `Prophet`, `XGBoost`
- **Natural Language**: `Transformer-based embeddings` (optional), `Rule-based NLP`
- **Visualization**: `Matplotlib` with custom styles

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/Piyush-Karn">Piyush Kumar</a>
  <br/>
  <i>Empowering decisions through autonomous intelligence.</i>
</p>
