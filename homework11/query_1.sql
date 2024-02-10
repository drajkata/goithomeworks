-- 5 uczniów z najwyższą średnią ocen ze wszystkich przedmiotów.

SELECT round(avg(assessment),2) AS Average, s.name AS Name
FROM assessments AS a 
JOIN students AS s ON a.student_id = s.id
GROUP BY a.student_id
ORDER BY Average DESC
LIMIT 5;