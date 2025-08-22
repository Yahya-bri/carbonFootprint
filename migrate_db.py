#!/usr/bin/env python3
"""
Migration script to update the database schema.
This will backup the existing data and recreate tables with the new schema.
"""

import os
import sqlite3
import shutil
from datetime import datetime
from src.db import init_db, get_session, engine
from src.models import Base, Sondeur, Essai, Chantier, UniteTravail

def backup_database():
    """Create a backup of the current database"""
    db_path = r'c:\Users\503386971\Documents\Projects\00_my_project\project_kill_me_plz\app.db'
    if os.path.exists(db_path):
        backup_path = db_path.replace('.db', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
        shutil.copy2(db_path, backup_path)
        print(f"Database backed up to: {backup_path}")
        return backup_path
    return None

def migrate_data():
    """Migrate data from old schema to new schema"""
    db_path = r'c:\Users\503386971\Documents\Projects\00_my_project\project_kill_me_plz\app.db'
    
    if not os.path.exists(db_path):
        print("No existing database found. Creating new database...")
        init_db()
        return
    
    # Backup existing database
    backup_path = backup_database()
    
    # Read existing data
    old_data = {'sondeurs': [], 'essais': [], 'chantiers': [], 'unite_travail': []}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Read existing data
        try:
            cursor.execute("SELECT * FROM sondeurs")
            old_data['sondeurs'] = cursor.fetchall()
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("SELECT * FROM essais")
            old_data['essais'] = cursor.fetchall()
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("SELECT * FROM chantiers")
            old_data['chantiers'] = cursor.fetchall()
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("SELECT * FROM unite_travail")
            old_data['unite_travail'] = cursor.fetchall()
        except sqlite3.OperationalError:
            pass
        
        conn.close()
        
    except Exception as e:
        print(f"Error reading existing data: {e}")
        return
    
    # Remove old database
    os.remove(db_path)
    
    # Create new database with updated schema
    print("Creating new database with updated schema...")
    init_db()
    
    # Migrate data
    session = get_session()
    try:
        # Migrate sondeurs
        for row in old_data['sondeurs']:
            if len(row) >= 2:  # id, name, address (optional)
                sondeur = Sondeur(
                    name=row[1],
                    address=row[2] if len(row) > 2 else None
                )
                session.add(sondeur)
        
        # Migrate essais
        for row in old_data['essais']:
            if len(row) >= 2:  # id, name, description (optional)
                essai = Essai(
                    name=row[1],
                    description=row[2] if len(row) > 2 else None
                )
                session.add(essai)
        
        # Migrate chantiers
        for row in old_data['chantiers']:
            if len(row) >= 2:  # id, name, location, date
                chantier = Chantier(
                    name=row[1],
                    location=row[2] if len(row) > 2 else None,
                    date=datetime.strptime(row[3], '%Y-%m-%d').date() if len(row) > 3 and row[3] else None
                )
                session.add(chantier)
        
        session.commit()
        
        # Migrate unite_travail (with new auto-increment ID)
        for row in old_data['unite_travail']:
            if len(row) >= 4:  # chantier_id, essai_id, sondeur_id, days, date_debut
                unite = UniteTravail(
                    chantier_id=row[0],
                    essai_id=row[1],
                    sondeur_id=row[2],
                    days=row[3],
                    date_debut=datetime.strptime(row[4], '%Y-%m-%d').date() if len(row) > 4 and row[4] else None
                )
                session.add(unite)
        
        session.commit()
        print("Data migration completed successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error during migration: {e}")
        if backup_path:
            print(f"Restoring backup from: {backup_path}")
            shutil.copy2(backup_path, db_path)
    finally:
        session.close()

if __name__ == "__main__":
    migrate_data()
