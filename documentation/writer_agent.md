# Writer Agent — Deep Dive

The **Writer Agent** is the final stage of the pipeline. It is responsible for formatting, visualization, and creating the "Understandable" output requested by users.

## 🎨 Visualization & Compilation

- **Jinja2 Templating**: Uses a sophisticated templating engine to generate Markdown or HTML reports. This allows for conditional formatting (e.g., hiding sections that have no data).
- **Pro Layouts**: The `report_pro.html.j2` template includes CSS for a cinematic, high-end look with "scroll-driven" aesthetics.
- **Chart Generation**: Integrates Python charting libraries to create visual visualizations of trends (saved in `output/charts/`).

## ⚙️ How it Works

1.  **Loader**: Reads JSON files from the Analyst, Forecaster, and (optional) Facts database.
2.  **Parser**: Normalizes the data into a single object (`data`) that the templates can easily access.
3.  **Generator**: Renders the templates into the final file format (.md or .html).

## 📄 Output Formats

1.  **Markdown (`.md`)**: Best for quick reading, Slack/Email sharing, and documentation.
2.  **HTML (`.html`)**: Best for deep presentations, featuring charts, professional typography, and responsive design.

## 📂 Internal Structure

- `src/cli.py`: Main CLI. Takes `--analyst`, `--weekly`, and `--out` paths.
- `src/parser.py`: Maps complex Analyst/Forecaster objects to template-friendly keys like `data.analysis.insights`.
- `src/generator.py`: Handles the actual Jinja2 rendering and file saving.
- `src/templates/`: Contains the `.j2` source files for the report designs.

## 🛠️ Customization

You can create new templates in the `src/templates/` folder. The parser is designed to be **topic-agnostic**, meaning it will work for any research query without core code changes.
