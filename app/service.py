from fastapi import Depends, HTTPException
from app.schemas import UserCreate
from app.models import User
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from passlib.context import CryptContext
import os

# Using the CryptContext from Passlib to handle password hashing.
# This setup uses the bcrypt hashing algorithm and marks older schemes as deprecated.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def create_user(user , db:Session):
    """
    Create a new user in the database.

    This function checks if the email is already registered. If not, it 
    hashes the provided password and saves the new user in the database.

    Parameters:
    - user: UserCreate - The user data containing email and password.
    - db: Session - The database session.

    Returns:
    - User: The newly created user object.

    Raises:
    - HTTPException: If the email is already registered (400).
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



