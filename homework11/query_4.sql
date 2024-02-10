-- Średnia ocen dla wszystkich grup, uwzględniając wszystkie oceny.

SELECT round(avg(assessment), 2) AS Average, g.name AS Name
FROM assessments AS a 
    JOIN students AS s ON a.student_id = s.id
    JOIN groups AS g ON s.group_id = g.id
GROUP BY s.group_id
ORDER BY Average DESC;