from fastapi import FastAPI, status
from pydantic import BaseModel, HttpUrl
from typing import Literal

app = FastAPI(title="LeetCode Progress Tracker API")


class Problem(BaseModel):
    number: int
    title: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    topic: str
    url: HttpUrl


# 临时的内存存储，之后 Stage 2 会换成 PostgreSQL
problems: list[Problem] = []


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/problems", status_code=status.HTTP_201_CREATED)
def create_problem(problem: Problem):
    problems.append(problem)
    return problem

@app.get("/problems")
def get_problems():
    return problems