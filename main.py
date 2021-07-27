from typing import Optional

from fastapi import FastAPI
from resume_parser import resumeparse





app = FastAPI()


@app.get("/")
def read_root():
    data = resumeparse.read_file('/Users/jonathan.waldman/PycharmProjects/pythonProject/resume/import/Resume-Jonathan-Waldman.pdf')

    return data


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}