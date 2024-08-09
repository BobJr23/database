from fastapi import FastAPI
from typing import List, Optional
from uuid import UUID, uuid4
import testdb
from pydantic import BaseModel
from auth import *
import requests
import random
import logging

app = FastAPI()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Student(BaseModel):
    name: str
    age: int


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    logger.info(f"Say hello endpoint called with name: {name}")
    return {"message": f"Hello {name}"}


@app.get("/weather/{city}")
async def get_weather(city: str):
    logger.info(f"Get weather endpoint called for city: {city}")
    response = requests.get(
        f"https://api.weatherapi.com/v1/current.json?q={city}&key={WEATHER_KEY}"
    )
    return response.json()


@app.get("/random-number/{mini}/{maxi}")
async def get_random_number(mini: int, maxi: int):
    logger.info(f"Get random number endpoint called with range: {mini}-{maxi}")
    return random.randint(mini, maxi)


@app.get("/status/")
async def get_status():
    logger.info("Status endpoint called")
    return {"status": "OK"}


@app.post("/new-student/", response_model=Student)
async def create_student(student: Student):
    logger.info(f"Create student endpoint called with data: {student}")
    testdb.create_student(student.name, student.age)
    return student


@app.get("/customers/", response_model=List[CustomerModel])
async def get_customers():
    logger.info("Get customers endpoint called")
    students = testdb.get_customers()
    return students


@app.post("/new-customer/", response_model=CustomerModel)
async def create_customer(student: CustomerModel):
    logger.info(f"Create customer endpoint called with data: {student}")
    testdb.create_customer(student.name, student.age)
    return student


@app.get("/students/", response_model=List[Student])
async def get_students():
    logger.info("Get students endpoint called")
    students = testdb.get_students()
    return students


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    logger.info(
        f"Login for access token endpoint called with username: {form_data.username}"
    )
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
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


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    logger.info(f"Read users me endpoint called for user: {current_user.username}")
    return current_user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
