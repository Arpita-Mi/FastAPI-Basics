from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.pool import NullPool
import psycopg2
from .config import db
from utils.utils import logger


Base = declarative_base()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db.DATABASE_USERNAME}:"
    f"{db.DATABASE_PASSWORD}@{db.DATABASE_HOST}:"
    f"{db.DATABASE_PORT}/{db.DATABASE_NAME}"
)

# Create the database engine
try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=NullPool  
    )
    logger.info("Database engine created successfully.")
except ProgrammingError as e:
    logger.error(f"Failed to create database engine: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        logger.info("Database session created successfully.")
        yield db
    except Exception as e:
        logger.error(f"Error occurred while using the database session: {e}")
    finally:
        db.close()
        logger.info("Database session closed.")






        