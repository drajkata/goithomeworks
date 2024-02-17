from datetime import datetime
from random import randint
from connect_db import session
from models import Assessment
from variables import NUMBER_SUBJECTS, NUMBER_STUDENTS, NUMBER_ASSESSMENTS_PER_STUDENT

def generate_data(number) -> list:
    for_data = []
    for i in range(number):
        if i < 0.5 * number:
            create_date = datetime(2022, randint(10, 12), randint(1,28)).date()
        else:
            create_date = datetime(2023, randint(1, 6), randint(1,28)).date()
        for id_student in range(1, NUMBER_STUDENTS + 1):
            for_data.append((randint(1, 5), id_student, randint(1, NUMBER_SUBJECTS), create_date))
    return for_data

def create_data(data) -> None:
    for fake_assessment in data:
        assessment = Assessment(assessment=fake_assessment[0], student_id=fake_assessment[1], subject_id=fake_assessment[2], created_at=fake_assessment[3])
        session.add(assessment)
    session.commit()

def create_assessments(number):
    create_data(generate_data(number))

if __name__ == '__main__':
    create_assessments(NUMBER_ASSESSMENTS_PER_STUDENT)