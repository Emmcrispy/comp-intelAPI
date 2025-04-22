# app/config/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# SQLAlchemy Base for models to inherit
Base = declarative_base()

# Engine for database connection
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
