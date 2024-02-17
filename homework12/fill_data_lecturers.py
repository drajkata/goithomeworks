import faker
from connect_db import session
from models import Lecturer
from variables import NUMBER_LECTURERS

def generate_data(numbers) -> list:
    fake_data = []
    f = faker.Faker()
    for _ in range(numbers):
        fake_data.append(f.name())
    return fake_data

def create_data(data) -> None:
    for fake_data in data:
        lecturer = Lecturer(name=fake_data)
        session.add(lecturer)
    session.commit()

def create_lecturers(numbers):
    create_data(generate_data(numbers))

if __name__ == '__main__':
    create_lecturers(NUMBER_LECTURERS)