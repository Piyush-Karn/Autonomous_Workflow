import pandas as pd

def build_features(ts_df, lags=(1, 2, 3, 4, 7, 14), rolling_windows=(3, 4, 7, 14, 28)):
    df = ts_df.copy()
    target_col = "article_count"

    # Defensive: ensure the target is 1D
    if not hasattr(df[target_col], "dtype"):
        df[target_col] = pd.Series(df[target_col]).astype(float)
    else:
        df[target_col] = df[target_col].astype(float)

    # Lag features
    for lag in lags:
        df[f"lag_{lag}"] = df[target_col].shift(lag)

    # Rolling stats
    for window in rolling_windows:
        df[f"roll_mean_{window}"] = df[target_col].shift(1).rolling(window=window).mean()
        df[f"roll_std_{window}"] = df[target_col].shift(1).rolling(window=window).std()

    # Calendar features
    df["dayofweek"] = df.index.dayofweek
    df["weekofyear"] = df.index.isocalendar().week.astype(int)
    df["month"] = df.index.month
    df["quarter"] = df.index.quarter

    return df
