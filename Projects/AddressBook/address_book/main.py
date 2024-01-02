from address_book import AddressBook
from record import Name, Phone, Email, Birthday, Address, Tag, Notes
# from view import display_contacts
import view

from thefuzz import fuzz


def clossest_match(querry: str, commands):
    """filters commands if they start with querry,
    if no command found querry is shortened by one char from the end
    and function tries again (recursively)"""
    if len(querry) == 0:
        return []
    matched_commands = list(filter(lambda x: x.startswith(querry), commands))
    if len(matched_commands) > 0:
        return matched_commands
    else:
        return clossest_match(querry[:-1], commands)


def command_hint(user_str: str, commands, threshold: int = 0) -> str:
    """return string with hint for user describing
    closest match to the available bot commands"""
    user_str = user_str.strip()
    hint = ""
    # for short string use startwith
    if len(user_str) <= 3:
        hits = clossest_match(user_str, commands)
    else:  # for longer strings use fuzzy string matching
        # calculate similarity scores for each command
        # ratio
        # scores = [fuzz.ratio(user_str, command) for command in commands]
        # partial
        # print(commands)
        scores = [fuzz.partial_ratio(user_str, command) for command in commands]

        # threshold = 0
        scores = list(filter(lambda x: x >= threshold, scores))
        # print(scores)
        # find best score
        best_score = max(scores)
        # print(best_score)
        # find all commands with best scores
        hits = [
            command for score, command in zip(scores, commands) if score == best_score
        ]
        # print(hits)

    if len(hits) > 0:
        hint = f"Did you mean?: {', '.join(hits)}"
    return hint

def input_error(func):
        def wrapper(*args):
            try:
                return func(*args)
            except KeyError as e:
                print(
                    f"Username not provided or user not found. Try again.\nError details: {str(e)}\n"
                )
            except IndexError as e:
                print(
                    f"Incorrect data has been entered. Try again.\nError details: {str(e)}\n"
                )
            except ValueError as e:
                print(
                    f"I'm sorry, but I don't understand your request. Try again.\nError details: {str(e)}\n"
                )
            # except Exception as e:
            #     print(f"Error caught: {e} in function {func.__name__} with values {args}")

        return wrapper


############################################################################  
#### HELLO / HELP FUNCTION
    
def hello():
    print(
        """
       db        88    ad88                                88  
      d88b       88   d8\"                                  88  
     d8\'`8b      88   88                                   88  
    d8\'  `8b     88 MM88MMM 8b,dPPYba,  ,adPPYba,  ,adPPYb,88  
   d8YaaaaY8b    88   88    88P\'   \"Y8 a8P_____88 a8\"    `Y88  
  d8\"\"\"\"\"\"\"\"8b   88   88    88         8PP\"\"\"\"\"\"\" 8b       88  
 d8\'        `8b  88   88    88         \"8b,   ,aa \"8a,   ,d88  
d8\'          `8b 88   88    88          `\"Ybbd8\"\'  `\"8bbdP\"Y8 

Hello! I am your virtual assistant.
To find out what can I do for you enter "help" command."""
    )

def help(object):
    object.help()

############################################################################      
### SHOW FUNCTIONS

@input_error
def show_all_contacts(object):view.display_contacts(view.ViewContacts(), object.show())

@input_error
def show_few_contacts(object):
    iter = None
    new_counting = True
    try:
        number_of_contacts = int(input("Enter number of contacts to display: "))
    except ValueError:
        print("Entered number is not an integer. Please try again.")
    while True:        
        page, iter, contacts, is_last = object.show_per_page(number_of_contacts, new_counting, iter)
        new_counting = False 
        print(f"\nPAGE {page}")
        view.display_contacts(view.ViewContacts(), contacts)
        if is_last:
            print("\nI've displayed all contacts from the Address Book.")
            break
        else:
            choice = input(
                f"\nDo you want to display next {number_of_contacts} contact(s)? (Y/N) "
            )
            if choice not in ["y", "Y", "Yes", "yes", "True"]:
                break 
 
@input_error
def show_all_notes(object): view.display_contacts(view.ViewNotes(), object.show())

############################################################################      
### SEARCH FUNCTIONS

@input_error
def find_contact(object):
    contact_name = input("Which contact do you want to display (enter name)?: ")
    view.display_contacts(view.ViewContact(), object.find(contact_name))

@input_error
def search(object):
    keyword = input("Enter keyword: ")
    view.display_contacts(view.ViewContacts(), object.search(keyword))


############################################################################  
#### ADD FUNCTION

@input_error
def add_operation(object):
    to_add = True
    print("\nPlease complete the information below. Name is mandatory, but the rest you can skip by clicking Enter.")
    name = Name(input("\nEnter name*: "))
    contacts = object.check_if_object_exists(name)
    if len(contacts) > 0:
        print("\nI've found in the Address Book the contact(s) with the same name:")
        view.display_contacts(view.ViewContacts(), contacts)
        choice = None
        choice = input("\nWould you like to update the contact? (Y/N): ")
        if choice in ["y", "Y", "Yes", "yes", "True"]:
            to_add = False
            if len(contacts) > 1:
                while True:
                    number = None
                    number = int(input("\nPlease enter the ID number of the contact you want to update: "))
                    if number in contacts.keys():
                        break
                    else:
                        print("\nSorry, but I couldn't find any contacts with this ID. Try again...\n")
                key = number
                value = contacts[number]
            else:
                key = list(contacts.keys())[0]
                value = list(contacts.values())[0]
            print("\nComplete the information below that you want to update or skip by clicking Enter.")
        else:
            print(f"\nContinue entering the information for new contact: {name.value}\n")
    phone = Phone(input("Enter new phone: "))
    email = Email(input("Enter new email: "))
    birthday = Birthday(input("Enter new birthday: "))
    address = Address(input("Enter new address: "))
    tag = Tag(input("Enter new tag: "))
    notes = Notes(input("Enter new notes: "))
    if object.check_entered_values(name, phone, email, birthday, address, tag, notes):
        if to_add:   
            new_contact = object.add(name, phone, email, birthday, address, tag, notes)
            object.save_data()
            view.display_contacts(view.ViewContacts(), new_contact)
        else:
            obj_updated = object.edit(value, name, phone, email, birthday, address, tag, notes)
            object.save_data()
            results_to_display = {}
            results_to_display[key] = obj_updated
            view.display_contacts(view.ViewContacts(), results_to_display)
    else:
        print("\nYou did not enter any data to change the contact information. Please try again.")
    
############################################################################  
#### EDIT FUNCTION

@input_error
def edit_operation(object):
    contact_name = input("Which contact do you want to update (enter name)?: ")
    contacts = object.check_if_object_exists(contact_name)
    if len(contacts) == 0:
            view.display_contacts(view.ViewContacts(), contacts)
    else:
        print("\nI've found in the Address Book the contact(s) with the same name:")
        view.display_contacts(view.ViewContacts(), contacts)
        if len(contacts) > 1:
            while True:
                number = None
                number = int(input("\nPlease enter the ID number of the contact you want to update: "))
                if number in contacts.keys():
                    break
                else:
                    print("\nSorry, but I couldn't find any contacts with this ID. Try again...")
            key = number
            value = contacts[number]
        else:
            key = list(contacts.keys())[0]
            value = list(contacts.values())[0]
        print("\nComplete the information below that you want to update or skip by clicking Enter.\n")
        name = Name(input("Enter new name: "))
        phone = Phone(input("Enter new phone: "))
        email = Email(input("Enter new email: "))
        birthday = Birthday(input("Enter new birthday: "))
        address = Address(input("Enter new address: "))
        tag = Tag(input("Enter new tag: "))
        notes = Notes(input("Enter new notes: "))
        if object.check_entered_values(name, phone, email, birthday, address, tag, notes):
            obj_updated = object.edit(value, name, phone, email, birthday, address, tag, notes)
            object.save_data()
            results_to_display = {}
            results_to_display[key] = obj_updated
            view.display_contacts(view.ViewContacts(), results_to_display)
        else:
            print("\nYou did not enter any data to change the contact information. Please try again.")

############################################################################  
#### DELETE FUNCTION

@input_error
def delete_operation(object):
    attributes = ['contact', 'phone', 'email', 'birthday', 'address', 'tag', 'notes']
    print("\nOf course! Please enter, what would you like to delete:\n'contact', 'phone', 'email', 'birthday', 'address', 'tag', 'notes'")
    while True:
        attribute = input("\nYour choice: ")
        attribute_to_delete = attribute.lower().strip()
        if attribute_to_delete in attributes:
            break
        print("\nPlease enter the correct command.")
    contact_name = input("\nPlease enter name of the contact?: ")
    contacts = object.check_if_object_exists(contact_name)
    if len(contacts) == 0:
            view.display_contacts(view.ViewContacts(), contacts)
    else:
        if len(contacts) > 1:
            print("\nI've found in the Address Book the contact(s):")
            view.display_contacts(view.ViewContacts(), contacts)
            while True:
                number = None
                number = int(input("\nPlease enter the ID number of the contact: "))
                if number in contacts.keys():
                    id = number
                    break
                else:
                    print("\nSorry, but I couldn't find any contacts with this ID. Try again...")
        else:    
            id = list(contacts.keys())[0]
        choice = None
        choice = input("\nWould you like to delete the contact? (Y/N): ")
        if choice in ["y", "Y", "Yes", "yes", "True"]:
            object.delete(id, attribute_to_delete)
            object.save_data()
            print(f"\nThe operation was successful for contact: {contact_name} with id: {id}")
        else:
            print("\nI took no action.")

############################################################################  
#### BIRTHDAY FUNCTIONS  

@input_error
def contact_birthday(object):
    contact_name = input("Which contact's birthday do you want to display (enter name)?: ")
    view.display_contacts(view.ViewContactBirthday(), object.birthday(contact_name))

@input_error
def contacts_upcoming_birthday(object):
    days = input("\nFind out who will be celebrating their birthday in the near future!\nHow many days in advance would you like to see your contacts' upcoming birthdays?\n\nEnter number of days: ")
    today = {}
    upcoming = {}
    list_of_dict = []
    list_of_dict = object.upcoming_birthdays(days)  
    today = list_of_dict[0]
    upcoming = list_of_dict[1]

    if not any(today) and not any(upcoming):
            print(f"\nNone of your contacts have upcoming birthdays in this period.")
    else:
        print(
            "   O O O O \n" "  _|_|_|_|_\n" " |         |\n",
            "|         |\n",
            "|_________|\n",
        )
    if any(today):
        print("\nSomeone has birthday today, so wish 'HAPPY BIRTHDAY' today to: ")
        view.display_contacts(view.ViewContacts(), today)
    if any(upcoming):
        print("\nSend birthday wishes to your contact on the upcoming days:")
        view.display_contacts(view.ViewContacts(), upcoming)

############################################################################  
#### EXIT FUNCTION

def end_program(object):
    object.save_data()
    print("""
                                           ..::::------:::..                                           
                                 .:-=+*#%@@@@@@@@@@@@@@@@@@@@%##*+=:.                                  
                            :-+#%@@@@@@@@@@@@%%##******##%%@@@@@@@@@@@#*=:                             
                        :+#@@@@@@@%#*+=-:..                 ..:-=+*%@@@@@@@#+-.                        
                    .=*@@@@@@#+=:                                    :-+#@@@@@@#=.                     
                  -#@@@@@#=:    .-=*:        -.         =         =+-:    :=*%@@@@#=.                  
               :*@@@@%+-    :=*%@@@=         +%:      .*@:        .#@@@#+-.   :=#@@@@#-                
             -#@@@%+:   :+#@@@@@@@+          #@@#*****@@@-         .%@@@@@@#+:   .=%@@@%=              
           :#@@@#-   :+%@@@@@@@@@#           %@@@@@@@@@@@=          -@@@@@@@@@%+:   :*@@@%=            
         .*@@@#-   -#@@@@@@@@@@@@:           @@@@@@@@@@@@*           #@@@@@@@@@@@#-   :*@@@#:          
        :%@@%-   -%@@@@@@@@@@@@@%           .@@@@@@@@@@@@#           =@@@@@@@@@@@@@%-   :#@@@=         
       =@@@*.  .#@@@@@@@@@@@@@@@#           -@@@@@@@@@@@@@           -@@@@@@@@@@@@@@@#.   +@@@*        
      =@@@=   -@@@@@@@@@@@@@@@@@%           =@@@@@@@@@@@@@:          +@@@@@@@@@@@@@@@@@-   -%@@*       
     =@@@=   +@@@@@@@@@@@@@@@@@@@-          %@@@@@@@@@@@@@=          %@@@@@@@@@@@@@@@@@@+   :%@@*      
    :@@@=   =@@@@@@@@@@@@@@@@@@@@%.        =@@@@@@@@@@@@@@@:        *@@@@@@@@@@@@@@@@@@@@=   :@@@-     
    #@@#   :@@@@@@@@@@@@@@@@@@@@@@%-      +@@@@@@@@@@@@@@@@%-     :#@@@@@@@@@@@@@@@@@@@@@@:   +@@%     
   .@@@:   *@@@@@@@@@@@@@@@@@@@@@@@@%*==*%@@@@@@@@@@@@@@@@@@@%*+*#@@@@@@@@@@@@@@@@@@@@@@@@*   .@@@=    
   =@@%    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    *@@*    
   +@@#   .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.   +@@%    
   +@@#   .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    Good bye!    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.   +@@%    
   =@@@    %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%    *@@*    
   .@@@-   =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=   .@@@=    
    *@@#    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#    +@@%     
    .@@@+    *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.   :@@@-     
     -@@@=    -%@@@@@@@@@@=.   :=#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+-:.:=%@@@@@@@@@@#.   :%@@+      
      =@@@=    .*@@@@@@@@-        :#@@@@@*==*%@@@@@@@@@@@%*++%@@@@@*:       .%@@@@@@@@=    -@@@*       
       =@@@*.    :*@@@@@@.          =@@%:     =@@@@@@@@%-     +@@%-          +@@@@@@*.    +@@@+        
        :%@@%=     :*@@@@=           :%:       .%@@@@@#.       *%.           #@@@@*:    -%@@@=         
         .+@@@%-     .+%@%.                     .%@@@#         ..           :@@%+.    :#@@@#.          
           :#@@@%=.     :+*.                     :@@@:                     .#+-     -#@@@%-            
             :#@@@@*:                             +@+                      .     :+%@@@%=              
               :+@@@@%+-                          .%.                         :+%@@@@*-                
                  -*@@@@@#=:                       :                      :=*@@@@@#=.                  
                    .-*%@@@@@#*=:.                                   :-+#@@@@@@*=.                     
                        :=*%@@@@@@@#*+=-::.                ..:-=+*#%@@@@@@@#+:                         
                            .-+*%@@@@@@@@@@@@%%%#######%%%@@@@@@@@@@@%#+-:                             
                                  :-=+*#%%@@@@@@@@@@@@@@@@@@%%#*+=-:.                                  
                                           ...::------:::.                      
""")
    exit()

############################################################################  
#### MAIN FUNCTION

def main():
    
    hello()
    contact = AddressBook()
    contact.read_data()
    
    OPERATION_FUNCTIONS = {
        "help": help,
        "find": find_contact,
        "show all": show_all_contacts,
        "show": show_few_contacts,
        "show notes": show_all_notes,
        "search": search,
        "birthday": contact_birthday,
        "upcoming birthdays": contacts_upcoming_birthday,
        "add" : add_operation,
        "edit" : edit_operation,
        "delete" : delete_operation,
        "good bye" : end_program, 
        "close" : end_program,
        "exit" : end_program,
        "." : end_program,
    }

    while True:
        listen = input("\nEnter your command here: ")
        command = listen.lower().strip()

        if command in OPERATION_FUNCTIONS:
            OPERATION_FUNCTIONS[command](contact)       
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
