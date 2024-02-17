from random import randint
from connect_db import session
from models import Subject
from variables import NUMBER_LECTURERS, SUBJECTS_LIST

def generate_date(subjects: list) -> list:
    for_data = []
    for i in range(len(subjects)):
        for_data.append((subjects[i], randint(1, NUMBER_LECTURERS)))
    return for_data

def create_data(data) -> None:
    for fake_subject in data:
        subject = Subject(name=fake_subject[0], lecturer_id=fake_subject[1])
        session.add(subject)
    session.commit()

def create_subjects(subjects):
    create_data(generate_date(subjects))

if __name__ == '__main__':
    create_subjects(SUBJECTS_LIST)