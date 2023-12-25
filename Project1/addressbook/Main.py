from DataPresentation import ContactNotFound
from AddressBook import AddressBook
from Record import Record, Name, Phone, Email, Birthday, Address, Tag, Notes
import DataPresentation

# from thefuzz import fuzz


# def clossest_match(querry: str, commands):
#     """filters commands if they start with querry,
#     if no command found querry is shortened by one char from the end
#     and function tries again (recursively)"""
#     if len(querry) == 0:
#         return []
#     matched_commands = list(filter(lambda x: x.startswith(querry), commands))
#     if len(matched_commands) > 0:
#         return matched_commands
#     else:
#         return clossest_match(querry[:-1], commands)


# def command_hint(user_str: str, commands, threshold: int = 0) -> str:
#     """return string with hint for user describing
#     closest match to the available bot commands"""
#     user_str = user_str.strip()
#     hint = ""
#     # for short string use startwith
#     if len(user_str) <= 3:
#         hits = clossest_match(user_str, commands)
#     else:  # for longer strings use fuzzy string matching
#         # calculate similarity scores for each command
#         # ratio
#         # scores = [fuzz.ratio(user_str, command) for command in commands]
#         # partial
#         # print(commands)
#         scores = [fuzz.partial_ratio(user_str, command) for command in commands]

#         # threshold = 0
#         scores = list(filter(lambda x: x >= threshold, scores))
#         # print(scores)
#         # find best score
#         best_score = max(scores)
#         # print(best_score)
#         # find all commands with best scores
#         hits = [
#             command for score, command in zip(scores, commands) if score == best_score
#         ]
#         # print(hits)

#     if len(hits) > 0:
#         hint = f"Did you mean?: {', '.join(hits)}"
#     return hint

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
            except ContactNotFound as e:
                print(f"Contact not found.")
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
    object.func_help()

############################################################################      
### SHOW FUNCTIONS

@input_error
def show_all_contacts(object): DataPresentation.pretty_view_contacts(object.func_show_all())

@input_error
def show_few_contacts(object):
    try:
        number_of_contacts = int(input("Enter number of contacts to display: "))
        DataPresentation.pretty_view_contacts(object.func_show(number_of_contacts))
    except ValueError:
        print("Entered number is not an integer. Please try again.")

@input_error
def show_all_notes(object): DataPresentation.pretty_view_notes(object.func_show_notes())

############################################################################      
### SEARCH FUNCTIONS

@input_error
def find_contact(object):
    contact_name = input("Which contact do you want to display (enter name)?: ")
    DataPresentation.pretty_view_contacts(object.func_find(contact_name))

@input_error
def search(object):
    keyword = input("Enter keyword: ")
    DataPresentation.pretty_view_contacts(object.func_search(keyword))

############################################################################  
#### ADD FUNCTIONS

@input_error
def add(object):
    name = Name(input("Enter name: "))
    phone = Phone(input("Enter phone: "))
    email = Email(input("Enter email: "))
    birthday = Birthday(input("Enter birthday: "))
    address = Address(input("Enter address: "))
    tag = Tag(input("Enter tag: "))
    notes = Notes(input("Enter notes: "))
    object.add_contact(name, phone, email, birthday, address, tag, notes)
    object.save_to_file()

############################################################################  
#### EDIT FUNCTIONS

@input_error
def edit(object):
    contact_name = input("Which contact do you want to update (enter name)?: ")
    contacts = object.check_if_object_exists(contact_name)
    if len(contacts) == 0:
            raise ContactNotFound
    else:
        print("\nI've found in the Address Book the contact(s) with the same name:")
        DataPresentation.pretty_view_contacts(contacts)
        choice = None
        choice = input("\nWould you like to update the contact(s) with the information you entered? (Y/N): ")
        if choice in ["y", "Y", "Yes", "yes", "True"]:
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
            print("\nComplete the information below that you want to update or skip by clicking Enter.")
            name = Name(input("\nEnter new name: "))
            phone = Phone(input("Enter new phone: "))
            email = Email(input("Enter new email: "))
            birthday = Birthday(input("Enter new birthday: "))
            address = Address(input("Enter new address: "))
            tag = Tag(input("Enter new tag: "))
            notes = Notes(input("Enter new notes: "))
            if object.check_entered_values(name, phone, email, birthday, address, tag, notes):
                new_obj = object.edit_contact(contacts[number], name, phone, email, birthday, address, tag, notes)
                object.save_to_file()
                results_to_display = {}
                results_to_display[key] = new_obj
                DataPresentation.pretty_view_contacts(results_to_display)
            else:
                print("\nI've found in the Address Book the contact(s) with the same name, but you did not enter any data to change the contact information. Please try again.")
        

############################################################################  
#### DELETE FUNCTIONS

@input_error
def delete_contact(object):
    contact_name = input("Which contact do you want to delete (enter name)?: ")
    object.func_delete_contact(contact_name)
    object.save_to_file()

@input_error    
def delete_contact_phone(object):
    contact_name = input("Which contact's phone do you want to delete (enter name)?: ")
    object.func_delete_phone(contact_name)
    object.save_to_file()

@input_error
def delete_contact_email(object):
    contact_name = input("Which contact's email do you want to delete (enter name)?: ")
    object.func_delete_email(contact_name)
    object.save_to_file()

@input_error
def delete_contact_birthday(object):
    contact_name = input("Which contact's birthday do you want to delete (enter name)?: ")
    object.func_delete_birthday(contact_name)
    object.save_to_file()

@input_error
def delete_contact_address(object):
    contact_name = input("Which contact's address do you want to delete (enter name)?: ")
    object.func_delete_address(contact_name)
    object.save_to_file()

@input_error
def delete_contact_tag(object):
    contact_name = input("Which contact's tag do you want to delete (enter name)?: ")
    object.func_delete_tag(contact_name)
    object.save_to_file()

@input_error
def delete_contact_notes(object):
    contact_name = input("Which contact's notes do you want to delete (enter name)?: ")
    object.func_delete_notes(contact_name)
    object.save_to_file()

############################################################################  
#### BIRTHDAY FUNCTIONS  

@input_error
def contact_birthday(object):
    contact_name = input("Which contact's birthday do you want to display (enter name)?: ")
    object.func_birthday(contact_name)

@input_error
def contacts_upcoming_birthday(object):
    days = input("\nFind out who will be celebrating their birthday in the near future!\nHow many days in advance would you like to see your contacts' upcoming birthdays?\nEnter number of days: ")
    object.func_upcoming_birthdays(days)  

############################################################################  
#### EXIT FUNCTION

def end_program(object):
    object.save_to_file()
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
    contact.read_from_file()
    
    OPERATION_FUNCTIONS = {
        "help": help,
        "find": find_contact,
        "show all": show_all_contacts,
        "show": show_few_contacts,
        "show notes": show_all_notes,
        "search": search,
        "birthday": contact_birthday,
        "upcoming birthdays": contacts_upcoming_birthday,
        "add" : add,
        "edit" : edit,
        "delete contact" : delete_contact,
        "delete phone" : delete_contact_phone,
        "delete email" : delete_contact_email,
        "delete birthday" : delete_contact_birthday,
        "delete address" : delete_contact_address,
        "delete tag" : delete_contact_tag,
        "delete notes" : delete_contact_notes,
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
