from fastapi import Depends, HTTPException
from app.schemas import UserCreate
from app.models import User
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from passlib.context import CryptContext
from utils.utils import logger

# Using the CryptContext from Passlib to handle password hashing.
# This setup uses the bcrypt hashing algorithm and marks older schemes as deprecated.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)



class CrudOperations:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        logger.info(f"Attempting to create user with email: {user.email}")
        db_user = self.db.query(User).filter(User.email == user.email).first()
        
        if db_user:
            logger.warning(f"User with email {user.email} already exists in the database.")
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user.password)
        new_user = User(email=user.email, password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        logger.info(f"New user created successfully: {new_user.email}")
        return new_user

    def get_user(self, user_id: int):
        logger.info(f"Fetching user with ID: {user_id}")
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            logger.warning(f"User with ID {user_id} not found.")
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"User fetched successfully: {user.id}")
        return user

    def update_user(self, user_id: int, user: UserCreate):
        logger.info(f"Attempting to update user with ID: {user_id}")
        db_user = self.db.query(User).filter(User.id == user_id).first()
        
        if not db_user:
            logger.warning(f"User with ID {user_id} not found.")
            raise HTTPException(status_code=404, detail={"message": "User not found"})

        if user.email:
            logger.info(f"Updating email for user ID {user_id} to {user.email}")
            db_user.email = user.email
        
        if user.password:
            hashed_password = hash_password(user.password)
            logger.info(f"Updating password for user ID {user_id}")
            db_user.password = hashed_password

        self.db.commit()
        self.db.refresh(db_user)
        logger.info(f"User updated successfully: {db_user}")
        return db_user

    def delete_user(self, user_id: int):
        logger.info(f"Attempting to delete user with ID: {user_id}")
        db_user = self.db.query(User).filter(User.id == user_id).first()
        
        if not db_user:
            logger.warning(f"User with ID {user_id} not found for deletion.")
            raise HTTPException(status_code=404, detail={"message": "User not found"})

        self.db.delete(db_user)
        self.db.commit()
        logger.info(f"User with ID {user_id} deleted successfully.")
        return db_user

