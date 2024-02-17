import faker
from random import randint
from connect_db import session
from models import Student
from variables import NUMBER_STUDENTS, NUMBER_GROUPS

def generate_data(numbers) -> list:
    fake_data = []
    f = faker.Faker()
    for _ in range(numbers):
        fake_data.append((f.name(), randint(1, NUMBER_GROUPS)))
    return fake_data

def create_data(data) -> None:
    for fake_student in data:
        student = Student(name=fake_student[0], group_id=fake_student[1])
        session.add(student)
    session.commit()

def create_students(numbers):
    create_data(generate_data(numbers))

if __name__ == '__main__':
    create_students(NUMBER_STUDENTS)