from sqlite3 import Error
from connection import create_connection, DB_NAME

def create_tables(conn):
    with open('school.sql', 'r') as f:
        sql = f.read()
    cur = conn.cursor()
    try:
        cur.executescript(sql)
    except Error as e:
        print(e)

def fill_data():
    with open("fill_data_groups.py") as groups:
        exec(groups.read())
    with open("fill_data_students.py") as students:
        exec(students.read())
    with open("fill_data_lecturers.py") as lecturers:
        exec(lecturers.read())
    with open("fill_data_subjects.py") as subjects:
        exec(subjects.read())
    with open("fill_data_assessments.py") as assessments:
        exec(assessments.read())

def get_query(conn, sql_query):
    with open(sql_query, 'r') as q:
        query = q.read()
    cur = conn.cursor()
    try:
        cur.executescript(query)
    except Error as e:
        print(e)

QUERY_DICT = {
    "1" : "query_1.sql",
    "2" : "query_2.sql",
    "3" : "query_3.sql",
    "4" : "query_4.sql",
    "5" : "query_5.sql",
    "6" : "query_6.sql",
    "7" : "query_7.sql",
    "8" : "query_8.sql",
    "9" : "query_9.sql",
    "10" : "query_10.sql",

}

if __name__ == '__main__':
   
    with create_connection(DB_NAME) as conn:
        if conn is not None:
            create_tables(conn)
        else:
            print("Error! cannot create the database connection.")
    fill_data()
    while(True):
        choice = input("\nEnter number of guery: ")
        if choice in QUERY_DICT.keys():
            get_query(conn, QUERY_DICT[choice])
        elif choice.lower() in ["end", "exit", "."]:
            break
        else:
            print("\nYou have entered an incorrect inquiry number. Enter a value from 1 to 10.")
        print("\nTo exit the program, enter 'end', 'exit' or '.'\n")
