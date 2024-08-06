from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, JSON
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base = declarative_base()


class Student(Base):
    __tablename__ = "test"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    licenses = Column(JSON)


def create_student(name: str, age: int):
    new_student = Student(
        name=name,
        age=age,
    )
    session.add(new_student)
    session.commit()


def create_customer(name: str, age: int, licenses: dict):
    new_customer = Customer(name=name, age=age, licenses=licenses)
    session.add(new_customer)
    session.commit()


def get_students():
    return session.query(Student).all()


if __name__ == "__main__":
    # Base.metadata.create_all(bind=engine)
    # create_customer(
    #     "Joe",
    #     22,
    #     licenses={"testID": {"id": "testID", "expiration": "today", "used": False}},
    # )
    create_student("Joe", 22)
    print("Students")
    students = session.query(Student).all()
    for student in students:
        print(student.name, student.age, student.id)
    print("\nCustomers")
    customers = session.query(Customer).all()
    for customer in customers:
        print(customer.name, customer.age, customer.id, customer.licenses["testID"])
