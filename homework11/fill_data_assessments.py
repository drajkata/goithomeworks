from datetime import datetime
from random import randint
from sqlite3 import Error
from connection import create_connection, DB_NAME


NUMBER_STUDENTS = 50
NUMBER_SUBJECTS = 8
NUMBER_ASSESSMENTS_PER_STUDENT = 20

def prepare_date(numbers) -> tuple:
    global NUMBER_STUDENTS, NUMBER_SUBJECTS
    for_data = []
    
    for i in range(numbers):
        if i < 0.5 * numbers:
            create_date = datetime(2022, randint(10, 12), randint(1,28)).date()
        else:
            create_date = datetime(2023, randint(1, 6), randint(1,28)).date()
        for id_student in range(1, NUMBER_STUDENTS + 1):
            for_data.append((randint(1, 5), id_student, randint(1, NUMBER_SUBJECTS), create_date))
    return for_data

def create_data(conn, data) -> None:
    sql = '''
    INSERT INTO assessments(assessment, student_id, subject_id, created_at) VALUES(?,?,?,?);
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
        create_data(conn, prepare_date(NUMBER_ASSESSMENTS_PER_STUDENT))