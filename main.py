from fastapi import FastAPI
from typing import List, Optional
from uuid import UUID, uuid4
import testdb
from pydantic import BaseModel
from auth import *

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


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
