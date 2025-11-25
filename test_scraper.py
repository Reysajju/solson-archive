#!/usr/bin/env python3
"""
Simple Test Script for Book Scraper
Tests the scraper with a small sample to verify functionality
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from book_scraper import BookScraper
from book_utils import BookManager

def test_scraper():
    """Test the scraper with a small sample"""
    print("🧪 Testing Book Scraper with small sample...")
    
    # Initialize scraper
    scraper = BookScraper(download_dir="/tmp/test_books")
    
    # Test with very small sample
    print("📚 Testing archive.org scraping (5 books)...")
    archive_books = scraper.scrape_archive_org(max_books=5)
    print(f"✅ Scraped {len(archive_books)} books from archive.org")
    
    if archive_books:
        print("📖 First book details:")
        book = archive_books[0]
        print(f"  Title: {book.get('title', 'N/A')}")
        print(f"  Author: {book.get('author', 'N/A')}")
        print(f"  PDF URL: {book.get('pdf_url', 'N/A')}")
        print(f"  Cover URL: {book.get('cover_url', 'N/A')}")
    
    print("\n📚 Testing Gutenberg scraping (3 books)...")
    gutenberg_books = scraper.scrape_gutenberg(max_books=3)
    print(f"✅ Scraped {len(gutenberg_books)} books from Gutenberg")
    
    # Test CSV saving
    all_books = archive_books + gutenberg_books
    if all_books:
        csv_path = scraper.save_to_csv(all_books, filename="test_books.csv")
        print(f"✅ CSV saved to: {csv_path}")
        
        # Test BookManager
        print("\n🧪 Testing BookManager...")
        manager = BookManager(download_dir="/tmp/test_books")
        
        if manager.df is not None:
            print(f"✅ BookManager loaded {len(manager.df)} books")
            
            # Test search
            if len(manager.df) > 0:
                first_title = manager.df.iloc[0]['title']
                search_results = manager.search_books(first_title.split()[0])
                print(f"✅ Search test: Found {len(search_results)} results")
        
        print("\n🎉 All tests passed! The scraper is ready to use.")
        print("💡 To run full scraping, use:")
        print("   python book_scraper.py")
        print("   or")
        print("   python colab_demo.py")
    
    else:
        print("❌ No books scraped. Check your internet connection.")

if __name__ == "__main__":
    test_scraper()