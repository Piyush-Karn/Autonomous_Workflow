import asyncio
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebInterface")

app = FastAPI(title="Autonomous Workflow Hub")

# Ensure directories exist
BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = Path(__file__).parent / "static"
TEMPLATES_DIR = Path(__file__).parent / "templates"
OUTPUT_DIR = BASE_DIR / "output"

STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

async def run_command_stream(command: list, step_name: str) -> AsyncGenerator[str, None]:
    """Runs a command and yields its output for SSE."""
    yield f"data: {json.dumps({'type': 'status', 'step': step_name, 'message': f'Starting {step_name}...'})}\n\n"
    
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=str(BASE_DIR)
    )

    while True:
        try:
            line = await process.stdout.readline()
            if not line:
                break
            # Use 'replace' to prevent crashes on mixed-encoding output from Windows subprocesses
            text = line.decode(errors='replace').strip()
            if text:
                yield f"data: {json.dumps({'type': 'log', 'step': step_name, 'message': text})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'log', 'step': step_name, 'message': f'[Stream Error]: {str(e)}'})}\n\n"
            break

    await process.wait()
    if process.returncode == 0:
        yield f"data: {json.dumps({'type': 'status', 'step': step_name, 'message': f'✅ {step_name} completed.'})}\n\n"
    else:
        yield f"data: {json.dumps({'type': 'error', 'step': step_name, 'message': f'❌ {step_name} failed with code {process.returncode}'})}\n\n"

@app.get("/api/research")
async def stream_research(topic: str, limit: int = 10, skip_charts: bool = False, mode: str = "brief"):
    async def event_generator():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic.lower()])[:20]
        
        # Define file paths
        research_file = OUTPUT_DIR / f"raw_{safe_topic}_{timestamp}.json"
        analysis_file = OUTPUT_DIR / f"analysis_{safe_topic}_{timestamp}.json"
        forecast_file = OUTPUT_DIR / f"forecast_{safe_topic}_{timestamp}.json"
        report_file = OUTPUT_DIR / f"report_{safe_topic}_{timestamp}.md"

        python_exe = sys.executable

        # 1. Research Agent
        async for msg in run_command_stream(
            [python_exe, "-m", "researcher_agent.src.cli", topic, "--limit", str(limit), "--out", str(research_file)],
            "Researcher"
        ): yield msg

        if not research_file.exists(): return

        # 2. Analyst Agent
        async for msg in run_command_stream(
            [python_exe, "-m", "analyst_agent.src.analyze", "--input", str(research_file), "--output", str(analysis_file), "--topic", topic],
            "Analyst"
        ): yield msg

        if not analysis_file.exists(): return

        # 3. Forecaster Agent
        async for msg in run_command_stream(
            [python_exe, "-m", "forecaster_agent.src.cli", str(analysis_file), "--out", str(forecast_file)],
            "Forecaster"
        ): yield msg

        # 4. Writer Agent
        writer_cmd = [python_exe, "-m", "writer_agent.src.cli", "--analyst", str(analysis_file), "--out", str(report_file), "--mode", mode]
        if forecast_file.exists():
            writer_cmd.extend(["--daily", str(forecast_file)]) # Using daily as default for unified flow
        if skip_charts:
            writer_cmd.append("--skip-charts")

        async for msg in run_command_stream(writer_cmd, "Writer"): yield msg

        if report_file.exists():
            relative_report_path = f"/output/{report_file.name}"
            yield f"data: {json.dumps({'type': 'complete', 'report_url': relative_report_path})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Serve the output directory so users can download reports
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
