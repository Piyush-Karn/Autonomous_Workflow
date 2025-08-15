import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import lightgbm as lgb
import xgboost as xgb

def naive_forecast(train_y, horizon):
    return np.repeat(train_y.iloc[-1], horizon)

def seasonal_naive_forecast(train_y, horizon, season_length=7):
    reps = int(np.ceil(horizon / season_length))
    season = train_y.iloc[-season_length:]
    return np.tile(season.values, reps)[:horizon]

def holtwinters_forecast(train_y, horizon, seasonal_periods=7):
    """Fallback to non-seasonal if data too short for full seasonal cycles."""
    if len(train_y) < 2 * seasonal_periods:
        model = ExponentialSmoothing(train_y, trend="add", seasonal=None)
    else:
        model = ExponentialSmoothing(train_y, seasonal="add", trend="add", seasonal_periods=seasonal_periods)
    fit = model.fit(optimized=True)
    return fit.forecast(horizon)

def arima_forecast(train_y, horizon):
    try:
        import pmdarima as pm
    except ImportError as e:
        raise RuntimeError("pmdarima is not installed. Install with: pip install pmdarima") from e
    model = pm.auto_arima(train_y, seasonal=False, stepwise=True, suppress_warnings=True)
    return model.predict(horizon)

def lightgbm_forecast(train_df, horizon):
    df = train_df.copy().dropna()
    if len(df) < 5:
        return [df["article_count"].iloc[-1]] * horizon  # fallback if too short

    y = df["article_count"]
    X = df.drop(columns=["article_count"])

    model = lgb.LGBMRegressor(
        objective="regression",
        learning_rate=0.1,
        num_leaves=15,
        max_depth=3,
        min_data_in_leaf=1,
        min_data_in_bin=1,
        n_estimators=200
    )
    model.fit(X, y)

    preds = []
    last_df = df.iloc[-1:].copy()

    for _ in range(horizon):
        pred = model.predict(last_df.drop(columns=["article_count"]))[0]
        preds.append(float(pred))
        # Update for autoregressive loop
        last_df = last_df.copy()
        last_df["lag_1"] = pred
        for lag in [2, 3, 4, 7, 14]:
            if f"lag_{lag}" in last_df.columns:
                last_df[f"lag_{lag}"] = last_df.get(f"lag_{lag-1}", pred)
        # Rolling update is skipped in minimal example
    return preds

def xgboost_forecast(train_df, horizon):
    df = train_df.copy().dropna()
    if len(df) < 5:
        return [df["article_count"].iloc[-1]] * horizon
    y = df["article_count"]
    X = df.drop(columns=["article_count"])
    model = xgb.XGBRegressor(
        objective="reg:squarederror", learning_rate=0.1, max_depth=3, n_estimators=200
    )
    model.fit(X, y)
    preds = []
    last_df = df.iloc[-1:].copy()

    for _ in range(horizon):
        pred = model.predict(last_df.drop(columns=["article_count"]))[0]
        preds.append(float(pred))
        last_df["lag_1"] = pred
    return preds
