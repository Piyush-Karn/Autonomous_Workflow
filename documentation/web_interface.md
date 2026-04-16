# Web Interface & Orchestration Hub

The **Web Interface** is a modern, unified entry point for the Autonomous Workflow ecosystem. It replaces manual CLI multi-step execution with a sleek, interactive dashboard that manages the entire agent pipeline from a single button click.

## 🏗️ Architecture

The interface is built with a decoupled architecture to ensure the agents remain modular and testable as standalone components.

### 1. FastAPI Backend (`interface/server.py`)
The backend acts as a **Thin Orchestrator**. 
- It wraps the agent CLI entry points (`python -m agent.cli ...`).
- It uses **Server-Sent Events (SSE)** to stream real-time logs from the subprocesses directly to the UI.
- It maps the output of each agent as the input for the next, managing the file dependencies automatically.

### 2. Glassmorphism Frontend
The UI uses modern web design principles to provide a premium feel:
- **Style**: Dark mode with translucent glassmorphism panels.
- **Interactivity**: Real-time log scrolling with automatic auto-scroll logic.
- **Responsiveness**: Fluid layout that works across different screen sizes.

## 🚀 Key Features

### Pro & Brief Modes
The interface allows you to toggle between **Standard Research** and **Pro Narrative**.
- **Brief**: Fast synthesis focusing on core data.
- **Pro**: Deep-dive analysis including expanded "Key Findings", "Topic Domains", and "Strategic Entity Correlation".

### Live Pipeline Monitoring
The dashboard displays a live feed of exactly what each agent is doing:
- `Researcher`: URLs being scraped and search volume.
- `Analyst`: Cluster IDs and sentiment scores.
- `Forecaster`: Confidence levels and trend slopes.
- `Writer`: Template rendering and final file paths.

## ⚙️ How to Run

1.  **Launch the Server**:
    ```bash
    python -m interface.server
    ```
2.  **Access the Dashboard**:
    Open [http://localhost:8000](http://localhost:8000).
3.  **Start Investigation**:
    - Enter a topic (e.g., "Future of EVs in 2026").
    - Select your search limit.
    - Click **Launch Investigation**.

## 🛠️ Windows Compatibility Note
The interface is optimized for Windows terminals. All subprocess logs have been stripped of non-ASCII emojis to prevent `UnicodeEncodeError` crashes, while the UI still uses high-quality icons for visual flair.

---
*Documentation for the Orchestration Hub.*
