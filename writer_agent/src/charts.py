import matplotlib.pyplot as plt
from pathlib import Path


def plot_series(series_data, title, out_path):
    """
    Plot a simple line chart of forecast values and save as PNG.
    """
    dates = [p["date"] for p in series_data]
    vals = [p["prediction"] for p in series_data]

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 4))
    plt.plot(dates, vals, marker="o")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Predicted Value")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
