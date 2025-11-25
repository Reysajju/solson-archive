#!/usr/bin/env python3
"""Helper script to import 1000+ books with PDFs, HD covers, metadata, and categories."""

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


def main() -> bool:
    logger.info("=" * 70)
    logger.info("STARTING BOOK IMPORT - TARGET: 1000+ BOOKS")
    logger.info("=" * 70)

    download_dir = Path("/home/engine/project/books")
    download_dir.mkdir(exist_ok=True)

    scraper = BookScraper(download_dir=str(download_dir))
    target_books = 1000

    start_time = time.time()
    logger.info("Running full scraping pipeline...")
    logger.info("This will download metadata, PDFs, HD covers, CSV, and ZIP archive")

    try:
        books, csv_path, zip_path = scraper.run_full_scraping(
            target_books=target_books,
            download_files=True
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
