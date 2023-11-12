from collections import UserDict
from dataclasses import dataclass

class Contact_not_found(Exception):
    pass

@dataclass
class AddressBook(UserDict):
    def __init__(self):
        self.contacts = {}

    def input_error(func):
        def wrapper(*args):
            try:
                return func(*args)       
            except KeyError as e:
                print(f"Username not provided or user not found. Try again.\n{str(e)}\n")
            except IndexError as e:
                print("Incorrect data has been entered. Try again.\n")
            except ValueError as e:
                print("I'm sorry, but I don't understand your request. Try again.\n")
            except Contact_not_found as e:
                print(f"Contact not found.")
            # except Exception as e:
            #     print(f"Error caught: {e} in function {func.__name__} with values {args}")
        return wrapper

    @input_error
    def func_hello(self):
        print("How can I help you?")
    
    @input_error
    def func_show(self):
        if not self.contacts:
            print("Address book is empty.")
        else:
            print('{:^60}'.format("-"*60))
            print('{:^20}|{:^20}|{:^20}'.format("Name", "Phone", "Email"))
            print('{:^60}'.format("-"*60))
            for name, contact in self.contacts.items():
                print('{:^20}|{:^20}|{:^20}'.format(name, contact[0], contact[1]))
    
    @input_error
    def func_add(self, name, phone=None, email = None):
        if len(name) == 0:
            raise KeyError
        else:
            new_contact = Record(name, phone, email)
            self.contacts[new_contact.name] = [new_contact.phone, new_contact.email]
            print('{:^60}'.format("-"*60))
            print('{:^20}|{:^20}|{:^20}'.format("Name", "Phone", "Email"))
            print('{:^60}'.format("-"*60))
            print('{:^20}|{:^20}|{:^20}'.format(name, self.contacts[name][0], self.contacts[name][1]))

    @input_error
    def func_edit_phone(self, name, new_phone):
        if name in self.contacts:
            contact = Record(name, self.contacts[name][0], self.contacts[name][1])
            contact.edit_phone(new_phone)
            self.contacts[contact.name][0] = contact.phone
        else:
            raise Contact_not_found
    
    @input_error
    def func_edit_email(self, name, new_email):
        if name in self.contacts:
            contact = Record(name, self.contacts[name][0], self.contacts[name][1])
            contact.edit_email(new_email)
            self.contacts[contact.name][1] = contact.email
        else:
            raise Contact_not_found

    @input_error
    def func_delete_contact(self, name):
        if name in self.contacts:
            self.contacts.pop(name)
            print("Contact deleted.")
        else:
            raise Contact_not_found

    @input_error
    def func_delete_phone(self, name):
        if name in self.contacts:
            contact = Record(name, self.contacts[name][0], self.contacts[name][1])
            contact.delete_phone()
            self.contacts[contact.name][0] = contact.phone
        else:
            raise Contact_not_found
        
    @input_error
    def func_delete_email(self, name):
        if name in self.contacts:
            contact = Record(name, self.contacts[name][0], self.contacts[name][1])
            contact.delete_email()
            self.contacts[contact.name][1] = contact.email
        else:
            raise Contact_not_found
    
    @input_error
    def func_find(self, name):
        if name in self.contacts:
            print('{:^60}'.format("-"*60))
            print('{:^20}|{:^20}|{:^20}'.format("Name", "Phone", "Email"))
            print('{:^60}'.format("-"*60))
            print('{:^20}|{:^20}|{:^20}'.format(name, self.contacts[name][0], self.contacts[name][1]))
        else:
            raise Contact_not_found
        
    @input_error
    def func_exit(self):
        print("Good bye!\n")
        exit()
    

@dataclass
class Field:
    pass

@dataclass
class Name(Field):
    pass

@dataclass
class Phone(Field):
    pass

@dataclass
class Email(Field):
    pass

@dataclass
class Record:
    name: Name
    phone: Phone
    email: Email

    def edit_phone(self, new_phone):
        self.phone = new_phone
        print(f"Phone number updated: {self.name} - {self.phone}")

    def edit_email(self, new_email):
        self.email = new_email
        print(f"Email updated: {self.name} - {self.email}")

    def delete_phone(self):
        self.phone = ""
        print(f"Phone number deleted for {self.name}")

    def delete_email(self):
        self.email = ""
        print(f"Email deleted for {self.name}")

def main():
    print("""
Hello! I am your virtual assistant.
What would you like to do with your Address Book?
Choose one of the commands:
    - hello - let's say hello,
    - add - to add new contact to Address Book,
    - find - to find user or info about user
    - edit phone - to change phone of the user,
    - edit email - to change email of the user,
    - delete contact - to remove contact from Address Book
    - delete phone - to delete phone of the user,
    - delete email - to delete email of the user,
    - show all - to show all of your contacts from address book,
    - good bye, close, exit or . - to say good bye and close the program.
After entering the command, you will be asked for additional information if needed to complete the command.""")

    addressbook = AddressBook()

    OPERATIONS_MAP = {
        "hello" : addressbook.func_hello,
        "add" : addressbook.func_add,
        "edit phone" : addressbook.func_edit_phone,
        "edit email" : addressbook.func_edit_email,
        "delete contact" : addressbook.func_delete_contact,
        "delete phone" : addressbook.func_delete_phone,
        "delete email" : addressbook.func_delete_email,
        "find" : addressbook.func_find,
        "show all" : addressbook.func_show,
        "good bye" : addressbook.func_exit,
        "close" : addressbook.func_exit,
        "exit" : addressbook.func_exit,
        "." : addressbook.func_exit,
    }

    while True:
        listen = input("\nEnter your command here: ")       
        
        if listen in OPERATIONS_MAP:
            if listen == "add":
                name = input("Enter name: ")
                phone = input("Enter phone: ")
                email = input("Enter email: ")           
                OPERATIONS_MAP[listen](name, phone, email)

            elif listen in ["find","delete contact", "delete phone", "delete email"]:
                name = input("Enter name: ")      
                OPERATIONS_MAP[listen](name)
            
            elif listen == "edit phone":
                name = input("Enter name of the contact to edit: ")
                new_phone = input("Enter new phone number: ")
                OPERATIONS_MAP[listen](name, new_phone)
            
            elif listen == "edit email":
                name = input("Enter name of the contact to edit: ")
                new_email = input("Enter new email: ")
                OPERATIONS_MAP[listen](name, new_email)
                
            else:
                OPERATIONS_MAP[listen]()
        else:
            print("Invalid command.")

if __name__ == '__main__':
    main()