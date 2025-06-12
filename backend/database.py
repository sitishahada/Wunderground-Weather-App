# === backend/database.py ===
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# You can replace this with Railway or your own PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin@localhost/WWeather_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
