# -- Przedmioty, które prowadzi wybrany wykładowca.

# SELECT name AS Subject
# FROM subjects
# WHERE lecturer_id = 1;

from sqlalchemy import select
from connect_db import session
from models import Subject

def query_5():
    q = session.execute(
        select(Subject.name.label("Subject"))
        .where(Subject.lecturer_id == 1)
    ).mappings().all()
    return q

if __name__ == '__main__':
    print(query_5())