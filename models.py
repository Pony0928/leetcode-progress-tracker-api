from sqlalchemy import Column, Integer, String
from database import Base

class ProblemDB(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, index=True)
    title = Column(String)
    difficulty = Column(String)
    topic = Column(String)
    url = Column(String)