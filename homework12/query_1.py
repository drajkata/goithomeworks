# 5 uczniów z najwyższą średnią ocen ze wszystkich przedmiotów.

# SELECT round(avg(assessment),2) AS Average, s.name AS Name
# FROM assessments AS a 
# JOIN students AS s ON a.student_id = s.id
# GROUP BY a.student_id
# ORDER BY Average DESC
# LIMIT 5;

from sqlalchemy import select, func, desc
from connect_db import session
from models import Assessment, Student

def query_1():
    q = session.execute(
        select(func.round(func.avg(Assessment.assessment), 2).label("Average"), Student.name.label("Name"))
        .join(Student)
        .group_by(Student)
        .order_by(desc("Average"))
        .limit(5)
    ).mappings().all()
    return q

if __name__ == '__main__':
    print(query_1())