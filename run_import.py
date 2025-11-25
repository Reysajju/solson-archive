#!/usr/bin/env python3
"""Helper script to import 1000+ books with PDFs, HD covers, metadata, and categories."""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from book_scraper import BookScraper
import logging

LOG_FILE = 'book_import.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape free books and build the dataset")
    parser.add_argument(
        "--target-books",
        type=int,
        default=1000,
        help="Total number of books to scrape (default: 1000)",
    )
    parser.add_argument(
        "--languages",
        type=str,
        default="",
        help="Comma-separated list of allowed language codes (e.g., en,fr). Leave empty for all languages.",
    )
    parser.add_argument(
        "--skip-downloads",
        action="store_true",
        help="Skip downloading PDFs and covers to collect metadata only.",
    )
    parser.add_argument(
        "--download-dir",
        type=str,
        default=str(Path("/home/engine/project/books")),
        help="Directory to store downloaded files and metadata.",
    )
    return parser.parse_args()


def main() -> bool:
    args = parse_args()
    target_books = args.target_books
    logger.info("=" * 70)
    logger.info("STARTING BOOK IMPORT - TARGET: %s BOOKS", target_books)
    logger.info("=" * 70)

    download_dir = Path(args.download_dir).expanduser().resolve()
    download_dir.mkdir(parents=True, exist_ok=True)

    language_filter = [lang.strip() for lang in args.languages.split(',') if lang.strip()]
    if not language_filter:
        language_filter = None

    scraper = BookScraper(download_dir=str(download_dir), language_filter=language_filter)
    download_files = not args.skip_downloads

    logger.info("Download directory: %s", download_dir)
    logger.info("Target books: %s", target_books)
    if language_filter:
        logger.info("Language filter: %s", ", ".join(language_filter))
    else:
        logger.info("Language filter: all languages")
    logger.info("Download files: %s", "yes" if download_files else "no (metadata only)")

    start_time = time.time()
    logger.info("Running full scraping pipeline...")
    logger.info("This will download metadata, PDFs, HD covers, CSV, and ZIP archive")

    try:
        books, csv_path, zip_path = scraper.run_full_scraping(
            target_books=target_books,
            download_files=download_files
        )

        elapsed = time.time() - start_time
        books_with_pdfs = len([b for b in books if b.get('local_pdf_path')])
        books_with_covers = len([b for b in books if b.get('local_cover_path')])
        books_with_desc = len([b for b in books if b.get('description')])
        books_with_cats = len([b for b in books if b.get('categories')])

        logger.info("=" * 70)
        logger.info("IMPORT COMPLETE!")
        logger.info("=" * 70)
        logger.info(f"Total books imported: {len(books)}")
        logger.info(f"Books with PDFs: {books_with_pdfs}")
        logger.info(f"Books with covers: {books_with_covers}")
        logger.info(f"Books with descriptions: {books_with_desc}")
        logger.info(f"Books with categories: {books_with_cats}")
        logger.info(f"CSV database: {csv_path}")
        logger.info(f"Zip archive: {zip_path}")
        logger.info(f"Elapsed time: {int(elapsed)} seconds")
        logger.info("=" * 70)

        summary = {
            "import_timestamp": datetime.utcnow().isoformat() + "Z",
            "target_books": target_books,
            "scraped_books": len(books),
            "books_with_pdfs": books_with_pdfs,
            "books_with_covers": books_with_covers,
            "books_with_descriptions": books_with_desc,
            "books_with_categories": books_with_cats,
            "csv_database": str(csv_path),
            "zip_archive": str(zip_path),
            "elapsed_seconds": int(elapsed),
            "language_filter": language_filter or ["all"],
            "download_files": download_files,
            "sources": {
                "archive_org": len([b for b in books if b.get('source') == 'archive.org']),
                "gutenberg_org": len([b for b in books if b.get('source') == 'gutenberg.org'])
            }
        }

        summary_path = download_dir / "import_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        logger.info(f"Summary saved to {summary_path}")
        return True

    except Exception as exc:
        logger.exception("Import failed: %s", exc)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
