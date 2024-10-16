from sqlalchemy import Boolean ,Column, ForeignKey, Integer , String
from sqlalchemy.orm import relationship
from app.database import Base
import psycopg2

class User(Base):
    __tablename__ = "user"

    id = Column(Integer,autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    