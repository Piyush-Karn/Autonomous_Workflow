# config.py

# Default forecast settings
DEFAULT_HORIZON = 14            # number of periods ahead to forecast
DEFAULT_FREQUENCY = "daily"     # daily or weekly
DEFAULT_MODEL = "lightgbm"      # naive, snaive, holtwinters, arima, lightgbm, xgboost
DEFAULT_TOP_K_KEYWORDS = 0      # number of top keywords to include as exogenous features (0 disables)

# Seasonal periods for common frequencies
SEASONAL_PERIODS = {
    "daily": 7,   # weekly seasonality for daily data
    "weekly": 52  # yearly seasonality for weekly data
}

# Rolling-origin CV settings
CV_FOLDS = 5
MIN_TRAIN_SIZE = 30  # minimum observations in initial training window
