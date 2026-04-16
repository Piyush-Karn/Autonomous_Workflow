# Researcher Agent — Deep Dive

The **Researcher Agent** is the entry point of the ecosystem. Its primary goal is to gather a critical mass of diverse articles and data points related to a specific query.

## 📂 Internal Structure

- `src/cli.py`: The command-line interface for manual runs.
- `src/search.py`: Handles the search engine interface (DuckDuckGo).
- `src/fetch.py`: Downloads raw HTML content from discovered URLs.
- `src/extract.py`: Cleans raw HTML into plain text, stripping boilerplate (ads, navbars).
- `src/orchestrate.py`: The high-level controller that manages the sequence of searching, fetching, and cleaning.

## ⚙️ How it Works

1.  **Search**: It uses `ddgs` (DuckDuckGo Search) to find the most relevant URLs. It filters for unique domains to ensure source diversity.
2.  **Concurrency**: It attempts to fetch multiple articles in batches to optimize speed.
3.  **Extraction**: It utilizes a cleaner logic to ensure the Analyst receives high-quality prose rather than messy HTML.
4.  **Data Schema**: The output is a `research_bundle.json` containing:
    *   `query`: The original search string.
    *   `articles`: A list of objects containing `title`, `url`, `source`, `published`, and `text`.

## 🛠️ Customization

You can adjust the `max_results` in `search.py` to increase the depth of the initial search. By default, it prioritizes `region="in-en"` for English-language news relevant to India, but this can be parameterized.
