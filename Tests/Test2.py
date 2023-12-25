kontakty = {
    'Anna Kowalska': {'telefon': '123456789', 'email': 'anna@example.com'},
    'Jan Nowak': {'telefon': '987654321', 'email': 'jan@example.com'},
    'Ewa Wiśniewska': {'telefon': '555666777', 'email': 'ewa@example.com'}
}

posortowane_kontakty = dict(sorted(kontakty.items(), key=lambda x: x[0]))

for nazwa, dane in posortowane_kontakty.items():
    print(nazwa, "->", dane)