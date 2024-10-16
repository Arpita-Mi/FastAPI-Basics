from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.pool import NullPool
import psycopg2
from .config import db
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
SQLALCHEMY_DATABASE_URL = f"postgresql://{db.DATABASE_USERNAME}:{db.DATABASE_PASSWORD}@{db.DATABASE_HOST}:{db.DATABASE_PORT}/{db.DATABASE_NAME}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


        