# Zadanie
# Musisz zaimplementować użyteczną funkcję, umożliwiającą wyświetlenie listy współpracowników, którym należy złożyć życzenia z okazji ich urodzin w tym tygodniu.
# Masz listę słowników users, każdy słownik zawiera klucze name i birthday. Jest to struktura reprezentująca model listy użytkowników z ich imionami i datami urodzin. name jest ciągiem znaków z imieniem użytkownika, a birthday jest obiektem datetime z datą urodzin.
# Twoim zadaniem jest napisanie funkcji get_birthdays_per_week, która pobiera listę users jako dane wejściowe i wyświetla na konsoli listę użytkowników (używając funkcji print), którym należy złożyć życzenia według dnia.
# Warunki akceptacji:
# - get_birthdays_per_week wyświetla osoby obchodzące urodziny w formacie:
    # Monday: Bill, Jill
    # Friday: Kim, Jan
# - Użytkownicy, których urodziny wypadły w weekend, powinni dostać życzenia w poniedziałek
# - Dla celów debugowania, wygodnie jest utworzyć testową listę users i wypełnić ją samodzielnie.
# - Funkcja wyświetla użytkowników obchodzących urodziny tydzień przed bieżącym dniem.
# - Tydzień zaczyna się w poniedziałek.

from datetime import datetime, timedelta
from collections import defaultdict

days_in_week = {
    0 : "Monday",
    1 : "Tuesday",
    2 : "Wednesday",
    3 : "Thursday",
    4 : "Friday",
    5 : "Saturday",
    6 : "Sunday",
}

def get_birthdays_per_week(users):
    global days_in_week
    
    current_datetime = datetime.now()
    # MY TESTS WITH CURRENT DATA
    # current_datetime = datetime(year=2023, month=12, day=29)
    # current_datetime = datetime(year=2024, month=1, day=1)
    # print(f"Current date: {current_datetime.date()}, Current week: {current_datetime_week}\n")

    current_month = current_datetime.month
    current_datetime_week = current_datetime.strftime("%W")

    birthday_this_week = []
    birthday_next_week = []
    
    for user in users:
        birthday = user["birthday"]
        birthday_month = birthday.month
        birthday_day = birthday.day

        if birthday_month < current_month:
            current_year = current_datetime.year + 1
        else:
            current_year = current_datetime.year

        birthday_in_this_year = datetime(year = current_year, month = birthday_month, day = birthday_day)
        birthday_in_this_year_in_working_week = None

        if birthday_in_this_year.weekday() == 5:
            birthday_in_this_year_in_working_week = birthday_in_this_year + timedelta(days = 2)
        elif birthday_in_this_year.weekday() == 6:
            birthday_in_this_year_in_working_week = birthday_in_this_year + timedelta(days = 1)
        else:
            birthday_in_this_year_in_working_week = birthday_in_this_year
        
        one_week_interval = timedelta(weeks = 1)
        reminder_date = birthday_in_this_year_in_working_week - one_week_interval
        reminder_week = reminder_date.strftime("%W")

        birthday_in_working_weekday = birthday_in_this_year_in_working_week.weekday()
        birthday_in_working_week = birthday_in_this_year_in_working_week.strftime("%W")

        # # Supporting dictionary list to group information
        # birthday_list.append({
        #     "name" : user["name"],
        #     "birthday" : birthday_in_this_year,
        #     "birthday_working_week" : birthday_in_this_year_in_working_week,
        #     "birthday_in_working_week" : birthday_in_working_week,
        #     "birthday_in_working_weekday" : birthday_in_working_weekday,
        #     "reminder" : reminder_date,
        #     "reminder_week" : reminder_week,
        #     })
        
        # # Supporting information about the user to test
        # print(f"User: {user['name']}, Birthday: {birthday_in_this_year_in_working_week.date()}, Birthday-week: {birthday_in_working_week}, Reminder: {reminder_date.date()}, Reminder-week: {reminder_week}")
        
        # Adding people to the results list
        if current_datetime_week == reminder_week:
            birthday_next_week.append([user["name"], birthday_in_working_weekday])
        if current_datetime_week == birthday_in_working_week:
            birthday_this_week.append([user["name"], birthday_in_working_weekday])

    # Display information about birthdays:
    # - next week:
    if birthday_next_week:
        print(f"They celebrate their birthdays next week:")
        grouped_users_birthday_next_week = defaultdict(list)
        for user in birthday_next_week:
            grouped_users_birthday_next_week[user[1]].append(user[0])
        list_grouped_users_birthday_next_week = list(grouped_users_birthday_next_week.items())
        for element in list_grouped_users_birthday_next_week:
            names = ""
            for name in element[1]:
                names += name + ", "
            names = names.removesuffix(", ")
            print(f"{days_in_week[element[0]]}: {names}")
    else:
        print("No one is celebrating a birthday next week.")
    # - this week
    if birthday_this_week: 
        print(f"\nThey celebrate their birthdays this week:")
        grouped_users_birthday_this_week = defaultdict(list)
        for user in birthday_this_week:
            grouped_users_birthday_this_week[user[1]].append(user[0])
        list_grouped_users_birthday_this_week = list(grouped_users_birthday_this_week.items())
        for element in list_grouped_users_birthday_this_week:
            names = ""
            for name in element[1]:
                names += name + ", "
            names = names.removesuffix(", ")
            print(f"{days_in_week[element[0]]}: {names}")
    else:
        print(f"\nNo one is celebrating a birthday this week.")

# # MY TEST DATA
# my_users = [
#     {"name" : "Monika", "birthday" : datetime(year=1960, month=12, day=31)},
#     {"name" : "Ania", "birthday" : datetime(year = 1974, month=1, day=2)},
#     {"name" : "Krzysztof", "birthday" : datetime(year = 1983, month=11, day=1)},
# ]
# get_birthdays_per_week(my_users)