-- Średnia ocen w grupach dla wybranego przedmiotu.

SELECT round(avg(assessment),2) AS Average, g.name AS Name
FROM assessments AS a 
    JOIN students AS s ON a.student_id = s.id
    JOIN groups AS g ON s.group_id = g.id
WHERE a.subject_id = 1
GROUP BY s.group_id
ORDER BY Average DESC;