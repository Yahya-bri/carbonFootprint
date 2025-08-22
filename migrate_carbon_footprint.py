#!/usr/bin/env python3
"""
Database migration script to add carbon footprint fields to UniteTravail table.
This script adds distance_km and co2_kg columns to track carbon footprint calculations.
"""

import sqlite3
import os
from src.db import DB_FILE

def migrate_carbon_footprint_fields():
    """Add carbon footprint fields to the unite_travail table"""
    
    if not os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} does not exist. Nothing to migrate.")
        return
    
    print(f"Migrating database: {DB_FILE}")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(unite_travail)")
        columns = [column[1] for column in cursor.fetchall()]
        
        migrations_applied = []
        
        # Add distance_km column if it doesn't exist
        if 'distance_km' not in columns:
            cursor.execute('ALTER TABLE unite_travail ADD COLUMN distance_km REAL')
            migrations_applied.append('distance_km')
            print("✅ Added distance_km column")
        else:
            print("ℹ️  distance_km column already exists")
        
        # Add co2_kg column if it doesn't exist
        if 'co2_kg' not in columns:
            cursor.execute('ALTER TABLE unite_travail ADD COLUMN co2_kg REAL')
            migrations_applied.append('co2_kg')
            print("✅ Added co2_kg column")
        else:
            print("ℹ️  co2_kg column already exists")
        
        if migrations_applied:
            conn.commit()
            print(f"✅ Migration completed successfully. Added columns: {', '.join(migrations_applied)}")
        else:
            print("ℹ️  No migration needed. All columns already exist.")
            
    except sqlite3.Error as e:
        print(f"❌ Database error during migration: {e}")
        if 'conn' in locals():
            conn.rollback()
    except Exception as e:
        print(f"❌ Unexpected error during migration: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_carbon_footprint_fields()
