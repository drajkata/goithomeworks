# -- Oceny uczniów w wybranej grupie z określonego przedmiotu.

# SELECT a.assessment AS Assesment, s.name AS Name
# FROM assessments AS a
#     JOIN students AS s ON a.student_id = s.id
# WHERE subject_id = 1 AND s.group_id = 1;

from sqlalchemy import select, and_
from connect_db import session
from models import Assessment, Student

def query_7():
    q = session.execute(
        select(Assessment.assessment.label("Assessment"), Student.name.label("Name"))
        .join(Student)
        .where(
            and_(
                Assessment.subject_id == 1,
                Student.group_id == 1
            ))
    ).mappings().all()
    return q

if __name__ == '__main__':
    print(query_7())