#!/usr/bin/env python3
"""Initialize the database with tables and default data."""

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import DatabaseManager
from app.core.config import settings


def main():
    """Initialize the database."""
    print("Initializing database...")
    print(f"Database URL: {settings.database_url}")
    
    # Ensure data directory exists
    if settings.database_url.startswith("sqlite"):
        db_path = settings.database_url.replace("sqlite:///", "")
        data_dir = os.path.dirname(db_path)
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)
            print(f"Created data directory: {data_dir}")
    
    # Initialize database
    DatabaseManager.init_database()
    
    # Print statistics
    stats = DatabaseManager.get_database_stats()
    print("\nDatabase initialized successfully!")
    print("Statistics:")
    for table, count in stats.items():
        print(f"  {table}: {count} records")


if __name__ == "__main__":
    main()