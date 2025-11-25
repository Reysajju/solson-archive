#!/usr/bin/env python3
"""
Free Books Scraper for Google Colab
Scrapes free books from multiple platforms including archive.org
Downloads PDF files, HD covers, and metadata
Saves data as CSV and organized zip files
"""

import os
import re
import csv
import json
import time
import zipfile
import requests
import pandas as pd
from pathlib import Path
from urllib.parse import urljoin, urlparse
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
import logging

# For web scraping
from bs4 import BeautifulSoup
import requests

# For archive.org API
import urllib.parse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BookScraper:
    def __init__(self, download_dir: str = "/content/books"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.pdf_dir = self.download_dir / "pdfs"
        self.covers_dir = self.download_dir / "covers"
        self.metadata_dir = self.download_dir / "metadata"
        
        for dir_path in [self.pdf_dir, self.covers_dir, self.metadata_dir]:
            dir_path.mkdir(exist_ok=True)
        
        self.books_data = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def download_file(self, url: str, destination: Path, timeout: int = 30) -> bool:
        """Download a file from URL to destination path"""
        try:
            response = self.session.get(url, stream=True, timeout=timeout)
            response.raise_for_status()
            
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Downloaded: {destination.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to download {url}: {e}")
            return False
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file system usage"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Replace spaces with underscores
        filename = re.sub(r'\s+', '_', filename)
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        return filename
    
    def scrape_archive_org(self, max_books: int = 500, existing_ids: Optional[Set[str]] = None) -> List[Dict]:
        """Scrape free books from archive.org while avoiding duplicate identifiers"""
        logger.info(f"Scraping archive.org for {max_books} books...")
        
        books: List[Dict] = []
        page = 1
        seen_ids: Set[str] = set()
        
        # Search for free PDF books
        search_url = "https://archive.org/advancedsearch.php"
        
        while len(books) < max_books:
            try:
                params = {
                    'q': 'collection:(opensource) OR mediatype:(texts) AND format:(pdf)',
                    'fl[]': ['identifier', 'title', 'description', 'creator', 'date', 'subject', 'download_count'],
                    'sort[]': 'downloads desc',
                    'rows': '100',
                    'page': str(page),
                    'output': 'json',
                    'save': 'yes'
                }
                
                response = self.session.get(search_url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if 'response' not in data or not data['response']['docs']:
                    break
                
                for doc in data['response']['docs']:
                    if len(books) >= max_books:
                        break
                    
                    identifier = doc.get('identifier', '')
                    if not identifier:
                        continue
                    
                    if identifier in seen_ids:
                        continue
                    
                    if existing_ids and identifier in existing_ids:
                        continue
                    
                    # Get detailed metadata
                    book_data = self.get_archive_org_book_details(identifier)
                    if book_data:
                        books.append(book_data)
                        seen_ids.add(identifier)
                        logger.info(f"Scraped {len(books)}/{max_books}: {book_data.get('title', 'Unknown')}")
                
                page += 1
                time.sleep(0.2)  # Reduced delay for faster scraping
                
            except Exception as e:
                logger.error(f"Error scraping archive.org page {page}: {e}")
                break
        
        return books
    
    def get_archive_org_book_details(self, identifier: str) -> Optional[Dict]:
        """Get detailed book information from archive.org"""
        try:
            # Get metadata
            metadata_url = f"https://archive.org/metadata/{identifier}"
            response = self.session.get(metadata_url, timeout=30)
            response.raise_for_status()
            
            metadata = response.json()
            
            if metadata.get('metadata', {}).get('title') is None:
                return None
            
            # Extract book data
            book_data = {
                'source': 'archive.org',
                'identifier': identifier,
                'title': metadata['metadata'].get('title', ''),
                'author': metadata['metadata'].get('creator', [''])[0] if metadata['metadata'].get('creator') else '',
                'description': metadata['metadata'].get('description', ''),
                'date': metadata['metadata'].get('date', ''),
                'publisher': metadata['metadata'].get('publisher', ''),
                'language': metadata['metadata'].get('language', 'en')[0] if metadata['metadata'].get('language') else 'en',
                'subjects': ', '.join(metadata['metadata'].get('subject', [])),
                'download_count': metadata.get('metadata', {}).get('download_count', 0),
                'file_size': 0,
                'pdf_url': '',
                'cover_url': '',
                'local_pdf_path': '',
                'local_cover_path': '',
                'categories': '',
                'isbn': metadata['metadata'].get('identifier-isbn', [''])[0] if metadata['metadata'].get('identifier-isbn') else '',
                'pages': metadata['metadata'].get('pages', ''),
                'added_date': datetime.now().isoformat()
            }
            
            # Find PDF and cover URLs
            files = metadata.get('files', [])
            pdf_url = None
            cover_url = None
            
            for file_info in files:
                name = file_info.get('name', '').lower()
                
                # Find PDF file (prefer main PDF)
                if name.endswith('.pdf') and not pdf_url:
                    if 'full text' in name or 'text' in name or not any(x in name for x in ['cover', 'thumb']):
                        pdf_url = f"https://archive.org/download/{identifier}/{file_info['name']}"
                        book_data['file_size'] = file_info.get('size', 0)
                
                # Find cover image
                if cover_url is None and ('cover' in name or 'thumb' in name) and name.endswith(('.jpg', '.jpeg', '.png')):
                    cover_url = f"https://archive.org/download/{identifier}/{file_info['name']}"
            
            book_data['pdf_url'] = pdf_url or ''
            book_data['cover_url'] = cover_url or ''
            
            # Categorize based on subjects
            subjects = metadata['metadata'].get('subject', [])
            if subjects:
                categories = []
                for subject in subjects[:5]:  # Limit to first 5 subjects
                    if isinstance(subject, str):
                        categories.append(subject)
                book_data['categories'] = ', '.join(categories)
            
            return book_data
            
        except Exception as e:
            logger.error(f"Error getting details for {identifier}: {e}")
            return None
    
    def scrape_gutenberg(self, max_books: int = 200) -> List[Dict]:
        """Scrape free books from Project Gutenberg"""
        logger.info(f"Scraping Project Gutenberg for {max_books} books...")
        
        books = []
        
        # Use Gutenberg's RSS feeds to find popular books
        rss_url = "https://www.gutenberg.org/cache/epub/feeds/today.rss"
        
        try:
            response = self.session.get(rss_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')[:max_books]
            
            for item in items:
                try:
                    title = item.find('title').text if item.find('title') else ''
                    link = item.find('link').text if item.find('link') else ''
                    
                    if not link:
                        continue
                    
                    # Extract book ID from link
                    book_id = link.split('/')[-1] if link.split('/')[-1].isdigit() else ''
                    if not book_id:
                        continue
                    
                    book_data = self.get_gutenberg_book_details(book_id)
                    if book_data:
                        books.append(book_data)
                        logger.info(f"Scraped Gutenberg {len(books)}/{max_books}: {title}")
                
                except Exception as e:
                    logger.error(f"Error processing Gutenberg item: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error scraping Gutenberg: {e}")
        
        return books
    
    def get_gutenberg_book_details(self, book_id: str) -> Optional[Dict]:
        """Get detailed book information from Project Gutenberg"""
        try:
            # Get book metadata
            metadata_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.rdf"
            response = self.session.get(metadata_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'xml')
            
            # Extract metadata
            title = soup.find('dcterms:title')
            author = soup.find('dcterms:creator')
            description = soup.find('dcterms:description')
            language = soup.find('dcterms:language')
            publisher = soup.find('dcterms:publisher')
            subject = soup.find_all('dcterms:subject')
            
            book_data = {
                'source': 'gutenberg.org',
                'identifier': book_id,
                'title': title.text.strip() if title else '',
                'author': author.text.strip() if author else '',
                'description': description.text.strip() if description else '',
                'date': '',
                'publisher': publisher.text.strip() if publisher else 'Project Gutenberg',
                'language': language.text.strip() if language else 'en',
                'subjects': ', '.join([s.text.strip() for s in subject if s.text.strip()]),
                'download_count': 0,
                'file_size': 0,
                'pdf_url': '',
                'cover_url': '',
                'local_pdf_path': '',
                'local_cover_path': '',
                'categories': '',
                'isbn': '',
                'pages': '',
                'added_date': datetime.now().isoformat()
            }
            
            # Try to find PDF download link
            pdf_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-pdf.pdf"
            try:
                test_response = self.session.head(pdf_url, timeout=10)
                if test_response.status_code == 200:
                    book_data['pdf_url'] = pdf_url
            except:
                pass
            
            # Try to find cover (book cover is not always available)
            cover_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.cover.medium.jpg"
            try:
                test_response = self.session.head(cover_url, timeout=10)
                if test_response.status_code == 200:
                    book_data['cover_url'] = cover_url
            except:
                pass
            
            # Set categories from subjects
            if subject:
                categories = [s.text.strip() for s in subject[:5] if s.text.strip()]
                book_data['categories'] = ', '.join(categories)
            
            return book_data
            
        except Exception as e:
            logger.error(f"Error getting Gutenberg details for {book_id}: {e}")
            return None
    
    def download_books(self, books: List[Dict], download_pdf: bool = True, download_covers: bool = True) -> List[Dict]:
        """Download PDF files and covers for books"""
        logger.info(f"Starting downloads for {len(books)} books...")
        
        for i, book in enumerate(books):
            try:
                title_safe = self.sanitize_filename(book.get('title', f'book_{i}'))
                
                # Download PDF
                if download_pdf and book.get('pdf_url'):
                    pdf_filename = f"{title_safe}_{book['identifier']}.pdf"
                    pdf_path = self.pdf_dir / pdf_filename
                    
                    if not pdf_path.exists():
                        if self.download_file(book['pdf_url'], pdf_path):
                            book['local_pdf_path'] = str(pdf_path)
                            logger.info(f"Downloaded PDF {i+1}/{len(books)}: {title_safe}")
                        else:
                            book['local_pdf_path'] = ''
                    else:
                        book['local_pdf_path'] = str(pdf_path)
                
                # Download Cover
                if download_covers and book.get('cover_url'):
                    cover_ext = '.jpg'
                    if book['cover_url'].lower().endswith('.png'):
                        cover_ext = '.png'
                    elif book['cover_url'].lower().endswith('.jpeg'):
                        cover_ext = '.jpeg'
                    
                    cover_filename = f"{title_safe}_{book['identifier']}{cover_ext}"
                    cover_path = self.covers_dir / cover_filename
                    
                    if not cover_path.exists():
                        if self.download_file(book['cover_url'], cover_path):
                            book['local_cover_path'] = str(cover_path)
                            logger.info(f"Downloaded cover {i+1}/{len(books)}: {title_safe}")
                        else:
                            book['local_cover_path'] = ''
                    else:
                        book['local_cover_path'] = str(cover_path)
                
                # Add delay to be respectful
                time.sleep(0.1)  # Reduced delay
                
            except Exception as e:
                logger.error(f"Error downloading files for book {i}: {e}")
                continue
        
        return books
    
    def save_to_csv(self, books: List[Dict], filename: str = "books_database.csv"):
        """Save books data to CSV file"""
        csv_path = self.download_dir / filename
        
        if not books:
            logger.warning("No books data to save")
            return
        
        # Define CSV columns
        columns = [
            'title', 'author', 'description', 'date', 'publisher', 'language',
            'subjects', 'categories', 'isbn', 'pages', 'source', 'identifier',
            'download_count', 'file_size', 'pdf_url', 'cover_url',
            'local_pdf_path', 'local_cover_path', 'added_date'
        ]
        
        # Filter books to only include those with data
        valid_books = [book for book in books if book.get('title')]
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(valid_books)
        
        # Reorder columns and fill missing values
        df = df.reindex(columns=columns, fill_value='')
        
        df.to_csv(csv_path, index=False, encoding='utf-8')
        logger.info(f"Saved {len(valid_books)} books to {csv_path}")
        
        return csv_path
    
    def create_zip_archive(self, filename: str = "free_books_collection.zip"):
        """Create a zip archive with all books and covers"""
        zip_path = self.download_dir / filename
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add PDFs
            for pdf_file in self.pdf_dir.glob("*.pdf"):
                zipf.write(pdf_file, f"pdfs/{pdf_file.name}")
            
            # Add covers
            for cover_file in self.covers_dir.glob("*"):
                if cover_file.is_file():
                    zipf.write(cover_file, f"covers/{cover_file.name}")
            
            # Add CSV if it exists
            csv_file = self.download_dir / "books_database.csv"
            if csv_file.exists():
                zipf.write(csv_file, "books_database.csv")
        
        logger.info(f"Created zip archive: {zip_path}")
        return zip_path
    
    def run_full_scraping(self, target_books: int = 1000, download_files: bool = True):
        """Run complete scraping process and ensure we reach the requested target"""
        logger.info(f"Starting full scraping process for {target_books} books...")
        
        all_books: List[Dict] = []
        seen_ids: Set[str] = set()
        
        def add_books(source_name: str, books: List[Dict]) -> int:
            added = 0
            for book in books:
                identifier = book.get('identifier')
                if not identifier or identifier in seen_ids:
                    continue
                seen_ids.add(identifier)
                all_books.append(book)
                added += 1
            logger.info(f"{source_name}: added {added} new books (total: {len(all_books)})")
            return added
        
        # First pass: archive.org (roughly half of the target, but at least 500)
        primary_archive_target = min(max(target_books // 2, 500), target_books)
        archive_books = self.scrape_archive_org(primary_archive_target, existing_ids=seen_ids)
        add_books("archive.org", archive_books)
        
        # Second pass: Project Gutenberg for the remaining books
        if len(all_books) < target_books:
            remaining = target_books - len(all_books)
            gutenberg_books = self.scrape_gutenberg(remaining)
            add_books("gutenberg.org", gutenberg_books)
        
        # Final top-up from archive.org if needed
        if len(all_books) < target_books:
            remaining = target_books - len(all_books)
            if remaining > 0:
                logger.info(f"Need {remaining} more books; continuing archive.org scraping...")
                extra_archive = self.scrape_archive_org(remaining, existing_ids=seen_ids)
                add_books("archive.org (top-up)", extra_archive)
        
        logger.info(f"Total books scraped: {len(all_books)}")
        
        # Download files
        if download_files:
            all_books = self.download_books(all_books)
        
        # Save to CSV
        csv_path = self.save_to_csv(all_books)
        
        # Create zip archive
        zip_path = self.create_zip_archive()
        
        # Generate statistics
        self.generate_statistics(all_books)
        
        return all_books, csv_path, zip_path
    
    def generate_statistics(self, books: List[Dict]):
        """Generate and display statistics about the scraped books"""
        logger.info("Generating statistics...")
        
        total_books = len(books)
        books_with_pdf = len([b for b in books if b.get('local_pdf_path')])
        books_with_covers = len([b for b in books if b.get('local_cover_path')])
        
        sources = {}
        languages = {}
        categories = {}
        
        for book in books:
            # Count by source
            source = book.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
            
            # Count by language
            lang = book.get('language', 'unknown')
            languages[lang] = languages.get(lang, 0) + 1
            
            # Count categories
            cats = book.get('categories', '').split(', ')
            for cat in cats[:3]:  # Limit to first 3 categories per book
                cat = cat.strip()
                if cat:
                    categories[cat] = categories.get(cat, 0) + 1
        
        stats = {
            'total_books': total_books,
            'books_with_pdf': books_with_pdf,
            'books_with_covers': books_with_covers,
            'sources': sources,
            'languages': languages,
            'top_categories': dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10])
        }
        
        # Save statistics
        stats_path = self.metadata_dir / "scraping_statistics.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\n" + "="*50)
        print("SCRAPING STATISTICS")
        print("="*50)
        print(f"Total books scraped: {total_books}")
        print(f"Books with PDFs downloaded: {books_with_pdf}")
        print(f"Books with covers downloaded: {books_with_covers}")
        print(f"\nSources:")
        for source, count in sources.items():
            print(f"  {source}: {count} books")
        
        print(f"\nLanguages:")
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {lang}: {count} books")
        
        print(f"\nTop Categories:")
        for cat, count in stats['top_categories'].items():
            print(f"  {cat}: {count} books")
        
        print("="*50)

def main():
    """Main function to run the scraper"""
    print("📚 Free Books Scraper for Google Colab")
    print("=" * 50)
    
    # Initialize scraper
    scraper = BookScraper()
    
    # Run scraping (you can adjust the target number)
    target_books = 1000
    books, csv_path, zip_path = scraper.run_full_scraping(target_books=target_books)
    
    print(f"\n✅ Scraping completed!")
    print(f"📊 CSV file: {csv_path}")
    print(f"📦 Zip archive: {zip_path}")
    print(f"📚 Total books: {len(books)}")
    
    # Show how to access books from CSV
    print(f"\n📖 How to access books:")
    print(f"1. Load the CSV: df = pd.read_csv('{csv_path}')")
    print(f"2. Filter books: fiction_books = df[df['categories'].str.contains('Fiction', case=False)]")
    print(f"3. Access PDF: pdf_path = df.iloc[0]['local_pdf_path']")
    print(f"4. Access cover: cover_path = df.iloc[0]['local_cover_path']")

if __name__ == "__main__":
    main()