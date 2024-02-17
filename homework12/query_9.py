# -- Lista kursów, na które uczęszcza uczeń.

# SELECT s.name AS Subject
# FROM assessments AS a
#     JOIN subjects AS s ON a.subject_id = s.id
# WHERE student_id = 1
# GROUP BY Subject
# ORDER BY Subject ASC;

from sqlalchemy import select
from connect_db import session
from models import Assessment, Subject

def query_9():
    q = session.execute(
        select(Subject.name.label("Subject"))
        .select_from(Assessment)
        .join(Subject)
        .where(Assessment.student_id == 1)
        .group_by(Subject)
        .order_by("Subject")
    ).mappings().all()
    return q

if __name__ == '__main__':
    print(query_9())