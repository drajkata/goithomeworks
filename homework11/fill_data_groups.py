from sqlite3 import Error
from connection import create_connection
from variables import DB_NAME, NUMBER_SUBJECTS, NUMBER_LECTURERS, NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_ASSESSMENTS_PER_STUDENT, QUERY_DICT, SUBJECTS_LIST

def generate_data(numbers) -> list:
    fake_groups = []
    for i in range(numbers):
        letter = 'ABCDEFGHIJKLMNOPQRSTUWYZ'
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