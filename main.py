from fastapi import FastAPI
from typing import List, Optional
from uuid import UUID, uuid4
import testdb
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    name: str
    age: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/new-student/", response_model=Student)
async def create_student(student: Student):
    testdb.create_student(student.name, student.age)
    return student


@app.get("/students/", response_model=List[Student])
async def get_students():
    students = testdb.get_students()
    return students


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
