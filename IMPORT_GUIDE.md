# Book Import Guide - 1000+ Books Collection

## Overview

This repository contains a comprehensive book scraping and import system that collects **1000+ free books** from multiple sources, including:
- ✅ **PDF Books** - Full text PDFs
- ✅ **HD Book Covers** - High-quality cover images  
- ✅ **Metadata** - Complete bibliographic information
- ✅ **Descriptions** - Book summaries and abstracts
- ✅ **Categories** - Subject classifications and tags

## Quick Start - Running the Import

### Method 1: Using the Main Import Script

```bash
# Install dependencies
pip install --break-system-packages -q requests beautifulsoup4 pandas lxml

# Run the import (takes 30-60 minutes for 1000 books)
python3 run_import.py
```

### Method 2: Run in Background

```bash
# Run in background and save output
nohup python3 run_import.py > import.log 2>&1 &

# Check progress
tail -f import.log

# Or check status
tail -n 50 import.log
```

### Method 3: Using Google Colab

Upload `Free_Books_Scraper_Colab.ipynb` to Google Colab and run all cells.

## What Gets Imported

### Books Database Structure

The import creates a `books/` directory with the following structure:

```
books/
├── books_database.csv          # Complete database of all 1000+ books
├── free_books_collection.zip   # Zip archive of all files
├── import_summary.json         # Import statistics and summary
├── pdfs/                       # Downloaded PDF books
│   ├── Book_Title_1_identifier.pdf
│   ├── Book_Title_2_identifier.pdf
│   └── ... (1000+ PDFs)
├── covers/                     # HD book cover images
│   ├── Book_Title_1_identifier.jpg
│   ├── Book_Title_2_identifier.jpg
│   └── ... (1000+ covers)
└── metadata/                   # Additional metadata files
    └── scraping_statistics.json
```

### Metadata Fields

Each book entry contains the following fields:

| Field | Description | Example |
|-------|-------------|---------|
| `title` | Book title | "The Great Gatsby" |
| `author` | Author name(s) | "F. Scott Fitzgerald" |
| `description` | Book summary/abstract | "A classic American novel about..." |
| `categories` | Subject categories | "Fiction, Classic Literature, American" |
| `date` | Publication date | "1925" |
| `publisher` | Publisher name | "Scribner" |
| `language` | ISO language code | "en" |
| `subjects` | Subject tags | "Jazz Age, New York, Romance" |
| `isbn` | ISBN number | "978-0743273565" |
| `pages` | Number of pages | "180" |
| `source` | Source platform | "archive.org" or "gutenberg.org" |
| `identifier` | Unique ID | "greatgatsby00fitz" |
| `download_count` | Popularity metric | "15430" |
| `file_size` | PDF size in bytes | "2458624" |
| `pdf_url` | Original PDF URL | "https://archive.org/download/..." |
| `cover_url` | Original cover URL | "https://archive.org/download/..." |
| `local_pdf_path` | Local PDF path | "/home/engine/project/books/pdfs/..." |
| `local_cover_path` | Local cover path | "/home/engine/project/books/covers/..." |
| `added_date` | Import timestamp | "2025-11-25T08:38:27.123Z" |

## Data Sources

### Archive.org
- **Target**: 600-700 books
- **Quality**: High-quality scanned PDFs
- **Content**: Mix of classics, educational, and open-source books
- **Metadata**: Complete bibliographic information
- **Covers**: HD cover images available

### Project Gutenberg
- **Target**: 300-400 books
- **Quality**: Digitally created texts
- **Content**: Public domain classics
- **Metadata**: Standard bibliographic data
- **Covers**: Cover images when available

## Using the Imported Books

### Loading the Database

```python
import pandas as pd

# Load the complete books database
df = pd.read_csv('/home/engine/project/books/books_database.csv')

print(f"Total books: {len(df)}")
print(df.head())
```

### Searching Books

```python
# Search by title
python_books = df[df['title'].str.contains('Python', case=False, na=False)]

# Search by author
shakespeare = df[df['author'].str.contains('Shakespeare', case=False, na=False)]

# Filter by category
fiction = df[df['categories'].str.contains('Fiction', case=False, na=False)]

# Filter by language
english_books = df[df['language'] == 'en']

# Get most popular books
popular = df.nlargest(10, 'download_count')
```

### Accessing Files

```python
# Get first book
book = df.iloc[0]

# Access PDF
pdf_path = book['local_pdf_path']
print(f"PDF: {pdf_path}")

# Access cover
cover_path = book['local_cover_path']
print(f"Cover: {cover_path}")

# Display book info
print(f"Title: {book['title']}")
print(f"Author: {book['author']}")
print(f"Description: {book['description']}")
print(f"Categories: {book['categories']}")
```

## Import Statistics

After import completes, check `books/import_summary.json` for:

```json
{
  "import_timestamp": "2025-11-25T08:38:27.748Z",
  "target_books": 1000,
  "scraped_books": 1000,
  "books_with_pdfs": 1000,
  "books_with_covers": 850,
  "books_with_descriptions": 950,
  "books_with_categories": 980,
  "csv_database": "/home/engine/project/books/books_database.csv",
  "zip_archive": "/home/engine/project/books/free_books_collection.zip",
  "elapsed_seconds": 2100,
  "sources": {
    "archive_org": 700,
    "gutenberg_org": 300
  }
}
```

## Expected Results

### Metrics

- **Total Books**: 1000-1200 books
- **PDF Downloads**: 900-1000 PDFs (90%+ success rate)
- **Cover Images**: 700-900 covers (70-90% availability)
- **Metadata Completeness**: 95%+ of all fields
- **Categories**: 100+ unique categories
- **Languages**: Primarily English, some multilingual
- **Total Size**: 5-10 GB (depending on PDF sizes)
- **Processing Time**: 30-60 minutes

### Quality Metrics

- ✅ All books include title and author
- ✅ 95%+ include descriptions
- ✅ 98%+ include categories/subjects
- ✅ 90%+ have PDF files downloaded
- ✅ 70-90% have HD cover images
- ✅ All entries have unique identifiers
- ✅ All PDF and cover URLs are tracked

## Troubleshooting

### Import is Slow

The import process includes respectful delays to avoid overloading servers. Expected time is 30-60 minutes for 1000 books.

### Some Downloads Fail

This is normal - not all books have PDFs or covers available. The system tracks which files were successfully downloaded.

### Check Progress

```bash
# View recent progress
tail -n 50 /home/engine/project/final_import.log

# Or continuously monitor
tail -f /home/engine/project/final_import.log

# Check if process is running
ps aux | grep run_import
```

### Resume After Interruption

The scraper starts fresh each time. For incremental updates, modify the `run_import.py` script to check for existing files.

## Legal & Ethics

- ✅ **Public Domain**: Only public domain and freely available books
- ✅ **Terms of Service**: Complies with platform ToS
- ✅ **Rate Limiting**: Respectful delays between requests
- ✅ **Attribution**: Source tracking for all books
- ✅ **Legal Use**: Books are legally free to access and distribute

## Advanced Usage

### Custom Collections

```python
from book_utils import BookManager

manager = BookManager("/home/engine/project/books")

# Get fiction books
fiction = manager.get_books_by_category("Fiction")

# Create custom collection
manager.create_collection("my_fiction", fiction.head(50))

# Get statistics
manager.get_statistics()
```

### Batch Processing

```python
import pandas as pd

df = pd.read_csv('/home/engine/project/books/books_database.csv')

# Process all PDFs
for idx, book in df.iterrows():
    if book['local_pdf_path']:
        # Your PDF processing code here
        print(f"Processing: {book['title']}")
```

## Files in This Repository

- `book_scraper.py` - Main scraping engine
- `book_utils.py` - Utility functions for book management
- `run_import.py` - Import script (use this!)
- `requirements.txt` - Python dependencies
- `README.md` - Main documentation
- `IMPORT_GUIDE.md` - This guide
- `Free_Books_Scraper_Colab.ipynb` - Google Colab notebook
- `example_usage.py` - Usage examples

## Support

For issues or questions:
1. Check the logs: `tail -f final_import.log`
2. Review import summary: `cat books/import_summary.json`
3. Check statistics: `cat books/metadata/scraping_statistics.json`

---

**Happy Reading! 📚✨**

The import system ensures you have access to a comprehensive library of free books with complete metadata, PDFs, and HD covers!
