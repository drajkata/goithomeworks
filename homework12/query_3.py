# -- Średnia ocen w grupach dla wybranego przedmiotu.

# SELECT round(avg(assessment), 2) AS Average, g.name AS Name
# FROM assessments AS a 
#     JOIN students AS s ON a.student_id = s.id
#     JOIN groups AS g ON s.group_id = g.id
# WHERE a.subject_id = 1
# GROUP BY s.group_id
# ORDER BY Average DESC;

from sqlalchemy import select, func, desc
from connect_db import session
from models import Assessment, Student, Group

def query_3():
    q = session.execute(
        select(func.round(func.avg(Assessment.assessment), 2).label("Average"), Group.name.label("Name"))
        .select_from(Assessment)
        .join(Student)
        .join(Group)
        .where(Assessment.subject_id == 1)
        .group_by(Group)
        .order_by(desc("Average"))
    ).mappings().all()
    return q

if __name__ == '__main__':
    print(query_3())