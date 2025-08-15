import numpy as np
from sklearn.metrics import mean_squared_error

def rolling_origin_cv(y, horizon, model_fn, model_params=None, folds=5, min_train_size=10):
    model_params = model_params or {}
    n = len(y)
    if n <= min_train_size or n <= horizon:
        return {"smape": None, "rmse": None}

    metrics = []
    for fold_start in range(min_train_size, n - horizon + 1, horizon):
        train_y = y[:fold_start]
        true_y = y[fold_start: fold_start + horizon]
        if len(true_y) == 0:
            continue
        preds = model_fn(train_y, horizon, **model_params)
        rmse_val = float(np.sqrt(mean_squared_error(true_y, preds)))
        smape_val = _smape(true_y, preds)
        metrics.append((smape_val, rmse_val))

    if not metrics:
        return {"smape": None, "rmse": None}

    smape_avg = float(np.mean([m for m, _ in metrics]))
    rmse_avg = float(np.mean([r for _, r in metrics]))
    return {"smape": smape_avg, "rmse": rmse_avg}

def _smape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    denom = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    denom[denom == 0] = 1e-8
    return float(np.mean(np.abs(y_true - y_pred) / denom) * 100)
