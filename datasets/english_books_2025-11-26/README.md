# English Books Snapshot — 26 Nov 2025

A dreamlike capsule of 250 English-language books, scraped directly from Archive.org with the polished `run_import.py` pipeline. Think of this folder as a pocket universe: every row in the CSV is a doorway, every JSON block a constellation map to a stranger library.

## Run configuration

- **Command:** `python3 run_import.py --target-books 250 --languages en --skip-downloads`
- **Languages:** English (`en`)
- **Downloads:** Disabled (metadata-only capture for fast iteration)
- **Output directory:** `books/`
- **Runtime:** 246 seconds (metadata only)
- **Sources:** Archive.org exclusively (250/250 titles)

## Snapshot contents

| File | Description |
| ---- | ----------- |
| `books_database.csv` | Full metadata for all 250 books (title, author, subjects, links, local placeholders). |
| `import_summary.json` | Execution summary: timestamps, counts, runtime, and switches used. |
| `scraping_statistics.json` | Aggregated stats for languages, sources, and the ten loudest categories. |

## Surreal reading itinerary

1. **Mirror Mazes** – 8 entries filed under the “mirror” tag invite you to reflect on literature that reflects back.
2. **Metaphysical Sheet Music** – 7 music-centric scores hum in the CSV; filter by `categories` containing `sheet music` and listen with your eyes.
3. **Dusty Dispatches** – Newspapers like *The Times* and *The Daily Telegraph* appear alongside occult grimoires; sort by `title` and alternate between fact and fable for a disorienting duet.
4. **Alchemy of Self-Help** – Blend Bruce Lee’s *Tao of Jeet Kune Do* with Seneca’s *On the Shortness of Life* and modern manifestos for a time-bending reading ritual.

Each stop above can be recreated by filtering the CSV with `pandas` or your favorite spreadsheet—mix the categories and you get a personalized surrealist syllabus.

## Snapshot metrics

- **Books scraped:** 250
- **Books with descriptions:** 197
- **Books with categories:** 193
- **PDFs/Covers downloaded:** 0 (by design)
- **Top category signals:** mirror (8), pdf.yt (8), sheet music (7), Banasthali (5), data.gov.in standards (4), folk poetry (4).

## Refreshing or extending

1. Activate the virtual environment (`source .venv/bin/activate`) or install `requirements.txt`.
2. Re-run `python3 run_import.py --target-books 250 --languages en --skip-downloads` for a fresh snapshot, or adjust the switches when you crave a longer trip (drop `--skip-downloads` for PDFs, change `--target-books`, or expand `--languages`).
3. Copy the regenerated CSV/JSON artifacts from `books/` into a new dated folder under `datasets/` to keep the historical timelines separate.

> **Note:** `books/` stays gitignored so heavy downloads never bloat the repo. The `datasets/` directory is the curated, human-friendly surface for sharing the voyage.
