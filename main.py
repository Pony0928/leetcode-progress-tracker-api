from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import Literal

app = FastAPI(title="LeetCode Progress Tracker API")


class Problem(BaseModel):
    number: int
    title: str
    difficulty: Literal["Easy", "Medium", "Hard"]
    topic: str
    url: HttpUrl


@app.get("/health")
def health_check():
    return {"status": "ok"}