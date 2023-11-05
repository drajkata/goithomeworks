# Napisz bota asystenta konsoli, który będzie rozpoznawał komendy wprowadzane z klawiatury i reagował zgodnie z wprowadzoną komendą.

# Bot asystent powinien być prototypem aplikacji asystenta. W pierwszym przybliżeniu, aplikacja asystenta powinna być w stanie pracować z książką kontaktów i kalendarzem. W tej pracy domowej skupimy się na interfejsie samego bota. Najprostszym i najwygodniejszym interfejsem na początkowym etapie rozwoju jest aplikacja konsolowa CLI (Command Line Interface). CLI jest dość proste w implementacji. Każdy CLI składa się z trzech głównych elementów:

# Parser poleceń. Jest to część odpowiedzialna za analizowanie ciągów wprowadzanych przez użytkownika, wyodrębnianie słów kluczowych i modyfikatorów poleceń z ciągu.
# Command handlers - zestaw funkcji, zwanych również handler, są one odpowiedzialne za bezpośrednie wykonywanie poleceń.
# Pętla żądanie-odpowiedź. Ta część aplikacji jest odpowiedzialna za odbieranie danych od użytkownika i zwracanie odpowiedzi z funkcji handler do użytkownika.
# Na pierwszym etapie nasz asystent bota musi być w stanie zapisać nazwę i numer telefonu, znaleźć numer telefonu według nazwy, zmienić zapisany numer telefonu i wyświetlić wszystkie zapisane rekordy w konsoli. Aby zaimplementować tę prostą logikę, użyjemy słownika. W słowniku będziemy przechowywać nazwę użytkownika jako klucz i numer telefonu jako wartość.

# Warunki
# Bot powinien znajdować się w nieskończonej pętli, czekając na polecenie użytkownika.
# Bot kończy pracę, jeśli jeżeli napotka “.”
# Bot nie jest wrażliwy na wielkość liter wprowadzanych poleceń.
# Bot przyjmuje komendy:
# "hello", odpowiada na konsoli "How can I help you?"
# "add ...". Za pomocą tego polecenia bot zapisuje nowy kontakt w swojej pamięci (na przykład w słowniku). Zamiast ..., użytkownik wprowadza nazwę i numer telefonu, zawsze oddzielone spacją.
# "zmień..." Za pomocą tego polecenia bot zapisuje nowy numer telefonu istniejącego kontaktu w pamięci. Zamiast ..., użytkownik wprowadza nazwę i numer telefonu, zawsze oddzielone spacją.
# "phone ...." To polecenie wyświetla numer telefonu dla określonego kontaktu w konsoli. Zamiast ..., użytkownik wprowadza nazwę kontaktu, którego numer ma zostać wyświetlony.
# "show all". To polecenie wyświetla wszystkie zapisane kontakty z numerami telefonów w konsoli.
# "good bye", "close", "exit" za pomocą dowolnej z tych komend bot kończy pracę po wyświetleniu w konsoli komunikatu "Good bye!".
# Wszystkie błędy wprowadzane przez użytkownika powinny być obsługiwane przy użyciu dekoratora input_error. Dekorator ten jest odpowiedzialny za zwracanie komunikatów takich jak "Wprowadź nazwę użytkownika", "Podaj nazwę i telefon" itp. Dekorator input_error musi obsługiwać wyjątki pojawiające się w funkcjach obsługi (KeyError, ValueError, IndexError) i zwracać użytkownikowi odpowiednią odpowiedź.
# Logika poleceń jest zaimplementowana w oddzielnych funkcjach, które przyjmują jeden lub więcej ciągów jako dane wejściowe i zwracają ciąg.
# Cała logika interakcji z użytkownikiem jest zaimplementowana w funkcji main, wszystkie print i input występują tylko tam.


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        # except Exception as e:
            # print(f"Error caught: {e} in function {func.__name__} with values {args}")
        except KeyError as e:
            return f"Username not provided or user not found. Try again.\n{str(e)}\n"
        except IndexError as e:
            return "Incorrect data has been entered. Try again.\n"
        except ValueError as e:
            return "I'm sorry, but I don't understand your request. Try again.\n"
    return wrapper

@input_error
def func_hello(*args):
    text = "How can I help you?\n"
    return text

@input_error
def func_exit(*args):
    text = "Good bye!\n"
    return text

@input_error
def func_add(args):
    user = ""
    value = "not specified"
    for arg in args:
        if arg.lower() not in OPERATIONS_MAP.keys() and not arg.isdigit():
            user += arg + " "
        if arg.isdigit():
            value = arg
    if len(user) > 0:
        key = user.removesuffix(" ")   
    elif len(user) == 0:
        raise KeyError("To add a user, enter the 'add' command, then enter the username and phone number, separating the information with a space.")
    CONTACTS[key] = value
    text = "User added successfully.\n"
    return text

@input_error
def func_change(args):
    user = ""
    value = "not specified"
    for arg in args:
        if arg.lower() not in OPERATIONS_MAP.keys() and not arg.isdigit():
            user += arg + " "
        if arg.isdigit():
            value = arg
    if len(user) > 0:
        key = user.removesuffix(" ")   
    elif len(user) == 0:
        raise KeyError("To change a user, enter the 'change' command, then enter the username and phone number, separating the information with a space.")
    CONTACTS[key] = value
    text = "User number successfully changed.\n"
    return text

@input_error
def func_phone(args):
    user = ""
    for arg in args:
        if arg.lower() not in OPERATIONS_MAP.keys() and not arg.isdigit():
            user += arg + " "
    if len(user) > 0:
        key = user.removesuffix(" ")   
    elif len(user) == 0:
        raise KeyError("To display a user's phone number, enter the command 'phone', then enter the username, separating the information with a space.")
    value = CONTACTS[key]
    text = f"{key}'s phone number is: {value}\n"
    return text

@input_error
def func_show(*args):
    text = ""
    for key, value in CONTACTS.items():
        text +=  f"{key}: {value}\n"
    if len(text) == 0:
        text = "The contact book is empty.\n"
    return text

OPERATIONS_MAP = {
    "hello" : func_hello,
    "add" : func_add,
    "change" : func_change,
    "phone" : func_phone,
    "show all" : func_show,
    "good bye" : func_exit,
    "close" : func_exit,
    "exit" : func_exit,
    "." : func_exit,
}

# I check which command I should execute
@input_error
def look_for_operation(words):
    command_not_found = True
    for command in OPERATIONS_MAP.keys():
        check_command = words.lower()
        if check_command.startswith(command):
            operation = OPERATIONS_MAP[command]
            command_not_found = False
    if command_not_found:
        raise ValueError 
    list_of_words = words.split(" ")
    # print(f"list_of_words: {list_of_words}")
    return operation(list_of_words)


CONTACTS = {}

if __name__ == '__main__':
    print("Hello! I am your virtual assistant.\n")
    while True:
        listen = input("Enter your command here: ")       
        operation = look_for_operation(listen)
        print(operation)
        if operation == "Good bye!\n":
            break