from random import randint
from sqlite3 import Error
from connection import create_connection
from variables import DB_NAME, NUMBER_LECTURERS, SUBJECTS_LIST

def prepare_date(subjects: list) -> tuple:
    for_data = []
    for i in range(len(subjects)):
        for_data.append((subjects[i], randint(1, NUMBER_LECTURERS)))
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

def create_subjects(conn, subjects):
    create_data(conn, prepare_date(subjects))

if __name__ == '__main__':
    with create_connection(DB_NAME) as conn:
        create_subjects(conn, SUBJECTS_LIST)