import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_FILE = os.path.join(PROJECT_ROOT, 'app.db')
DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    # Import models lazily to avoid circular imports
    from src.models import Base
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()
