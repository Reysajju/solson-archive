# English Books Snapshot — 25 Nov 2025

This folder contains the English-only metadata snapshot generated directly from `run_import.py`. The scrape was executed inside the repository workspace so the resulting CSV/JSON artifacts can live inside version control without needing to redownload everything.

## Run configuration

- **Command:** `python3 run_import.py --target-books 1000 --languages en --skip-downloads`
- **Languages:** English (`en`)
- **Downloads:** Skipped (metadata-only capture)
- **Output directory:** `books/`
- **Run timestamp (UTC):** TBD

## Snapshot contents

| File | Description |
| ---- | ----------- |
| `books_database.csv` | Metadata for every scraped title. |
| `import_summary.json` | High-level run summary (targets, counts, elapsed time). |
| `scraping_statistics.json` | Language/source/category distribution stats. |

## Key metrics

- **Books scraped:** TBD
- **Books with PDFs downloaded:** 0 (downloads disabled)
- **Books with covers downloaded:** 0 (downloads disabled)
- **Sources:** TBD

## Refreshing the dataset

1. Activate the virtual environment (or install `requirements.txt`).
2. Run the command shown above. You can optionally change `--target-books`, `--languages`, or drop `--skip-downloads` if you want the PDFs/covers.
3. Copy the resulting CSV/JSON artifacts from `books/` into a dated folder under `datasets/`.

> **Note:** The `books/` directory remains gitignored so large binary assets do not enter the repository. Only the curated snapshot in this folder is tracked.
