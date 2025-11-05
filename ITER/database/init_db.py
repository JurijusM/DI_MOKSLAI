"""
Initialize ITER Database
Creates database schema and tables.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.database import init_database, engine
from backend.app.models import Base

def main():
    """Initialize the database."""
    print("=" * 60)
    print("ITER Database Initialization")
    print("=" * 60)
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("\n[OK] Database initialized successfully!")
        print(f"[INFO] Database location: {Path(__file__).parent / 'iter.db'}")
        print("\nTables created:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
    except Exception as e:
        print(f"\n[ERROR] Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



