from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
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


# Base.metadata.create_all(bind=engine)
def create_student(name: str, age: int):
    new_student = Student(name=name, age=age)
    session.add(new_student)
    session.commit()


def get_students():
    return session.query(Student).all()


if __name__ == "__main__":
    students = session.query(Student).all()
    print(students)
    for student in students:
        print(student.name, student.age, student.id)
