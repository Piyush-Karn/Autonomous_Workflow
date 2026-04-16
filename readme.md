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

## 🚀 The Web Dashboard
The system now features a **Premium Web Interface** that allows you to run the entire pipeline with a single click. No more complex CLI commands—just enter your topic and watch the agents work in real-time.

**To Launch the Dashbord:**
```bash
python -m interface.server
```
Visit **[http://localhost:8000](http://localhost:8000)** to start your investigation.

## 🤖 The Agent Ecosystem

The project is built on a modular "Chain of Thought" architecture where specialized agents collaborate:

| Agent | Icon | Role | Key Technologies |
| :--- | :---: | :--- | :--- |
| **Researcher** | 🔍 | **Data Discovery**: Searches the web, scrapes articles, and extracts core content. | `DuckDuckGo`, `Newspaper3k`, `BeautifulSoup` |
| **Analyst** | 🧠 | **Semantic Intelligence**: Extracts patterns, calculates sentiment, and synthesizes executive highlights. | `SpaCy`, `NLTK`, `Scikit-learn`, `Sumy` |
| **Forecaster** | 📈 | **Predictive Modeling**: Projects future trends and identifies historical article volume trajectories. | `XGBoost`, `Prophet`, `LightGBM`, `Statsmodels` |
| **Writer** | ✍️ | **Professional Delivery**: Generates cinematic, pro-narrative reports in Markdown and HTML. | `Jinja2`, `Matplotlib`, `WeasyPrint` |

## 🔄 Workflow Architecture

```mermaid
graph LR
    User([User Prompt]) ---|Topic| Hub[<b>Web Dashboard</b>]
    Hub ---|Orchestrate| R[<b>Researcher</b>]
    R ---|Raw Articles| A[<b>Analyst</b>]
    A ---|Insights & Patterns| F[<b>Forecaster</b>]
    F ---|Predictions| W[<b>Writer</b>]
    W ---|Report| Output([Polished Report])

    style R fill:#1e293b,stroke:#3b82f6,color:#fff
    style A fill:#1e293b,stroke:#8b5cf6,color:#fff
    style F fill:#1e293b,stroke:#ec4899,color:#fff
    style W fill:#1e293b,stroke:#10b981,color:#fff
    style Hub fill:#0f172a,stroke:#f59e0b,color:#fff
    style User fill:#0f172a,stroke:#fff,color:#fff
    style Output fill:#0f172a,stroke:#fff,color:#fff
```

## ✨ Key Features
- **🚀 One-Touch Pipeline**: Go from a topic to a 10-page report with a single click.
- **📊 Real-time Monitoring**: Watch agent logs stream live to your browser via SSE.
- **🧠 Pattern Discovery**: Automatically finds "Strategic Linkages" and "Historical Trajectories".
- **🎨 Premium Visuals**: Modern Glassmorphism UI with cinematic responsive designs.
- **🛡️ Quality Assurance**: ASCII-only logs for 100% compatibility across Windows/Unix terminals.

## ⚙️ Installation

1. **Clone & Setup**:
   ```bash
   git clone <repo-url>
   cd Autonomous_Workflow
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. **Install All Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **NLP Resources**:
   ```bash
   python -m spacy download en_core_web_sm
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')"
   ```

## 🏗️ Technical DNA & Documentation
For a deep dive into each module, visit our **[Internal Documentation](documentation/index.md)**.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/Piyush-Karn">Piyush Kumar</a>
  <br/>
  <i>Empowering decisions through autonomous intelligence.</i>
</p>
