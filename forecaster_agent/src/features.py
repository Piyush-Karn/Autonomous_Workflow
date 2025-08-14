# features.py
import pandas as pd

def build_features(ts_df, lags=(1,7,14), rolling_windows=(7,14,28)):
    """
    Given a time series dataframe with 'article_count' and possibly exogenous features,
    create lag and rolling-window features for ML models.
    """
    df = ts_df.copy()
    target_col = "article_count"
    for lag in lags:
        df[f"lag_{lag}"] = df[target_col].shift(lag)

    for window in rolling_windows:
        df[f"roll_mean_{window}"] = df[target_col].shift(1).rolling(window=window).mean()
        df[f"roll_std_{window}"] = df[target_col].shift(1).rolling(window=window).std()

    # Calendar features
    df["dayofweek"] = df.index.dayofweek
    df["month"] = df.index.month

    return df
