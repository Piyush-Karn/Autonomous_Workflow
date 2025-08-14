# models.py
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
# REMOVE top-level: import pmdarima as pm
from sklearn.ensemble import GradientBoostingRegressor
import lightgbm as lgb
import xgboost as xgb

def naive_forecast(train_y, horizon):
    return np.repeat(train_y.iloc[-1], horizon)

def seasonal_naive_forecast(train_y, horizon, season_length=7):
    reps = int(np.ceil(horizon / season_length))
    season = train_y.iloc[-season_length:]
    return np.tile(season.values, reps)[:horizon]

def holtwinters_forecast(train_y, horizon, seasonal_periods=7):
    model = ExponentialSmoothing(train_y, seasonal="add", trend="add", seasonal_periods=seasonal_periods)
    fit = model.fit(optimized=True)
    return fit.forecast(horizon)

def arima_forecast(train_y, horizon):
    try:
        import pmdarima as pm
    except Exception as e:
        raise RuntimeError(
            "ARIMA is unavailable due to pmdarima not being installed or incompatible. "
            "Run: pip install --upgrade pip setuptools wheel && "
            "pip install --upgrade numpy && pip install --force-reinstall --no-cache-dir pmdarima"
        ) from e
    model = pm.auto_arima(train_y, seasonal=False, stepwise=True, suppress_warnings=True)
    return model.predict(horizon)

def lightgbm_forecast(train_df, horizon):
    df = train_df.copy().dropna()
    y = df["article_count"]
    X = df.drop(columns=["article_count"])
    model = lgb.LGBMRegressor()
    model.fit(X, y)
    preds = []
    last_df = df.iloc[-1:].copy()
    for _ in range(horizon):
        pred = model.predict(last_df.drop(columns=["article_count"]))[0]
        preds.append(pred)
        # Minimal autoregressive update
        last_df["lag_1"] = pred
    return preds

def xgboost_forecast(train_df, horizon):
    df = train_df.copy().dropna()
    y = df["article_count"]
    X = df.drop(columns=["article_count"])
    model = xgb.XGBRegressor()
    model.fit(X, y)
    preds = []
    last_df = df.iloc[-1:].copy()
    for _ in range(horizon):
        pred = model.predict(last_df.drop(columns=["article_count"]))[0]
        preds.append(pred)
        last_df["lag_1"] = pred
    return preds
