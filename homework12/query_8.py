# -- -- Średnia ocen wystawionych przez wykładowcę z danego przedmiotu.

# -- SELECT round(avg(assessment),2) AS Average, s.name AS Subject 
# -- FROM assessments AS a
# --     JOIN subjects AS s ON a.subject_id = s.id
# -- WHERE subject_id IN
# -- (SELECT id FROM subjects WHERE lecturer_id = 1)
# -- GROUP BY subject_id
# -- ORDER BY Average DESC;

from sqlalchemy import select, func, desc
from connect_db import session
from models import Assessment, Student, Group, Subject

def query_8():
    q = session.execute(
        select(func.round(func.avg(Assessment.assessment), 2).label("Average"), Subject.name.label("Name"))
        .select_from(Assessment)
        .join(Student)
        .join(Subject)
        .where(Assessment.subject_id.in_(
            select(Subject.id).where(Subject.lecturer_id == 1)
            ))
        .group_by(Assessment.subject_id)
        .order_by(desc("Average"))
    ).mappings().all()
    return q

if __name__ == '__main__':
    print(query_8())