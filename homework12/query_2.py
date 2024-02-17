# -- Uczeń z najwyższą średnią ocen z wybranego przedmiotu.

# SELECT round(avg(assessment),2) AS Average, s.name AS Name
# FROM assessments AS a 
#     JOIN students AS s on a.student_id = s.id
# WHERE a.subject_id = 1
# GROUP BY a.student_id
# ORDER BY Average DESC
# LIMIT 1;

from sqlalchemy import select, func, desc
from connect_db import session
from models import Assessment, Student

def query_2():
    q = session.execute(
        select(func.round(func.avg(Assessment.assessment), 2).label("Average"), Student.name.label("Name"))
        .where(Assessment.subject_id == 1)
        .join(Student)
        .group_by(Student)
        .order_by(desc("Average"))
    ).first()
    return q

if __name__ == '__main__':
    print(query_2())


