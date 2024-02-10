from sqlite3 import Error
# from main import DB_NAME, create_connection
from connection import create_connection, DB_NAME

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 50
NUMBER_SUBJECTS = 8
NUMBER_LECTURERS = 5

NUMBER_ASSESSMENT_PER_STUDENT = 20

def generate_data(numbers) -> list:
    fake_groups = []
    for i in range(numbers):
        letter = 'ABC'
        template_name = f"2022/2023-{letter[i]}"
        fake_groups.append(template_name)
    return fake_groups

def prepare_date(groups) -> tuple:
    for_groups = []
    for group in groups:
        for_groups.append((group,))
    return for_groups


def create_data(conn, groups) -> None:
    sql = '''
    INSERT INTO groups(name) VALUES(?);
    '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, groups)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


if __name__ == '__main__':
    with create_connection(DB_NAME) as conn:
        create_data(conn, prepare_date(generate_data(NUMBER_GROUPS)))