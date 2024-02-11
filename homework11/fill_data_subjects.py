from random import randint
from sqlite3 import Error
from connection import create_connection
from variables import DB_NAME, NUMBER_SUBJECTS, NUMBER_LECTURERS, NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_ASSESSMENTS_PER_STUDENT, QUERY_DICT, SUBJECTS_LIST

def prepare_date(numbers) -> tuple:
    for_data = []
    for i in range(numbers):
        for_data.append((SUBJECTS_LIST[i], randint(1, NUMBER_LECTURERS)))
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
        create_data(conn, prepare_date(NUMBER_SUBJECTS))