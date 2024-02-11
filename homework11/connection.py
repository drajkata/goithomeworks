from sqlite3 import connect
from contextlib import contextmanager

@contextmanager
def create_connection(name_db):
    conn = connect(name_db)
    yield conn
    conn.rollback()
    conn.close()