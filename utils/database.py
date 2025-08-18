import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Create DB engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10, # keep 10 connections in the pool
    max_overflow=20, # allow 20 extra connections if needed
    pool_timeout=30, #wait for 30 seconds for a connection
    pool_recycle=3600, # refresh connections every hour
)

# create database session
SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)

# Base class for models
Base = declarative_base()

#dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()