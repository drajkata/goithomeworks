from sqlite3 import connect
from contextlib import contextmanager

DB_NAME = "school.db"

@contextmanager
def create_connection(DB_NAME):
    conn = connect(DB_NAME)
    yield conn
    conn.rollback()
    conn.close()