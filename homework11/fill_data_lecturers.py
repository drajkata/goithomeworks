import faker
from sqlite3 import Error
from connection import create_connection
from variables import DB_NAME, NUMBER_SUBJECTS, NUMBER_LECTURERS, NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_ASSESSMENTS_PER_STUDENT, QUERY_DICT, SUBJECTS_LIST

def generate_fake_data(numbers) -> list:
    fake_data = []
    f = faker.Faker()
    for _ in range(numbers):
        fake_data.append(f.name())
    return fake_data

def prepare_date(data) -> tuple:
    for_data = []
    for i in data:
        for_data.append((i,))
    return for_data

def create_data(conn, data) -> None:
    sql = '''
    INSERT INTO lecturers(name) VALUES(?);
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
        create_data(conn, prepare_date(generate_fake_data(NUMBER_LECTURERS)))