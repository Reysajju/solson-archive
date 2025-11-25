# Quick Start Guide - Import 1000+ Books

## Overview

This repository provides a complete system to import **1000+ free books** from Archive.org and Project Gutenberg, including:

- ✅ PDF books (full text)
- ✅ HD book covers (high-quality images)
- ✅ Complete metadata (title, author, description, categories, ISBN, publisher, language, etc.)
- ✅ CSV database (searchable and filterable)
- ✅ Zip archive (all files packaged)

## One-Command Import

```bash
python3 run_import.py
```

That's it! The script will:
1. Scrape 1000+ books from Archive.org and Project Gutenberg
2. Download PDF files for all available books
3. Download HD cover images
4. Extract complete metadata (title, author, description, categories, etc.)
5. Create CSV database with all information
6. Generate zip archive with all files
7. Produce comprehensive statistics

## Expected Runtime

- **30-60 minutes** for 1000+ books (depending on network speed)
- Respectful rate limiting is built in to avoid overloading servers

## Output Structure

After completion, you'll have:

```
books/
├── books_database.csv           # Complete database (1000+ books)
├── free_books_collection.zip    # All files zipped
├── import_summary.json          # Import statistics
├── pdfs/                        # PDF books
│   ├── Book_1.pdf
│   ├── Book_2.pdf
│   └── ... (900-1000 PDFs)
├── covers/                      # HD covers
│   ├── Book_1.jpg
│   ├── Book_2.jpg
│   └── ... (700-850 covers)
└── metadata/
    └── scraping_statistics.json
```

## Using the Imported Books

### Load the Database

```python
import pandas as pd

# Load all books
df = pd.read_csv('books/books_database.csv')

print(f"Total books: {len(df)}")
print(df.head())
```

### Search and Filter

```python
# Search by title
python_books = df[df['title'].str.contains('Python', case=False, na=False)]

# Filter by author
shakespeare = df[df['author'].str.contains('Shakespeare', case=False, na=False)]

# Filter by category
fiction = df[df['categories'].str.contains('Fiction', case=False, na=False)]

# Most popular books
popular = df.nlargest(10, 'download_count')
```

### Access Book Files

```python
# Get a specific book
book = df.iloc[0]

# Print book information
print(f"Title: {book['title']}")
print(f"Author: {book['author']}")
print(f"Description: {book['description']}")
print(f"Categories: {book['categories']}")
print(f"PDF: {book['local_pdf_path']}")
print(f"Cover: {book['local_cover_path']}")
```

## Database Fields

Each book record contains:

- **title** - Book title
- **author** - Author name(s)
- **description** - Book summary/abstract
- **categories** - Subject classifications (e.g., "Fiction, Classic Literature")
- **date** - Publication date
- **publisher** - Publisher name
- **language** - Language code (e.g., "en" for English)
- **subjects** - Subject tags
- **isbn** - ISBN number (when available)
- **pages** - Number of pages
- **source** - Source platform (archive.org or gutenberg.org)
- **identifier** - Unique book ID
- **download_count** - Popularity/download count
- **file_size** - PDF file size in bytes
- **pdf_url** - Original PDF URL
- **cover_url** - Original cover URL
- **local_pdf_path** - Path to downloaded PDF
- **local_cover_path** - Path to downloaded cover
- **added_date** - When book was imported

## Example Use Cases

### Create a Fiction Collection

```python
import pandas as pd

df = pd.read_csv('books/books_database.csv')
fiction = df[df['categories'].str.contains('Fiction', case=False, na=False)]
fiction.to_csv('fiction_books.csv', index=False)
print(f"Saved {len(fiction)} fiction books")
```

### Find Books by Language

```python
df = pd.read_csv('books/books_database.csv')
english_books = df[df['language'] == 'en']
spanish_books = df[df['language'] == 'es']
```

### Get Collection Statistics

```python
df = pd.read_csv('books/books_database.csv')

print(f"Total books: {len(df)}")
print(f"Books with PDFs: {len(df[df['local_pdf_path'] != ''])}")
print(f"Books with covers: {len(df[df['local_cover_path'] != ''])}")

# Category distribution
categories = df['categories'].str.split(', ').explode().value_counts().head(10)
print("\nTop 10 Categories:")
print(categories)
```

## Advanced Features

### Using the BookManager Utility

```python
from book_utils import BookManager

# Initialize manager
manager = BookManager("/home/engine/project/books")

# Search books
python_books = manager.search_books('Python', 'title')
fiction_books = manager.get_books_by_category('Fiction')

# Get most popular
popular = manager.get_most_popular(10)

# Get statistics
manager.get_statistics()

# Create custom collection
classics = manager.search_books('Classic', 'categories')
manager.create_collection("classics", classics.head(50))
```

## Troubleshooting

### Check Import Progress

```bash
# View log file
tail -f book_import.log

# Check last 50 lines
tail -n 50 book_import.log
```

### Verify System

```bash
# Check dependencies
python3 -c "import requests, bs4, pandas; print('✓ Dependencies OK')"

# Test with 10 books
python3 -c "from book_scraper import BookScraper; s = BookScraper('./test'); books, csv, zip = s.run_full_scraping(10); print(f'✓ Imported {len(books)} books')"
```

### Import is Slow

This is normal! The system includes respectful delays to avoid overloading servers.
- Metadata collection: ~1-2 books/second
- PDF downloads: Varies by file size
- Total time: 30-60 minutes for 1000 books

## File Locations

- **Import Script**: `run_import.py` (run this!)
- **Core Engine**: `book_scraper.py`
- **Utilities**: `book_utils.py`
- **Output Directory**: `books/`
- **CSV Database**: `books/books_database.csv`
- **Zip Archive**: `books/free_books_collection.zip`

## Requirements

```
requests>=2.31.0
beautifulsoup4>=4.12.0
pandas>=2.0.0
lxml>=4.9.0
```

Install with:
```bash
pip install --break-system-packages requests beautifulsoup4 pandas lxml
```

## Legal Notice

All books imported are:
- ✅ Public domain or freely available
- ✅ Legally distributable
- ✅ Scraped with respectful rate limiting
- ✅ Properly attributed to sources

## Summary

**To import 1000+ books with PDFs, HD covers, and complete metadata:**

```bash
# Single command
python3 run_import.py

# Wait 30-60 minutes

# Access the data
python3 -c "import pandas as pd; df = pd.read_csv('books/books_database.csv'); print(f'Imported {len(df)} books')"
```

That's it! The system handles everything automatically.

---

For more details, see:
- **README.md** - Full documentation
- **IMPORT_GUIDE.md** - Detailed import guide
- **STATUS.md** - System status and verification
- **PROJECT_SUMMARY.md** - Project overview
