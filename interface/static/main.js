const runBtn = document.getElementById('run-btn');
const topicInput = document.getElementById('topic-input');
const logOutput = document.getElementById('log-output');
const statusContainer = document.getElementById('status-container');
const resultContainer = document.getElementById('result-container');
const downloadLink = document.getElementById('download-link');
const resetBtn = document.getElementById('reset-btn');

let eventSource = null;

runBtn.addEventListener('click', startResearch);
resetBtn.addEventListener('click', () => location.reload());

topicInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startResearch();
});

function startResearch() {
    const topic = topicInput.value.trim();
    if (!topic) {
        alert("Please enter a research topic first.");
        return;
    }

    const limit = document.getElementById('limit').value;
    const mode = document.getElementById('mode').value;
    const skipCharts = document.getElementById('skip-charts').checked;

    // UI Reset
    runBtn.disabled = true;
    runBtn.innerText = "Investigating...";
    statusContainer.style.display = 'block';
    resultContainer.style.display = 'none';
    logOutput.innerHTML = '<div class="log-line">--- Initializing Pipeline ---</div>';
    
    // Reset Stepper
    document.querySelectorAll('.step').forEach(s => s.classList.remove('active', 'complete'));

    // Start SSE
    const url = `/api/research?topic=${encodeURIComponent(topic)}&limit=${limit}&mode=${mode}&skip_charts=${skipCharts}`;
    eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch(data.type) {
            case 'log':
                appendLog(data.message);
                break;
            case 'status':
                appendLog(`[${data.step}] ${data.message}`, 'status');
                updateStepper(data.step, 'active');
                break;
            case 'error':
                appendLog(data.message, 'error');
                eventSource.close();
                runBtn.disabled = false;
                runBtn.innerText = "Retry Investigation";
                break;
            case 'complete':
                handleCompletion(data.report_url);
                break;
        }
    };

    eventSource.onerror = () => {
        appendLog("System Connection Lost. The process might still be running locally.", "error");
        eventSource.close();
        runBtn.disabled = false;
    };
}

function appendLog(msg, type = '') {
    const div = document.createElement('div');
    div.className = `log-line ${type}`;
    div.innerText = msg;
    logOutput.appendChild(div);
    logOutput.scrollTop = logOutput.scrollHeight;
}

function updateStepper(stepName, state) {
    const stepEl = document.getElementById(`step-${stepName}`);
    if (!stepEl) return;

    if (state === 'active') {
        // Mark previous steps as complete
        let found = false;
        document.querySelectorAll('.step').forEach(s => {
            if (s === stepEl) {
                found = true;
                s.classList.add('active');
                s.classList.remove('complete');
            } else if (!found) {
                s.classList.add('complete');
                s.classList.remove('active');
            }
        });
    }
}

function handleCompletion(url) {
    eventSource.close();
    
    // Mark all steps complete
    document.querySelectorAll('.step').forEach(s => {
        s.classList.add('complete');
        s.classList.remove('active');
    });

    appendLog("Investigation finalized. Generating report links...", "status");
    
    resultContainer.style.display = 'block';
    downloadLink.href = url;
    
    runBtn.disabled = false;
    runBtn.innerText = "Investigation Complete";
}
