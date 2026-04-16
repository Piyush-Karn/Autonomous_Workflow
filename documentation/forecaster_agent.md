# Forecaster Agent — Deep Dive

The **Forecaster Agent** adds a predictive dimension to the research. It helps stakeholders understand if interest in a topic is growing, shrinking, or seasonal.

## 📈 Key Capabilities

- **Weekly/Daily Forecasting**: Generates projections for article volume (proxy for "Public/Media Interest").
- **Seasonality Detection**: Identifies repeating patterns (e.g., weekend lulls or monthly spikes).
- **Keyword Trajectory**: Tracks how specific themes (like "Battery Safety") are trending relative to the main topic.

## ⚙️ How it Works

1.  **Time Series Construction**: Aggregates Analyst data into a time-indexed series based on publication dates.
2.  **Modeling**:
    *   **Prophet**: Used for its ability to handle holidays and strong seasonal effects.
    *   **LightGBM**: Occasionally used for more complex, feature-rich forecasting.
3.  **Confidence Scoring**: Assigns a confidence level to each forecast based on data volatility and model fit.

## 🛠️ Graceful Fallback

In cases where historical data is too sparse for deep time-series modeling, the system uses a **Historical Trajectory Emulation**. This calculates a linear slope of recent articles to provide a "Steady", "Upward", or "Downward" status even without complex models.

## 📂 Internal Structure

- `src/forecast.py`: Main entry point for forecasting runs.
- `src/models/`: Contains the specific model wrappers for Prophet and other regressors.
