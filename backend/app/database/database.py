"""
Database configuration for the AI Financial Mentor application.

This module is responsible for:
1. Connecting to the SQLite database.
2. Creating the SQLAlchemy engine.
3. Creating database sessions.
4. Providing the Base class for all database models.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///finance.db"

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()