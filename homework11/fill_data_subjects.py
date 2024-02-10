import faker
from random import randint
from sqlite3 import Error
from connection import create_connection, DB_NAME

NUMBER_SUBJECTS = 8
NUMBER_LECTURERS = 5

SUBJECTS_LIST = ["Mathematics", "Biology", "History", "Chemistry", "Literature", "Physics", "Art", "Physical Education"]

def generate_data(numbers) -> list:
    global SUBJECTS_LIST
    fake_data = []
    f = faker.Faker()
    for i in range(numbers):
        fake_data.append(SUBJECTS_LIST[i])
    return fake_data

def prepare_date(data) -> tuple:
    for_data = []
    for i in data:
        for_data.append((i, randint(1, NUMBER_LECTURERS)))
    return for_data

def create_data(conn, data) -> None:
    sql = '''
    INSERT INTO subjects(name, lecturer_id) VALUES(?, ?);
    '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, data)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


if __name__ == '__main__':
    with create_connection(DB_NAME) as conn:
        create_data(conn, prepare_date(generate_data(NUMBER_SUBJECTS)))