from query_1 import query_1
from query_2 import query_2
from query_3 import query_3
from query_4 import query_4
from query_5 import query_5
from query_6 import query_6
from query_7 import query_7
from query_8 import query_8
from query_9 import query_9
from query_10 import query_10

NUMBER_SUBJECTS = 8
NUMBER_LECTURERS = 5
NUMBER_GROUPS = 3
NUMBER_STUDENTS = 50
NUMBER_ASSESSMENTS_PER_STUDENT = 20

QUERY_DICT = {
    "1" : [query_1, "Query 1: 5 uczniów z najwyższą średnią ocen ze wszystkich przedmiotów."],
    "2" : [query_2, "Query 2: Uczeń z najwyższą średnią ocen z wybranego przedmiotu."],
    "3" : [query_3, "Query 3: Średnia ocen w grupach dla wybranego przedmiotu."],
    "4" : [query_4, "Query 4: Średnia ocen dla wszystkich grup, uwzględniając wszystkie oceny."],
    "5" : [query_5, "Query 5: Przedmioty, które prowadzi wybrany wykładowca."],
    "6" : [query_6, "Query 6: Lista uczniów w wybranej grupie."],
    "7" : [query_7, "Query 7: Oceny uczniów w wybranej grupie z określonego przedmiotu."],
    "8" : [query_8, "Query 8: Średnia ocen wystawionych przez wykładowcę z danego przedmiotu."],
    "9" : [query_9, "Query 9: Lista kursów, na które uczęszcza uczeń."],
    "10" : [query_10, "Query 10: Lista kursów prowadzonych przez wybranego wykładowcę dla określonego ucznia."],
}

SUBJECTS_LIST = ["Mathematics", "Biology", "History", "Chemistry", "Literature", "Physics", "Art", "Physical Education"]