# -- Lista kursów prowadzonych przez wybranego wykładowcę dla określonego ucznia.

# SELECT s.name AS Subject
# FROM assessments AS a
#     JOIN subjects AS s ON a.subject_id = s.id
#     JOIN students AS st ON a.student_id = st.id
# WHERE subject_id IN 
# (SELECT id FROM subjects WHERE lecturer_id = 1)
# AND student_id = 1
# GROUP BY Subject
# ORDER BY Subject ASC;

from sqlalchemy import select, and_
from connect_db import session
from models import Assessment, Subject, Student

def query_10():
    q = session.execute(
        select(Subject.name.label("Subject"))
        .select_from(Assessment)
        .join(Subject)
        .join(Student)
        .where(and_(
            Assessment.subject_id.in_(
            select(Subject.id).where(Subject.lecturer_id == 1)
            ),
            Assessment.student_id == 1
            ))
        .group_by(Subject)
        .order_by("Subject")
    ).mappings().all()
    return q

if __name__ == '__main__':
    print(query_10())