import pandas as pd
from . import loader, features, models, cv, config, utils
from .schema import ForecastResult, SeriesForecast

def _forecast_one_series(ts_df, target_col, frequency, horizon, model_name):
    df = ts_df.copy()

    if model_name in ("lightgbm", "xgboost"):
        df["article_count"] = df[target_col].astype(float)
        df = features.build_features(df)

        if model_name == "lightgbm":
            forecast_vals = models.lightgbm_forecast(df, horizon)
        else:
            forecast_vals = models.xgboost_forecast(df, horizon)
    else:
        y = df[target_col]
        if model_name == "naive":
            forecast_vals = models.naive_forecast(y, horizon)
        elif model_name == "snaive":
            forecast_vals = models.seasonal_naive_forecast(y, horizon, config.SEASONAL_PERIODS[frequency])
        elif model_name == "holtwinters":
            forecast_vals = models.holtwinters_forecast(y, horizon, config.SEASONAL_PERIODS[frequency])
        elif model_name == "arima":
            forecast_vals = models.arima_forecast(y, horizon)
        else:
            raise ValueError(f"Unknown model: {model_name}")

    forecast_dates = pd.date_range(
        df.index[-1] + pd.Timedelta(1, unit="D" if frequency == "daily" else "W"),
        periods=horizon,
        freq="D" if frequency == "daily" else "W"
    )
    return [{"date": d.strftime("%Y-%m-%d"), "prediction": float(v)} for d, v in zip(forecast_dates, forecast_vals)]


def run_forecast(input_path, frequency, horizon, model_name, top_k_keywords):
    ts_df = loader.load_analyst_json(input_path, frequency, top_k_keywords, include_sentiment=True)

    all_cols = list(ts_df.columns)
    main_target = "article_count"
    kw_targets = [c for c in all_cols if c.startswith("kw_") and c.endswith("_count")]

    # CV for main target
    ts_for_main = ts_df.copy()
    if model_name in ("lightgbm", "xgboost"):
        ts_for_main["article_count"] = ts_for_main[main_target].astype(float)
        ts_for_main = features.build_features(ts_for_main)
    y_main = ts_for_main["article_count"]

    if model_name == "naive":
        cv_metrics = cv.rolling_origin_cv(y_main, horizon, models.naive_forecast)
    elif model_name == "snaive":
        cv_metrics = cv.rolling_origin_cv(y_main, horizon, models.seasonal_naive_forecast,
                                          {"season_length": config.SEASONAL_PERIODS[frequency]})
    elif model_name == "holtwinters":
        cv_metrics = cv.rolling_origin_cv(y_main, horizon, models.holtwinters_forecast,
                                          {"seasonal_periods": config.SEASONAL_PERIODS[frequency]})
    elif model_name == "arima":
        cv_metrics = cv.rolling_origin_cv(y_main, horizon, models.arima_forecast)
    else:
        cv_metrics = {"smape": None, "rmse": None}

    out_series = []
    skipped_series = []

    # Lowered keyword threshold so more pass
    min_total_threshold = 2
    min_len_threshold = 12 if frequency == "weekly" else 28

    # Main series forecast
    out_series.append(
        SeriesForecast(
            series=main_target,
            confidence=_confidence_from_cv(cv_metrics),
            forecasts=_forecast_one_series(ts_df, main_target, frequency, horizon, model_name)
        )
    )

    # Keyword series forecasts
    for kw_col in kw_targets:
        history = ts_df[kw_col]
        total_count = history.sum()
        non_zero_count = (history > 0).sum()

        if total_count < min_total_threshold:
            skipped_series.append(kw_col)
            continue

        use_model = model_name
        if model_name in ("lightgbm", "xgboost") and (
            len(history) < min_len_threshold or non_zero_count <= 4
        ):
            use_model = "holtwinters"

        if len(history) >= min_len_threshold:
            series_cv = (
                cv.rolling_origin_cv(history, horizon, models.holtwinters_forecast)
                if use_model == "holtwinters"
                else {"smape": None, "rmse": None}
            )
        else:
            series_cv = {"smape": None, "rmse": None}

        out_series.append(
            SeriesForecast(
                series=kw_col,
                confidence=_confidence_from_cv(series_cv, fallback=(use_model != model_name)),
                forecasts=_forecast_one_series(ts_df, kw_col, frequency, horizon, use_model)
            )
        )

    return ForecastResult(
        meta={
            "model": model_name,
            "horizon": horizon,
            "frequency": frequency,
            "generated_at": utils.timestamp(),
            "series_count": len(out_series),
            "skipped_series": skipped_series
        },
        forecasts=out_series,
        cv_metrics=cv_metrics,
        top_features=[]
    )

def _confidence_from_cv(cv_metrics, fallback=False):
    if fallback:
        return "low"
    smape = cv_metrics.get("smape")
    if smape is None:
        return "medium"
    if smape > 60:
        return "low"
    elif smape > 30:
        return "medium"
    return "high"
