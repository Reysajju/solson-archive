#!/usr/bin/env python3
"""
Google Colab Demo - Free Books Scraper
Run this directly in Google Colab to scrape 1000+ free books
"""

# Step 1: Install required packages
print("📦 Installing required packages...")
!pip install requests beautifulsoup4 pandas --quiet

# Step 2: Import libraries
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Step 3: Download and run the main scraper
print("📚 Starting Free Books Scraper...")
print("This will scrape 1000+ free books from archive.org and Project Gutenberg")
print("⏰ This process may take 30-60 minutes depending on your connection")
print()

# Download the scraper script
!wget -q https://raw.githubusercontent.com/your-username/your-repo/main/book_scraper.py -O book_scraper.py

# Run the scraper
from book_scraper import BookScraper

# Initialize and run
scraper = BookScraper(download_dir="/content/books")

print("🎯 Target: 1000 books")
print("📂 Download location: /content/books/")
print()

# Run the full scraping process
try:
    books, csv_path, zip_path = scraper.run_full_scraping(target_books=1000)
    
    print("\n" + "="*60)
    print("🎉 SCRAPING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"📚 Total books scraped: {len(books)}")
    print(f"📊 Database saved to: {csv_path}")
    print(f"📦 Zip archive created: {zip_path}")
    
    # Show file sizes
    if os.path.exists(csv_path):
        csv_size = os.path.getsize(csv_path) / (1024*1024)  # MB
        print(f"📄 CSV file size: {csv_size:.2f} MB")
    
    if os.path.exists(zip_path):
        zip_size = os.path.getsize(zip_path) / (1024*1024)  # MB
        print(f"📦 Zip file size: {zip_size:.2f} MB")
    
    print("\n📖 How to use your collection:")
    print("1. Load the database:")
    print("   import pandas as pd")
    print(f"   df = pd.read_csv('{csv_path}')")
    print()
    print("2. Browse books:")
    print("   print(df[['title', 'author', 'categories']].head())")
    print()
    print("3. Find specific books:")
    print("   fiction = df[df['categories'].str.contains('Fiction', case=False)]")
    print()
    print("4. Access book files:")
    print("   pdf_path = df.iloc[0]['local_pdf_path']")
    print("   cover_path = df.iloc[0]['local_cover_path']")
    
    # Offer download
    print("\n💾 Download files from Colab:")
    print("1. Use the file browser on the left sidebar")
    print("2. Navigate to /content/books/")
    print("3. Right-click and download files")
    print("4. Or use:")
    print("   from google.colab import files")
    print(f"   files.download('{csv_path}')")
    print(f"   files.download('{zip_path}')")
    
except Exception as e:
    print(f"❌ Error during scraping: {e}")
    print("💡 Try running with a smaller target:")
    print("   books, csv_path, zip_path = scraper.run_full_scraping(target_books=100)")

print("\n✨ Done! Check your /content/books/ folder for the results!")