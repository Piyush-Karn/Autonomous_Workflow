# cv.py
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

def rolling_origin_cv(y, horizon, model_fn, model_params=None, folds=5, min_train_size=30):
    """
    Perform rolling-origin cross-validation for a time series.
    model_fn: callable(train_y, test_horizon, **params) -> preds
    """
    metrics = []
    n = len(y)
    test_size = horizon
    model_params = model_params or {}

    for fold_start in range(min_train_size, n - test_size, test_size):
        train_y = y[:fold_start]
        true_y = y[fold_start: fold_start + test_size]
        preds = model_fn(train_y, test_size, **model_params)
        mape = mean_absolute_percentage_error(true_y, preds)
        rmse = mean_squared_error(true_y, preds, squared=False)
        metrics.append((mape, rmse))

    if not metrics:
        return {"mape": np.nan, "rmse": np.nan}

    mape_avg = np.mean([m for m, _ in metrics]) * 100
    rmse_avg = np.mean([r for _, r in metrics])
    return {"mape": mape_avg, "rmse": rmse_avg}
