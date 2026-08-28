from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import Literal
from database import engine, get_db
from models import Base, ProblemDB, UserDB
from schemas import UserCreate, UserOut
from auth import hash_password

app = FastAPI(title="LeetCode Progress Tracker API")
Base.metadata.create_all(bind=engine)


class Problem(BaseModel):
    number: int
    title: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    topic: str
    url: HttpUrl


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/problems", status_code=status.HTTP_201_CREATED)
def create_problem(problem: Problem, db:Session = Depends(get_db)):
    db_problem = ProblemDB(
        number = problem.number,
        title = problem.title,
        difficulty = problem.difficulty,
        topic = problem.topic,
        url = str(problem.url),
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@app.get("/problems")
def get_problems(db:Session = Depends(get_db)):
    return db.query(ProblemDB).all()


@app.get("/problems/{number}")
def get_problem(number:int, db:Session = Depends(get_db)):
    problem = db.query(ProblemDB).filter(ProblemDB.number == number).first()
    if problem is None:
        raise HTTPException(status_code=404,detail=f"Problem{number} not found")
    return problem


@app.put("/problems/{number}")
def update_problem(number: int, update_problem: Problem,db:Session = Depends(get_db)):
    problem = db.query(ProblemDB).filter(ProblemDB.number == number).first()
    if problem is None:
        raise HTTPException(status_code=404, detail=f"Problem {number} not found")
    problem.title = update_problem.title
    problem.difficulty = update_problem.difficulty
    problem.topic = update_problem.topic
    problem.url = str(update_problem.url)
    db.commit()
    db.refresh(problem)
    return problem


    
@app.delete("/problems/{number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem(number: int, db:Session = Depends(get_db)):
    problem = db.query(ProblemDB).filter(ProblemDB.number == number).first()
    if problem is None:
        raise HTTPException(status_code=404, detail=f"Problem {number} not found")
    db.delete(problem)
    db.commit()
    return

@app.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user:UserCreate,db:Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    new_user = UserDB(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user