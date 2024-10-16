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



class CrudOperations:
    def __init__(self, db:Session):
        self.db = db

    def create_user(self, user:UserCreate):
        db_user = self.db.query(User).filter(User.email == user.email).first()
        
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user.password)
        new_user = User(email=user.email, password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def get_user(self,user_id:int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self,user_id:int,user:UserCreate):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail={"message": "user not found"})
        

        if user.email:
            db_user.email = user.email
        if user.password:
            db_user.password = hash_password(user.password)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user


    def delete_user(self,user_id:int):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail={"message": "user not found"})

        self.db.delete(db_user)
        self.db.commit()
        return db_user
