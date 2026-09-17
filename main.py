from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, HttpUrl
from typing import Literal
from database import engine, get_db
from models import Base, ProblemDB, UserDB
from schemas import UserCreate, UserOut, UserLogin
from auth import hash_password, verify_password, create_access_token, decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt as pyjwt_lib

app = FastAPI(title="LeetCode Progress Tracker API")
Base.metadata.create_all(bind=engine)
bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise auth_error

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")

        if not isinstance(user_id, str) or not user_id.isdecimal():
            raise auth_error

        user_id = int(user_id)

    except pyjwt_lib.InvalidTokenError:
        raise auth_error

    user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if user is None:
        raise auth_error

    return user


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
def create_problem(
    problem: Problem,
    db: Session = Depends(get_db),
):
    existing_problem = (
        db.query(ProblemDB)
        .filter(ProblemDB.number == problem.number)
        .first()
    )

    if existing_problem is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Problem {problem.number} already exists",
        )

    db_problem = ProblemDB(
        number=problem.number,
        title=problem.title,
        difficulty=problem.difficulty,
        topic=problem.topic,
        url=str(problem.url),
    )

    db.add(db_problem)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        duplicate = (
            db.query(ProblemDB)
            .filter(ProblemDB.number == problem.number)
            .first()
        )

        if duplicate is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Problem {problem.number} already exists",
            )

        raise

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

@app.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=UserOut)
def get_me(
    current_user: UserDB = Depends(get_current_user),
):
    return current_user