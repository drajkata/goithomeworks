# -- Lista uczniów w wybranej grupie.

# SELECT name AS Name
# FROM students
# WHERE group_id = 1;

from sqlalchemy import select
from connect_db import session
from models import Student

def query_6():
    q = session.execute(
        select(Student.name.label("Name"))
        .where(Student.group_id == 1)
    ).mappings().all()
    return q

if __name__ == '__main__':
    print(query_6())