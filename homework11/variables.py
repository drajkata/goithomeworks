DB_NAME = "school.db"
DB_SCRIPT = "school.sql"

NUMBER_SUBJECTS = 8
NUMBER_LECTURERS = 5
NUMBER_GROUPS = 3
NUMBER_STUDENTS = 50
NUMBER_ASSESSMENTS_PER_STUDENT = 20

QUERY_DICT = {
    "1" : ["query_1.sql", "Query 1: 5 uczniów z najwyższą średnią ocen ze wszystkich przedmiotów."],
    "2" : ["query_2.sql", "Query 2: Uczeń z najwyższą średnią ocen z wybranego przedmiotu."],
    "3" : ["query_3.sql", "Query 3: Średnia ocen w grupach dla wybranego przedmiotu."],
    "4" : ["query_4.sql", "Query 4: Średnia ocen dla wszystkich grup, uwzględniając wszystkie oceny."],
    "5" : ["query_5.sql", "Query 5: Przedmioty, które prowadzi wybrany wykładowca."],
    "6" : ["query_6.sql", "Query 6: Lista uczniów w wybranej grupie."],
    "7" : ["query_7.sql", "Query 7: Oceny uczniów w wybranej grupie z określonego przedmiotu."],
    "8" : ["query_8.sql", "Query 8: Średnia ocen wystawionych przez wykładowcę z danego przedmiotu."],
    "9" : ["query_9.sql", "Query 9: Lista kursów, na które uczęszcza uczeń."],
    "10" : ["query_10.sql", "Query 10: Lista kursów prowadzonych przez wybranego wykładowcę dla określonego ucznia."],
}

SUBJECTS_LIST = ["Mathematics", "Biology", "History", "Chemistry", "Literature", "Physics", "Art", "Physical Education"]