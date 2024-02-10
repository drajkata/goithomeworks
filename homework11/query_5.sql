-- Przedmioty, które prowadzi wybrany wykładowca.

SELECT name AS Subject
FROM subjects
WHERE lecturer_id = 1;