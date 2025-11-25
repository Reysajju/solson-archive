#!/usr/bin/env python3
"""
Example Usage of Scraped Books Collection
Demonstrates various ways to access and use the scraped books
"""

import pandas as pd
import os
from pathlib import Path
from book_utils import BookManager

def demonstrate_usage():
    """Demonstrate various ways to use the scraped books collection"""
    
    print("📚 Free Books Collection - Usage Examples")
    print("=" * 50)
    
    # Load the book manager
    manager = BookManager("/content/books")
    
    if manager.df is None:
        print("❌ No books database found!")
        print("Please run the scraper first:")
        print("python book_scraper.py")
        return
    
    df = manager.df
    print(f"✅ Loaded {len(df)} books from database")
    
    # Example 1: Display basic information
    print("\n📊 Example 1: Collection Overview")
    print("-" * 30)
    print(f"Total books: {len(df)}")
    print(f"Books with PDFs: {len(df[df['local_pdf_path'] != ''])}")
    print(f"Books with covers: {len(df[df['local_cover_path'] != ''])}")
    print(f"Languages: {df['language'].nunique()}")
    print(f"Sources: {', '.join(df['source'].unique())}")
    
    # Example 2: Show sample books
    print("\n📖 Example 2: Sample Books")
    print("-" * 30)
    sample_books = df[['title', 'author', 'categories']].head(5)
    for idx, book in sample_books.iterrows():
        print(f"{idx+1}. {book['title']} by {book['author']}")
        print(f"   📂 {book['categories']}")
    
    # Example 3: Search by title
    print("\n🔍 Example 3: Search for 'Python' books")
    print("-" * 30)
    python_books = manager.search_books('Python')
    print(f"Found {len(python_books)} Python books:")
    for idx, book in python_books.head(3).iterrows():
        print(f"📕 {book['title']}")
        print(f"   ✍️  {book['author']}")
        print(f"   📄 PDF: {os.path.basename(book['local_pdf_path']) if book['local_pdf_path'] else 'Not available'}")
    
    # Example 4: Browse by category
    print("\n🏷️  Example 4: Fiction Books")
    print("-" * 30)
    fiction_books = manager.get_books_by_category('Fiction')
    print(f"Found {len(fiction_books)} fiction books")
    if len(fiction_books) > 0:
        print("Sample fiction books:")
        for idx, book in fiction_books.head(3).iterrows():
            print(f"📚 {book['title']} ({book['date']})")
    
    # Example 5: Most popular books
    print("\n⭐ Example 5: Most Popular Books")
    print("-" * 30)
    popular_books = manager.get_most_popular(5)
    for idx, book in popular_books.iterrows():
        print(f"🏆 {book['title']}")
        print(f"   📊 Downloads: {book['download_count']:,}")
        print(f"   📖 {book['author']}")
    
    # Example 6: Books by language
    print("\n🌐 Example 6: Books by Language")
    print("-" * 30)
    lang_counts = df['language'].value_counts()
    for lang, count in lang_counts.head(5).items():
        print(f"{lang}: {count} books")
    
    # Example 7: Create custom collection
    print("\n📁 Example 7: Create Custom Collection")
    print("-" * 30)
    
    # Get books with PDFs and covers
    complete_books = df[(df['local_pdf_path'] != '') & (df['local_cover_path'] != '')]
    
    if len(complete_books) > 0:
        # Create a "complete" collection
        collection_path = manager.create_collection("Complete", complete_books.head(20))
        print(f"Created collection with {len(complete_books.head(20))} complete books")
    
    # Example 8: Access specific book files
    print("\n📂 Example 8: Access Book Files")
    print("-" * 30)
    
    if len(df) > 0:
        # Get first book with PDF
        book_with_pdf = df[df['local_pdf_path'] != ''].iloc[0]
        
        print(f"Book: {book_with_pdf['title']}")
        print(f"PDF Path: {book_with_pdf['local_pdf_path']}")
        print(f"Cover Path: {book_with_pdf['local_cover_path']}")
        
        # Check if files exist
        if os.path.exists(book_with_pdf['local_pdf_path']):
            pdf_size = os.path.getsize(book_with_pdf['local_pdf_path']) / (1024*1024)  # MB
            print(f"PDF Size: {pdf_size:.2f} MB")
        
        if os.path.exists(book_with_pdf['local_cover_path']):
            cover_size = os.path.getsize(book_with_pdf['local_cover_path']) / 1024  # KB
            print(f"Cover Size: {cover_size:.2f} KB")
    
    # Example 9: Statistics
    print("\n📊 Example 9: Detailed Statistics")
    print("-" * 30)
    manager.get_statistics()
    
    # Example 10: Reading list creation
    print("\n📚 Example 10: Create Reading List")
    print("-" * 30)
    
    # Get some diverse books
    diverse_books = pd.concat([
        df[df['categories'].str.contains('Fiction', case=False)].head(2),
        df[df['categories'].str.contains('Science', case=False)].head(2),
        df[df['categories'].str.contains('History', case=False)].head(2)
    ]).drop_duplicates()
    
    if len(diverse_books) > 0:
        reading_list_path = manager.create_reading_list(
            diverse_books.index.tolist(), 
            "Diverse_Reading_List"
        )
        print(f"Created reading list with {len(diverse_books)} books")

def show_file_access_examples():
    """Show how to access and work with book files"""
    
    print("\n📂 File Access Examples")
    print("=" * 30)
    
    # Load database
    try:
        df = pd.read_csv("/content/books/books_database.csv")
    except FileNotFoundError:
        print("❌ Database file not found!")
        return
    
    # Example 1: List all PDF files
    print("\n📄 Example 1: List PDF Files")
    pdf_files = df[df['local_pdf_path'] != '']['local_pdf_path'].tolist()
    print(f"Found {len(pdf_files)} PDF files:")
    for i, pdf_path in enumerate(pdf_files[:5]):
        print(f"  {i+1}. {os.path.basename(pdf_path)}")
    
    # Example 2: Find book by filename
    print("\n🔍 Example 2: Find Book by Filename")
    if pdf_files:
        sample_pdf = pdf_files[0]
        book_info = df[df['local_pdf_path'] == sample_pdf].iloc[0]
        print(f"Filename: {os.path.basename(sample_pdf)}")
        print(f"Title: {book_info['title']}")
        print(f"Author: {book_info['author']}")
        print(f"Category: {book_info['categories']}")
    
    # Example 3: File size analysis
    print("\n💾 Example 3: File Size Analysis")
    pdf_sizes = []
    for pdf_path in pdf_files[:10]:  # Check first 10
        if os.path.exists(pdf_path):
            size_mb = os.path.getsize(pdf_path) / (1024*1024)
            pdf_sizes.append(size_mb)
    
    if pdf_sizes:
        print(f"Average PDF size: {sum(pdf_sizes)/len(pdf_sizes):.2f} MB")
        print(f"Largest PDF: {max(pdf_sizes):.2f} MB")
        print(f"Smallest PDF: {min(pdf_sizes):.2f} MB")

def main():
    """Main function to run all examples"""
    print("🎓 Free Books Collection - Complete Usage Guide")
    print("=" * 60)
    
    # Check if books database exists
    if not os.path.exists("/content/books/books_database.csv"):
        print("❌ Books database not found!")
        print("\nTo get started, run the scraper:")
        print("1. In Google Colab:")
        print("   !python book_scraper.py")
        print("\n2. Or locally:")
        print("   pip install -r requirements.txt")
        print("   python book_scraper.py")
        return
    
    # Run examples
    demonstrate_usage()
    show_file_access_examples()
    
    print("\n" + "=" * 60)
    print("✨ Examples completed! You can now:")
    print("📖 Search and browse books")
    print("📂 Access PDF files and covers")
    print("📊 Analyze your collection")
    print("📁 Create custom collections")
    print("\n💡 Check the README.md for more advanced usage!")

if __name__ == "__main__":
    main()