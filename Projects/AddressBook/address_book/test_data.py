from dataclasses import dataclass
from record import Record, Name, Phone, Email, Birthday, Address, Tag, Notes

@dataclass
class TestData:
    test_contacts = {
        1 : Record(Name("Karolina Nowak"), Phone("600 123 456"), Email("anowak@email.com"), Birthday("1985-10-20"), 
                    Address("Wroclaw, 50-234, ul. Trzebnicka 23/4"),
                    Tag("Okulista"), 
                    Notes("Przyjmuje od 8 do 16"),
                    ),
        2 : Record(Name("Piotr Wiśniewski"), Phone("512 987 654"), Email("pwisniewski@email.com"), Birthday("1992-03-07"),
                    Address("Warszawa, 00-001, ul. Kwiatowa 5/3"),
                    Tag("Mechanik"),
                    Notes(""),
                    ),
        3 : Record(Name("Anna Kowalczyk"), Phone("665 111 222"), Email("mkowalczyk@email.com"), Birthday("1988-07-12"),
                    Address("Kraków, 30-300, Aleja Słoneczna 7B"),
                    Tag("Kwiaciarnia"),
                    Notes("Piekne maja tulipany"),
                    ),
        4 : Record(Name("Kamil Lewandowski"), Phone("700 222 333"), Email("klewandowski@email.com"), Birthday("1995-01-30"),
                    Address("Gdańsk, 80-800, ul. Dębowa 22/8"),
                    Tag("Fryzjer"),
                    Notes("Dobre ceny"),
                    ),
        5 : Record(Name("Aleksandra Wójcik"), Phone("510 333 444"), Email("awojcik@email.com"), Birthday("1983-12-04"),
                    Address("Łódź, 90-090, Rondo Róży 3"),
                    Tag("Praca"),
                    Notes("Wspolpracownik"),
                    ),
        6 : Record(Name("Michał Kamiński"), Phone("730 444 555"), Email("mkaminski@email.com"), Birthday("1997-09-18"),
                    Address("Lublin, 20-200, ul. Leśna 15A"),
                    Tag("Koszykowka"),
                    Notes("Kumpel z podworka"),
                    ),
        7 : Record(Name("Karolina Jankowska"), Phone("602 555 666"), Email("kjankowska@email.com"), Birthday("1991-06-25"),
                    Address("Poznań, 60-600, Plac Morski 4/6"),
                    Tag("Praca"),
                    Notes("Manager"),
                    ),
        8 : Record(Name("Tomasz Zając"), Phone("516 666 777"), Email("tzajac@email.com"), Birthday("1980-04-09"),
                    Address("Olsztyn, 10-100, Aleja Zielona 12"),
                    Tag("Szkola"),
                    Notes("Nauczyciel od matematyki dziecka"),
                    ),
        9 : Record(Name("Natalia Szymańska"), Phone("660 777 888"), Email("nszymanska@email.com"), Birthday("1994-11-19"),
                    Address("Katowice, 40-400, ul. Słowackiego 9/2"),
                    Tag("Dentysta"),
                    Notes("Ciezko z terminami"),
                    ),
        10 : Record(Name("Marcin Dąbrowski"), Phone("780 888 999"), Email("mdabrowski@email.com"), Birthday("1987-08-03"),
                    Address("Szczecin, 70-700, Skwer Nadbrzeżny 18"),
                    Tag("Szkola"),
                    Notes("Wychowawca dziecka"),
                    ),
                    }
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
