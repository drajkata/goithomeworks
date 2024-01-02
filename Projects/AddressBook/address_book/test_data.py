from dataclasses import dataclass
from record import Record

@dataclass
class TestData:
    test_contacts = {
        1 : Record("Karolina Nowak", "600 123 456", "anowak@email.com", "1985-10-20", 
                    "Wroclaw, 50-234, ul. Trzebnicka 23/4",
                    "Okulista", 
                    "Przyjmuje od 8 do 16"
                    ),
        2 : Record("Piotr Wiśniewski", "512 987 654", "pwisniewski@email.com", "1992-03-07",
                    "Warszawa, 00-001, ul. Kwiatowa 5/3",
                    "Mechanik",
                    "",
                    ),
        3 : Record("Anna Kowalczyk", "665 111 222", "mkowalczyk@email.com", "1988-07-12",
                    "Kraków, 30-300, Aleja Słoneczna 7B",
                    "Kwiaciarnia",
                    "Piekne maja tulipany",
                    ),
        4 : Record("Kamil Lewandowski", "700 222 333", "klewandowski@email.com","1995-01-30",
                    "Gdańsk, 80-800, ul. Dębowa 22/8",
                    "Fryzjer",
                    "Dobre ceny",
                    ),
        5 : Record("Aleksandra Wójcik", "510 333 444", "awojcik@email.com", "1983-12-04",
                    "Łódź, 90-090, Rondo Róży 3",
                    "Praca",
                    "Wspolpracownik",
                    ),
        6 : Record("Michał Kamiński","730 444 555","mkaminski@email.com", "1997-09-18",
                    "Lublin, 20-200, ul. Leśna 15A",
                    "Koszykowka",
                    "Kumpel z podworka",
                    ),
        7 : Record("Karolina Jankowska", "602 555 666", "kjankowska@email.com", "1991-06-25",
                    "Poznań, 60-600, Plac Morski 4/6",
                    "Praca",
                    "Manager",
                    ),
        8 : Record("Tomasz Zając", "516 666 777", "tzajac@email.com", "1980-04-09",
                    "Olsztyn, 10-100, Aleja Zielona 12",
                    "Szkola",
                    "Nauczyciel od matematyki dziecka",
                    ),
        9 : Record("Natalia Szymańska", "660 777 888", "nszymanska@email.com", "1994-11-19",
                    "Katowice, 40-400, ul. Słowackiego 9/2",
                    "Dentysta",
                    "Ciezko z terminami",
                    ),
        10 : Record("Marcin Dąbrowski", "780 888 999", "mdabrowski@email.com", "1987-08-03",
                    "Szczecin, 70-700, Skwer Nadbrzeżny 18",
                    "Szkola",
                    "Wychowawca dziecka",
                    )
                    }
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
