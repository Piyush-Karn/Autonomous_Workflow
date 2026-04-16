from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from . import charts

TEMPLATE_DIR = Path(__file__).parent / "templates"
CHART_DIR = Path(__file__).parent.parent / "output" / "charts"


def _ensure_dir(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)


def _render_charts(parsed_data, skip_charts=False):
    if skip_charts:
        return {"weekly_main": None, "weekly_keywords": [], "extras": {}}

    CHART_DIR.mkdir(parents=True, exist_ok=True)
    out = {"weekly_main": None, "weekly_keywords": [], "extras": {}}

    # Weekly main
    if parsed_data.get("weekly") and parsed_data["weekly"].get("main_series") and parsed_data["weekly"]["main_series"].get("forecasts"):
        p = CHART_DIR / "weekly_article_count.png"
        charts.plot_series(parsed_data["weekly"]["main_series"]["forecasts"], "Weekly Article Count (Forecast)", p)
        out["weekly_main"] = str(p)

    # Weekly keyword series
    if parsed_data.get("weekly") and parsed_data["weekly"].get("keyword_series"):
        for idx, kw in enumerate(parsed_data["weekly"]["keyword_series"][:8], start=1):
            if kw.get("forecasts"):
                safe = (kw.get("series") or f"kw_{idx}").replace("/", "_").replace("\\", "_")
                p = CHART_DIR / f"{safe}.png"
                charts.plot_series(kw["forecasts"], f"{safe} (Forecast)", p)
                out["weekly_keywords"].append({"series": kw.get("series"), "path": str(p)})

    # Facts-driven charts (if present in pro mode)
    pro = parsed_data.get("pro") or {}
    mkt = (pro.get("market_overview") or {}).get("market_size_series")
    if mkt:
        p = CHART_DIR / "market_size_trend.png"
        _plot_xy_series(mkt, "Market Size Trend", p)
        out["extras"]["market_size_trend"] = str(p)

    scams = (parsed_data.get("facts") or {}).get("scam_incidents")
    if scams:
        p = CHART_DIR / "scam_incidents_trend.png"
        _plot_xy_series(scams, "Scam Incidents Trend", p)
        out["extras"]["scam_incidents_trend"] = str(p)

    return out


def _plot_xy_series(series, title, out_path):
    # series as list of dicts with 'year' and 'value' or 'date' and 'value'
    import matplotlib.pyplot as plt
    from datetime import datetime

    xs, ys = [], []
    for row in series:
        x = row.get("year") or row.get("date")
        v = row.get("value", 0)
        if isinstance(x, int):
            xs.append(str(x))
        else:
            xs.append(str(x))
        ys.append(float(v))

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8.5, 4.2))
    plt.plot(xs, ys, marker="o", linewidth=2, color="#34d399")
    plt.title(title)
    plt.xlabel("Period")
    plt.ylabel("Value")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def generate_report(parsed_data, out_path: Path, skip_charts: bool = False):
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=select_autoescape())
    suffix = out_path.suffix.lower()
    _ensure_dir(out_path)

    chart_paths = _render_charts(parsed_data, skip_charts=skip_charts)
    data = dict(parsed_data)
    data["charts"] = chart_paths

    is_pro = (data.get("mode") == "pro")
    md_tpl = "report_pro.md.j2" if is_pro else "report_template.md.j2"
    html_tpl = "report_pro.html.j2" if is_pro else "report_template.html.j2"

    if suffix == ".md":
        tpl = env.get_template(md_tpl)
        out_path.write_text(tpl.render(data=data), encoding="utf-8")
        print(f"✅ Report saved: {out_path}")
        return

    if suffix == ".html":
        tpl = env.get_template(html_tpl)
        out_path.write_text(tpl.render(data=data), encoding="utf-8")
        print(f"✅ Report saved: {out_path}")
        return

    if suffix == ".pdf":
        try:
            from weasyprint import HTML
        except ImportError:
            raise RuntimeError("WeasyPrint missing. Use .html or install WeasyPrint + Cairo/GTK/Pango.")
        tpl = env.get_template(html_tpl)
        html = tpl.render(data=data)
        HTML(string=html, base_url=str(TEMPLATE_DIR.resolve())).write_pdf(str(out_path))
        print(f"✅ Report saved: {out_path}")
        return

    raise ValueError("Unsupported output format. Use .md, .html, or .pdf")
