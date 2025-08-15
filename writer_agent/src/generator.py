from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import markdown

TEMPLATE_DIR = Path(__file__).parent / "templates"


def generate_report(parsed_data, out_path: Path, skip_charts: bool = False):
    """
    Render a report based on parsed forecast data.
    Supports .md, .html, .pdf (PDF requires WeasyPrint and system libs).
    """
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape()
    )

    suffix = out_path.suffix.lower()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if suffix == ".md":
        template = env.get_template("report_template.md.j2")
        rendered = template.render(data=parsed_data)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"✅ Report saved to {out_path}")
        return

    if suffix == ".html":
        template = env.get_template("report_template.html.j2")
        rendered = template.render(data=parsed_data)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"✅ Report saved to {out_path}")
        return

    if suffix == ".pdf":
        # Lazy import only for PDF, to avoid Windows system lib issues when not needed
        try:
            from weasyprint import HTML
        except ImportError:
            raise RuntimeError(
                "WeasyPrint not installed. Install with: pip install weasyprint\n"
                "On Windows, also install GTK/Pango/Cairo per: "
                "https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation"
            )
        template = env.get_template("report_template.html.j2")
        rendered = template.render(data=parsed_data)
        HTML(string=rendered).write_pdf(str(out_path))
        print(f"✅ Report saved to {out_path}")
        return

    raise ValueError("Unsupported output format. Use .md, .html, or .pdf")
