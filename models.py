from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.sql import func
from database import Base

class ProblemDB(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, index=True)
    title = Column(String)
    difficulty = Column(String)
    topic = Column(String)
    url = Column(String)

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())