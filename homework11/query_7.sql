-- Oceny uczniów w wybranej grupie z określonego przedmiotu.

SELECT a.assessment AS Assesment, s.name AS Name
FROM assessments AS a
    JOIN students AS s ON a.student_id = s.id
WHERE subject_id = 1 AND s.group_id = 1;