# Free Books Scraper

A comprehensive Python tool for scraping free books from multiple platforms including archive.org and Project Gutenberg, optimized for Google Colab.

## Quick Start in Google Colab

```python
# One-click setup and run
!pip install requests beautifulsoup4 pandas
!python book_scraper.py
```

## Features

- 📚 **1000+ Free Books**: Scrape from archive.org, Project Gutenberg
- 📄 **PDF Downloads**: Automatic PDF book downloads
- 🖼️ **HD Covers**: High-quality cover image downloads
- 📊 **Complete Metadata**: Title, author, description, categories, ISBN
- 📦 **Organized Storage**: CSV database + zip archives
- 🔍 **Easy Access**: Simple functions to find and access books
- 🆓 **100% Free**: Only scrapes public domain and free books

## Files Overview

- `book_scraper.py` - Main scraping engine
- `book_utils.py` - Book management utilities
- `colab_demo.py` - Google Colab demo script
- `test_scraper.py` - Quick test script
- `README.md` - Complete documentation
- `requirements.txt` - Python dependencies

## Usage Examples

### Load and Search Books
```python
import pandas as pd
from book_utils import BookManager

# Load collection
manager = BookManager("/content/books")
df = manager.df

# Search books
python_books = manager.search_books('Python')
fiction_books = manager.get_books_by_category('Fiction')
popular_books = manager.get_most_popular(10)
```

### Access Book Files
```python
# Get first book
book = df.iloc[0]

# Access PDF
pdf_path = book['local_pdf_path']

# Access cover
cover_path = book['local_cover_path']
```

## Output Structure

```
/content/books/
├── books_database.csv       # Complete book database
├── free_books_collection.zip # All files zipped
├── pdfs/                    # Downloaded PDFs
├── covers/                  # HD cover images
└── metadata/                # Statistics and info
```

## CSV Database Columns

- `title`, `author`, `description`, `date`, `publisher`
- `language`, `categories`, `subjects`, `isbn`, `pages`
- `source`, `identifier`, `download_count`, `file_size`
- `pdf_url`, `cover_url`, `local_pdf_path`, `local_cover_path`
- `added_date`

## Platform Sources

1. **Archive.org** - 600+ books, high-quality scans
2. **Project Gutenberg** - 300+ books, public domain classics
3. **Extensible** - Easy to add more platforms

## Legal Notice

Only scrapes public domain and freely available books. Users must comply with copyright laws and platform terms of service.

## Requirements

- Python 3.7+
- requests, beautifulsoup4, pandas
- Google Colab or local environment

## Support

See README.md for detailed documentation and examples.