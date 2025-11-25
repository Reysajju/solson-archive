# Additional Utilities for Book Processing

import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional
import zipfile
import shutil

class BookManager:
    """Utility class to manage the scraped book collection"""
    
    def __init__(self, base_dir: str = "/content/books"):
        self.base_dir = Path(base_dir)
        self.csv_path = self.base_dir / "books_database.csv"
        self.df = None
        self.load_database()
    
    def load_database(self):
        """Load the books database from CSV"""
        if self.csv_path.exists():
            self.df = pd.read_csv(self.csv_path)
            print(f"📚 Loaded {len(self.df)} books from database")
        else:
            print("❌ No database found. Run the scraper first.")
    
    def search_books(self, query: str, search_field: str = 'title') -> pd.DataFrame:
        """Search books by title, author, or category"""
        if self.df is None:
            return pd.DataFrame()
        
        if search_field in ['title', 'author', 'description', 'categories']:
            mask = self.df[search_field].str.contains(query, case=False, na=False)
            return self.df[mask]
        else:
            print(f"❌ Invalid search field: {search_field}")
            return pd.DataFrame()
    
    def get_books_by_category(self, category: str) -> pd.DataFrame:
        """Get all books in a specific category"""
        return self.search_books(category, 'categories')
    
    get_books_by_language = lambda self, lang: self.df[self.df['language'] == lang] if self.df is not None else pd.DataFrame()
    
    def get_most_popular(self, n: int = 10) -> pd.DataFrame:
        """Get n most popular books by download count"""
        if self.df is None:
            return pd.DataFrame()
        
        return self.df.nlargest(n, 'download_count')
    
    def get_recent_books(self, n: int = 10) -> pd.DataFrame:
        """Get n most recently added books"""
        if self.df is None:
            return pd.DataFrame()
        
        return self.df.nlargest(n, 'added_date')
    
    def create_collection(self, name: str, books_df: pd.DataFrame):
        """Create a custom collection CSV"""
        collection_path = self.base_dir / f"collection_{name.lower().replace(' ', '_')}.csv"
        books_df.to_csv(collection_path, index=False)
        print(f"📁 Created collection: {collection_path}")
        return collection_path
    
    def get_statistics(self):
        """Print collection statistics"""
        if self.df is None:
            print("❌ No database loaded")
            return
        
        print("📊 COLLECTION STATISTICS")
        print("=" * 40)
        print(f"Total books: {len(self.df)}")
        print(f"Books with PDFs: {len(self.df[self.df['local_pdf_path'] != ''])}")
        print(f"Books with covers: {len(self.df[self.df['local_cover_path'] != ''])}")
        
        # Sources
        print("\n📚 Sources:")
        print(self.df['source'].value_counts())
        
        # Languages
        print("\n🌐 Languages:")
        print(self.df['language'].value_counts().head(5))
        
        # Top categories
        categories = self.df['categories'].str.split(', ').explode().value_counts().head(10)
        print("\n🏷️  Top Categories:")
        print(categories)
        
        # File sizes
        total_size = self.df['file_size'].sum() / (1024**3)  # GB
        print(f"\n💾 Total collection size: {total_size:.2f} GB")
    
    def export_book_info(self, book_index: int) -> Dict:
        """Export detailed information for a single book"""
        if self.df is None or book_index >= len(self.df):
            return {}
        
        book = self.df.iloc[book_index]
        return {
            'title': book['title'],
            'author': book['author'],
            'description': book['description'],
            'pdf_path': book['local_pdf_path'],
            'cover_path': book['local_cover_path'],
            'categories': book['categories'],
            'language': book['language'],
            'source': book['source']
        }
    
    def create_reading_list(self, book_indices: List[int], list_name: str) -> str:
        """Create a reading list from selected books"""
        if self.df is None:
            return ""
        
        selected_books = self.df.iloc[book_indices]
        return self.create_collection(list_name, selected_books)
    
    def backup_collection(self, backup_name: str = None):
        """Create a backup of the entire collection"""
        if backup_name is None:
            from datetime import datetime
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = self.base_dir.parent / backup_name
        backup_path.mkdir(exist_ok=True)
        
        # Copy all files
        if self.base_dir.exists():
            shutil.copytree(self.base_dir, backup_path / "books", dirs_exist_ok=True)
        
        # Create a zip as well
        zip_path = self.base_dir.parent / f"{backup_name}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.base_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.base_dir)
                    zipf.write(file_path, arcname)
        
        print(f"📦 Backup created: {backup_path}")
        print(f"📦 Backup zip created: {zip_path}")
        return backup_path, zip_path

# Quick usage examples for Colab
def quick_examples():
    """Quick usage examples for Google Colab"""
    
    print("🚀 Quick Usage Examples")
    print("=" * 30)
    
    # Initialize manager
    manager = BookManager()
    
    if manager.df is None:
        print("❌ No books database found. Run the scraper first.")
        return
    
    # Example 1: Search for Python books
    python_books = manager.search_books('Python')
    print(f"\n📖 Found {len(python_books)} Python books:")
    if len(python_books) > 0:
        print(python_books[['title', 'author']].head())
    
    # Example 2: Get fiction books
    fiction_books = manager.get_books_by_category('Fiction')
    print(f"\n📚 Found {len(fiction_books)} fiction books")
    
    # Example 3: Most popular books
    popular = manager.get_most_popular(5)
    print(f"\n⭐ Top 5 most popular books:")
    print(popular[['title', 'author', 'download_count']])
    
    # Example 4: Create a classics collection
    classics = manager.search_books('Classic', 'categories')
    if len(classics) > 0:
        manager.create_collection("Classics", classics.head(20))
    
    # Example 5: Statistics
    manager.get_statistics()

if __name__ == "__main__":
    quick_examples()