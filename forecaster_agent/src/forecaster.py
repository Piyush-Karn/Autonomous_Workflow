# forecaster.py
import pandas as pd
from . import loader, features, models, cv, config, utils
from .schema import ForecastResult

def run_forecast(input_path, frequency, horizon, model_name, top_k_keywords):
    ts_df = loader.load_analyst_json(input_path, frequency, top_k_keywords)

    if model_name in ("lightgbm", "xgboost"):
        ts_df = features.build_features(ts_df)
    
    # Cross-validation
    y = ts_df["article_count"]
    if model_name == "naive":
        cv_metrics = cv.rolling_origin_cv(y, horizon, models.naive_forecast)
        forecast_vals = models.naive_forecast(y, horizon)
    elif model_name == "snaive":
        cv_metrics = cv.rolling_origin_cv(y, horizon, models.seasonal_naive_forecast,
                                          {"season_length": config.SEASONAL_PERIODS[frequency]})
        forecast_vals = models.seasonal_naive_forecast(y, horizon, config.SEASONAL_PERIODS[frequency])
    elif model_name == "holtwinters":
        cv_metrics = cv.rolling_origin_cv(y, horizon, models.holtwinters_forecast,
                                          {"seasonal_periods": config.SEASONAL_PERIODS[frequency]})
        forecast_vals = models.holtwinters_forecast(y, horizon, config.SEASONAL_PERIODS[frequency])
    elif model_name == "arima":
        cv_metrics = cv.rolling_origin_cv(y, horizon, models.arima_forecast)
        forecast_vals = models.arima_forecast(y, horizon)
    elif model_name == "lightgbm":
        cv_metrics = {"mape": None, "rmse": None}  # Skip for initial example
        forecast_vals = models.lightgbm_forecast(ts_df, horizon)
    elif model_name == "xgboost":
        cv_metrics = {"mape": None, "rmse": None}
        forecast_vals = models.xgboost_forecast(ts_df, horizon)
    else:
        raise ValueError(f"Unknown model: {model_name}")

    forecast_dates = pd.date_range(ts_df.index[-1] + pd.Timedelta(1, unit="D" if frequency=="daily" else "W"),
                                   periods=horizon, freq="D" if frequency=="daily" else "W")
    forecasts = [{"date": d.strftime("%Y-%m-%d"), "prediction": float(v)} for d, v in zip(forecast_dates, forecast_vals)]

    return ForecastResult(
        meta={
            "model": model_name,
            "horizon": horizon,
            "frequency": frequency,
            "generated_at": utils.timestamp()
        },
        forecasts=forecasts,
        cv_metrics=cv_metrics,
        top_features=[]  # Feature importances for ML could be added here
    )
