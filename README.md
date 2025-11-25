# Free Books Scraper - Google Colab Edition

A comprehensive Python script to scrape free books from multiple platforms including archive.org and Project Gutenberg. This tool downloads PDF files, HD covers, and complete metadata, organizing everything into structured CSV and zip archives.

## 🚀 Features

- **Multi-platform Scraping**: Archive.org, Project Gutenberg, and more
- **Complete Metadata**: Title, author, description, categories, ISBN, publisher, language
- **File Downloads**: PDF books and HD cover images
- **Organized Storage**: Structured directories and CSV database
- **1000+ Books**: Target collection of over 1000 free books
- **Google Colab Ready**: Optimized for Colab environment
- **Free & Legal**: Only scrapes public domain and freely available books

## 📋 Requirements

Install the required packages:

```python
!pip install requests beautifulsoup4 pandas
```

## 🛠️ Usage

### Basic Usage

```python
# Clone or upload the script to your Colab notebook
from book_scraper import BookScraper

# Initialize the scraper
scraper = BookScraper(download_dir="/content/books")

# Run full scraping process
books, csv_path, zip_path = scraper.run_full_scraping(target_books=1000)
```

### Quick Start in Google Colab

```python
# Install dependencies
!pip install requests beautifulsoup4 pandas

# Run the scraper
!python book_scraper.py
```

### Custom Scraping

```python
# Scrape from specific platforms only
archive_books = scraper.scrape_archive_org(max_books=500)
gutenberg_books = scraper.scrape_gutenberg(max_books=200)

# Download files for specific books
books_with_files = scraper.download_books(archive_books[:50])

# Save to custom CSV
scraper.save_to_csv(books_with_files, filename="my_collection.csv")

# Create custom zip
scraper.create_zip_archive(filename="my_books.zip")
```

## 📁 File Structure

After running, you'll get this structure:

```
/content/books/
├── pdfs/                    # Downloaded PDF books
│   ├── Book_Title_1.pdf
│   ├── Book_Title_2.pdf
│   └── ...
├── covers/                  # HD cover images
│   ├── Book_Title_1.jpg
│   ├── Book_Title_2.jpg
│   └── ...
├── metadata/                # Metadata and statistics
│   └── scraping_statistics.json
├── books_database.csv       # Complete book database
└── free_books_collection.zip # All files in one zip
```

## 📊 CSV Database Structure

The `books_database.csv` contains the following columns:

| Column | Description |
|--------|-------------|
| `title` | Book title |
| `author` | Author name |
| `description` | Book description/summary |
| `date` | Publication date |
| `publisher` | Publisher information |
| `language` | Book language (ISO code) |
| `subjects` | Subject tags |
| `categories` | Book categories |
| `isbn` | ISBN number (if available) |
| `pages` | Number of pages |
| `source` | Source platform (archive.org, gutenberg.org) |
| `identifier` | Unique identifier |
| `download_count` | Popularity/download count |
| `file_size` | File size in bytes |
| `pdf_url` | Original PDF URL |
| `cover_url` | Original cover URL |
| `local_pdf_path` | Local PDF file path |
| `local_cover_path` | Local cover file path |
| `added_date` | When book was added to collection |

## 🔍 Accessing Books from CSV

### Loading the Database

```python
import pandas as pd

# Load the CSV
df = pd.read_csv('/content/books/books_database.csv')

print(f"Total books: {len(df)}")
print(df.head())
```

### Finding Specific Books

```python
# Search by title
python_books = df[df['title'].str.contains('Python', case=False)]

# Filter by author
shakespeare_books = df[df['author'].str.contains('Shakespeare', case=False)]

# Filter by category
fiction_books = df[df['categories'].str.contains('Fiction', case=False)]

# Filter by language
english_books = df[df['language'] == 'en']

# Most popular books
popular_books = df.nlargest(10, 'download_count')
```

### Accessing Book Files

```python
# Get first book
first_book = df.iloc[0]

# Access PDF file
pdf_path = first_book['local_pdf_path']
if pdf_path:
    print(f"PDF location: {pdf_path}")
    # You can now open, read, or process the PDF

# Access cover image
cover_path = first_book['local_cover_path']
if cover_path:
    print(f"Cover location: {cover_path}")
    # You can display or process the cover image
```

### Displaying Book Information

```python
def display_book_info(book_index):
    """Display detailed information about a specific book"""
    book = df.iloc[book_index]
    
    print(f"📚 {book['title']}")
    print(f"✍️  Author: {book['author']}")
    print(f"📅 Year: {book['date']}")
    print(f"🏢 Publisher: {book['publisher']}")
    print(f"🌐 Language: {book['language']}")
    print(f"📖 Categories: {book['categories']}")
    print(f"📄 Pages: {book['pages']}")
    print(f"📊 Downloads: {book['download_count']}")
    print(f"🔗 Source: {book['source']}")
    
    if book['description']:
        print(f"\n📝 Description:\n{book['description'][:500]}...")
    
    print(f"\n📁 PDF: {book['local_pdf_path']}")
    print(f"🖼️  Cover: {book['local_cover_path']}")

# Display info for book at index 0
display_book_info(0)
```

### Creating Custom Collections

```python
# Create a collection of classic literature
classics = df[df['categories'].str.contains('Classic|Literature', case=False)]

# Save custom collection
classics.to_csv('/content/books/classic_literature.csv', index=False)

# Create a collection of science books
science_books = df[df['categories'].str.contains('Science|Mathematics|Physics', case=False)]
science_books.to_csv('/content/books/science_collection.csv', index=False)
```

## 🎯 Advanced Usage

### Batch Processing

```python
def process_books_by_category(category_name):
    """Process all books in a specific category"""
    category_books = df[df['categories'].str.contains(category_name, case=False)]
    
    print(f"Found {len(category_books)} books in '{category_name}'")
    
    for idx, book in category_books.iterrows():
        print(f"Processing: {book['title']}")
        
        # Access PDF
        if book['local_pdf_path']:
            # Add your PDF processing logic here
            pass
        
        # Access cover
        if book['local_cover_path']:
            # Add your image processing logic here
            pass

# Process all fiction books
process_books_by_category('Fiction')
```

### Statistics and Analysis

```python
# Collection statistics
print(f"Total books: {len(df)}")
print(f"Books with PDFs: {len(df[df['local_pdf_path'] != ''])}")
print(f"Books with covers: {len(df[df['local_cover_path'] != ''])}")

# Top categories
categories = df['categories'].str.split(', ').explode().value_counts().head(10)
print("\nTop 10 Categories:")
print(categories)

# Language distribution
languages = df['language'].value_counts()
print("\nLanguage Distribution:")
print(languages)

# Publication decade analysis
df['decade'] = (df['date'].str.extract(r'(\d{4})').astype(float) // 10 * 10).astype(int)
decades = df['decade'].value_counts().sort_index()
print("\nBooks by Decade:")
print(decades)
```

## 📦 Download and Extract

### From Google Colab

```python
# Download individual files
from google.colab import files

# Download CSV
files.download('/content/books/books_database.csv')

# Download zip archive
files.download('/content/books/free_books_collection.zip')
```

### Manual Download

1. Go to the Colab file browser (left sidebar)
2. Navigate to `/content/books/`
3. Right-click on files and select "Download"

## 🔄 Extracting and Using the Zip Archive

```python
import zipfile
import os

# Extract the zip archive
with zipfile.ZipFile('/content/books/free_books_collection.zip', 'r') as zip_ref:
    zip_ref.extractall('/content/extracted_books/')

# The extracted structure will be:
# /content/extracted_books/
# ├── pdfs/
# ├── covers/
# └── books_database.csv
```

## 📚 Sources and Platforms

### Archive.org
- **Collection**: Open source texts, public domain books
- **Format**: PDF, EPUB, and more
- **Quality**: High-quality scans and OCR
- **Metadata**: Complete bibliographic information

### Project Gutenberg
- **Collection**: Public domain classics
- **Format**: PDF, EPUB, plain text
- **Quality**: Digitally created texts
- **Metadata**: Standard bibliographic data

## ⚠️ Important Notes

1. **Legal Compliance**: Only scrapes public domain and freely available books
2. **Rate Limiting**: Built-in delays to respect server resources
3. **Storage Space**: 1000+ books may require significant storage (5-10GB)
4. **Processing Time**: Full scraping may take 30-60 minutes
5. **Network**: Stable internet connection required

## 🛠️ Troubleshooting

### Common Issues

```python
# If downloads fail, try reducing the target number
books, csv_path, zip_path = scraper.run_full_scraping(target_books=100)

# If specific books fail, check the logs
import logging
logging.basicConfig(level=logging.DEBUG)

# If storage is full, clean up
!rm -rf /content/books/
# Then restart with smaller target
```

### Memory Issues

```python
# Process books in batches
batch_size = 100
for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    # Process batch
    print(f"Processing batch {i//batch_size + 1}")
```

## 📄 License

This script is provided for educational and research purposes. Users are responsible for ensuring compliance with copyright laws and terms of service of the source platforms.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the scraper.

---

**Happy Reading! 📚✨**