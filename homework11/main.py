from variables import DB_NAME, DB_SCRIPT, NUMBER_LECTURERS, NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_ASSESSMENTS_PER_STUDENT, QUERY_DICT, SUBJECTS_LIST
from sqlite3 import Error
from connection import create_connection
from fill_data_groups import create_groups
from fill_data_students import create_students
from fill_data_lecturers import create_lecturers
from fill_data_subjects import create_subjects
from fill_data_assessments import create_assessments

def create_tables(conn):
    with open(DB_SCRIPT, 'r') as f:
        sql = f.read()
    cur = conn.cursor()
    try:
        cur.executescript(sql)
    except Error as e:
        print(e)

def fill_tables(conn):
    create_groups(conn, NUMBER_GROUPS)
    create_students(conn, NUMBER_STUDENTS)
    create_lecturers(conn, NUMBER_LECTURERS)
    create_subjects(conn, SUBJECTS_LIST)
    create_assessments(conn, NUMBER_ASSESSMENTS_PER_STUDENT)

def get_query(conn, sql_query):
    with open(sql_query, 'r') as q:
        query = q.read()
    c = conn.cursor()
    try:
        c.execute(query)
    except Error as e:
        print(e)
    return c.fetchall()

if __name__ == '__main__':
   
    with create_connection(DB_NAME) as conn:
        if conn is not None:
            create_tables(conn)
        else:
            print("Error! cannot create the database connection.")
        fill_tables(conn)
        while(True):
            choice = input("\nEnter number of guery: ")
            if choice in QUERY_DICT.keys():
                print(f"\n{QUERY_DICT[choice][1]}\n")
                for tuple in get_query(conn, QUERY_DICT[choice][0]):
                    print(tuple)
            elif choice.lower() in ["end", "exit", "."]:
                print("\nGood bye!\n")
                break
            else:
                print("\nYou have entered an incorrect inquiry number. Enter a value from 1 to 10.")
            print("\nTo exit the program, enter 'end', 'exit' or '.'\n")
