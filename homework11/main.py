from sqlite3 import Error
from connection import create_connection
import os
import faker
from random import randint
from datetime import datetime
from variables import DB_NAME, DB_SCRIPT, NUMBER_SUBJECTS, NUMBER_LECTURERS, NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_ASSESSMENTS_PER_STUDENT, QUERY_DICT, SUBJECTS_LIST

def create_tables(conn):
    with open(DB_SCRIPT, 'r') as f:
        sql = f.read()
    cur = conn.cursor()
    try:
        cur.executescript(sql)
    except Error as e:
        print(e)

def read_file(dir):
        exec(
            compile(open(dir, "rb").read(), dir, 'exec'),
            globals(),
            locals()
        )

def fill_data():  
    read_file(os.path.abspath("fill_data_groups.py"))
    read_file(os.path.abspath("fill_data_students.py"))
    read_file(os.path.abspath("fill_data_lecturers.py"))
    read_file(os.path.abspath("fill_data_subjects.py"))
    read_file(os.path.abspath("fill_data_assessments.py"))

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
        fill_data()
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
