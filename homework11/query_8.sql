-- Średnia ocen wystawionych przez wykładowcę z danego przedmiotu.

SELECT round(avg(assessment),2) AS Average, s.name AS Subject 
FROM assessments AS a
    JOIN subjects AS s ON a.subject_id = s.id
WHERE subject_id IN
(SELECT id FROM subjects WHERE lecturer_id = 1)
GROUP BY subject_id
ORDER BY Average DESC;