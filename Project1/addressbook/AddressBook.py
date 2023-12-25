from collections import UserDict
from dataclasses import dataclass
from datetime import datetime, timedelta
import pickle
from pathlib import Path
from TestData import TestData
from Record import Record, Name, Phone, Email, Birthday, Address, Tag, Notes
import DataPresentation
from DataPresentation import ContactNotFound

############################################################################      
### ITERATOR

class IteratorOfContacts:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.keys = list(dictionary.keys())
        self.index = 0
        
    def __next__(self):
        if self.index > len(self.dictionary):
            raise StopIteration
        key = self.keys[self.index]
        value = self.dictionary[key]
        self.index += 1
        yield key, value

############################################################################      
### MAIN CLASS ADDRESSBOOK

@dataclass
class AddressBook(UserDict):
    def __init__(self):
        self.counter: int
        self.filename = "contacts.bin"
        self.path = Path("./" + self.filename)

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.contacts, file)

    def read_from_file(self):
        if self.path.is_file() == False:
            test_data = TestData()
            self.contacts = test_data.test_contacts
        else:
            with open(self.filename, "rb") as file:
                self.contacts = pickle.load(file)
        return self.contacts

    def __iter__(self):
        return IteratorOfContacts(self.contacts)

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
                print("\nSorry, but I couldn't find any contacts with this name.")
            # except Exception as e:
            #     print(f"Error caught: {e} in function {func.__name__} with values {args}")

        return wrapper

    



############################################################################      
### GENERAL FUNCTIONS

    @input_error
    def check_entered_values(self, name = None, phone = None, email = None, birthday = None, address = None, tag = None, notes = None):
        if name.value is None and phone.value is None and email.value is None and birthday.value is None and address.value is None and tag.value is None and notes.value is None:
            return False
        else: return True
    
    @input_error
    def check_if_object_exists(self, name):
        results = {}
        if any(str(obj.name).lower() == name.lower() for obj in self.contacts.values()):
            for key, obj in self.contacts.items():
                if str(obj.name).lower() == name.lower():
                    results[key] = obj
        return results


    @input_error
    def check_latest_id(self):
        list_of_id = []
        for key_id in self.contacts.keys():
            list_of_id.append(key_id)
        max_ID = max(list_of_id)
        return max_ID



############################################################################      
### HELP FUNCTIONS
    @input_error
    def func_help(self):
        print("""
What would you like to do with your Address Book?
Choose one of the commands:
    - help - check what can you do with this Address Book,
    - find - to find a contact by name,
    - search - to find a contact after entering keyword,
    - show all - to show all of your contacts from address book,
    - show - to display N contacts from Address Book,
    - show notes - to display contact name with tag and notes,
    - add - to add new contact to Address Book,
    - edit phone - to change phone of the user,
    - edit email - to change email of the user,
    - edit birthday - to change birthday of the user,
    - edit address - to change address of the user,
    - edit tag - to change tag of the user,
    - edit notes - to change notes of the user,      
    - delete contact - to remove contact from Address Book
    - delete phone - to delete phone of the user,
    - delete email - to delete email of the user,
    - delete birthday - to delete birthday of the user,
    - delete address - to delete address of the user, 
    - delete tag - to delete tag of the user,
    - delete notes - to delete notes of the user,
    - birthday - to display days to birthday of the user,
    - upcoming birthdays - to check upcoming birthdays from your conatct in Address Book
    - good bye, close, exit or . - to say good bye and close the program.
After entering the command, you will be asked for additional information if needed to complete the command.""")

############################################################################      
### SHOW FUNCTIONS
            
    @input_error
    def func_show_all(self):
        if len(self.contacts) == 0:
            print("Address book is empty.")
        else:
            DataPresentation.pretty_view_contacts(self.contacts)

    @input_error
    def func_show(self, number_of_contacts):
        iterator = iter(sorted(self.contacts.items(), key=lambda x: x[1].name))
        
        self.counter = 0
        while True:
            self.counter += 1
            print(f"\nPAGE {self.counter}")
            contacts_to_display = {}
            for _ in range(number_of_contacts):
                try:
                    key, obj = next(iterator)
                    contacts_to_display[key] = obj
                except StopIteration:
                    break
            DataPresentation.pretty_view_contacts(contacts_to_display)
            if self.counter * number_of_contacts < len(self.contacts):
                choice = input(
                    f"\nDo you want to display next {number_of_contacts} contact(s)? (Y/N) "
                )
                if choice not in ["y", "Y", "Yes", "yes", "True"]:
                    break
            else:
                break

############################################################################      
### SEARCH FUNCTIONS
                
    @input_error
    def func_find(self, contact_name):
        results_for_search = {}
        for key, obj in self.contacts.items():
            value = getattr(obj, "name")
            if contact_name.lower() in value.lower():
                results_for_search[key] = obj
        if len(results_for_search) > 0:
            DataPresentation.pretty_view_contacts(results_for_search)
        else:
            return None

    @input_error
    def func_search(self, keyword):
        results_for_keyword = {}
        attributes_to_search = ["name", "phone", "email", "birthday", "address", "tag", "notes"]

        for key, obj in self.contacts.items():
            for attribute in attributes_to_search:
                value = getattr(obj, attribute)
                if keyword.lower() in value.lower():
                    results_for_keyword[key] = obj
                    break 
        if len(results_for_keyword) > 0:
            DataPresentation.pretty_view_contacts(results_for_keyword)
        else:
            return None


############################################################################  
#### ADD FUNCTIONS

    @input_error
    def add_contact(self, name, phone, email, birthday, address, tag, notes):
        values_tu_add = {
            "name" : name.value,
            "phone" : phone.value,
            "email" : email.value,
            "birthday" : birthday.value,
            "address" : address.value,
            "tag" : tag.value,
            "notes" : notes.value
            }
        to_add = False
        corrected_values = self.check__entered_values(phone, email, birthday, address, tag, notes)
        contacts = self.check_if_object_exists(name)
        if len(contacts) == 0:
            to_add = True
        else:
            if corrected_values:
                print("\nI've found in the Address Book the contact(s) with the same name:")
                DataPresentation.pretty_view_contacts(contacts)
                choice = None
                choice = input("\nWould you like to update the contact(s) with the information you entered? (Y/N): ")
                if choice in ["y", "Y", "Yes", "yes", "True"]:
                    if len(contacts) == 1:
                        self.func_update_information(contacts[1], values_tu_add)
                    else:
                        while True:
                            number = None
                            number = int(input("Please enter the ID number of the contact you want to update: "))
                            if number in contacts.keys():
                                print("\nI've updated the contact with the entered data. Here is your contact:")
                                self.func_update_information(contacts[number], values_tu_add)
                                results_to_display = {}
                                results_to_display[number] = contacts[number]
                                DataPresentation.pretty_view_contacts(results_to_display)
                                break
                            else:
                                print("\nSorry, but I couldn't find any contacts with this ID. Try again...")
                else:
                    print("\nI took no action.")
            else:
                print("\nI've found in the Address Book the contact(s) with the same name, but you did not enter any data to change the contact information. Please try again.")
        if to_add == True:
            id = int(self.check_latest_id() + 1)
            new_contact = Record(name.value, phone.value, email.value, birthday.value, address.value, tag.value, notes.value)
            self.contacts[id] = new_contact
            print("\nI've added a contact to the address book with the following information:")
            results_to_display = {}
            results_to_display[id] = new_contact
            DataPresentation.pretty_view_contacts(results_to_display)  

############################################################################  
#### EDIT FUNCTIONS
    
    @input_error
    def func_update_information(self, contact_obj, new_values: dict):
        if new_values["name"] : contact_obj.edit_name(new_values["name"])
        if new_values["phone"] : contact_obj.edit_phone(new_values["phone"])
        if new_values["email"] : contact_obj.edit_email(new_values["email"])
        if new_values["birthday"] : contact_obj.edit_birthday(new_values["birthday"])
        if new_values["address"] : contact_obj.edit_address(new_values["address"])
        if new_values["tag"] : contact_obj.edit_tag(new_values["tag"])
        if new_values["notes"] : contact_obj.edit_notes(new_values["notes"])

    @input_error
    def edit_contact(self, obj, name, phone, email, birthday, address, tag, notes):
        values_tu_update = {
            "name" : name.value,
            "phone" : phone.value,
            "email" : email.value,
            "birthday" : birthday.value,
            "address" : address.value,
            "tag" : tag.value,
            "notes" : notes.value
            }
        self.func_update_information(obj, values_tu_update)
        return obj
        
    
############################################################################  
#### DELETE FUNCTIONS

    @input_error
    def func_delete_contact(self, contact_name):
        if any(obj.name == contact_name for obj in self.contacts.values()):
            results = {}
            for key, obj in self.contacts.items():
                if obj.name == contact_name:
                    results[key] = obj
            print("\nI've found in the Address Book the following contact(s):")
            DataPresentation.pretty_view_contacts(results)
            choice = None
            choice = input("\nWould you like to delete the contact(s)? (Y/N): ")
            if choice in ["y", "Y", "Yes", "yes", "True"]:
                if len(results) == 1:
                    self.contacts.remove(key)
                    print("\nOf course! I've deleted successfully the contact with the entered data.")  
                if len(results) > 1:
                    print("\nOf course! ")
                    while True:
                        number = None
                        number = int(input("Please enter the ID number of the contact you want to delete: "))
                        if number in results.keys():
                            self.contacts.pop(number)
                            print(f"\nI've deleted successfully the contact with id: {number}")
                            break
                        else:
                            print("\nSorry, but I couldn't find any contacts with this ID. Try again...")
            else:
                print("\nI took no action.")
        else:
            raise ContactNotFound

    @input_error
    def func_delete_phone(self, contact_name):
        if any(obj.name == contact_name for obj in self.contacts.values()):
            result = None
            result = next(obj for obj in self.contacts.values() if obj.name == contact_name)
            result.delete_phone()
        else:
            raise ContactNotFound

    @input_error
    def func_delete_email(self, contact_name):
        if any(obj.name == contact_name for obj in self.contacts.values()):
            result = None
            result = next(obj for obj in self.contacts.values() if obj.name == contact_name)
            result.delete_email()
        else:
            raise ContactNotFound

    @input_error
    def func_delete_birthday(self, contact_name):
        if any(obj.name == contact_name for obj in self.contacts.values()):
            result = None
            result = next(obj for obj in self.contacts.values() if obj.name == contact_name)
            result.delete_birthday()
        else:
            raise ContactNotFound

    @input_error
    def func_delete_address(self, contact_name):
        if any(obj.name == contact_name for obj in self.contacts.values()):
            result = None
            result = next(obj for obj in self.contacts.values() if obj.name == contact_name)
            result.delete_address()
        else:
            raise ContactNotFound

    @input_error
    def func_delete_tag(self, contact_name):
        if any(obj.name == contact_name for obj in self.contacts.values()):
            result = None
            result = next(obj for obj in self.contacts.values() if obj.name == contact_name)
            result.delete_tag()
        else:
            raise ContactNotFound

    @input_error
    def func_delete_notes(self, contact_name):
        if any(obj.name == contact_name for obj in self.contacts.values()):
            result = None
            result = next(obj for obj in self.contacts.values() if obj.name == contact_name)
            result.delete_notes()
        else:
            raise ContactNotFound

############################################################################  
#### BIRTHDAY FUNCTIONS   

    @input_error
    def func_birthday(self, contact_name):
        if any(obj.name == contact_name for obj in self.contacts.values()):
            result = None
            result = next(obj for obj in self.contacts.values() if obj.name == contact_name)
            result.days_to_birthday(result.name, result.birthday)
        else:
            raise ContactNotFound

    @input_error
    def func_upcoming_birthdays(self, days_str):
        def month_sort_key(date_str):
            date = datetime.strptime(date_str, "%d %B (%A)")
            current_month = datetime.now().month
            return (date.month - current_month) % 12
        today = datetime.now()
        formatted_date = today.strftime("%d %B %Y")
        days = int(days_str)
        last_day = today + timedelta(days=days)
        formatted_last_day = last_day.strftime("%d %B %Y")
        print(
            f"\nChecking period ({formatted_date} - {formatted_last_day}).\n")

        birthdays_dict= {}
        today_birthday = {}

        for key, obj in self.contacts.items():
            
            if obj.birthday is not None:
                birthday = datetime.strptime(obj.birthday, "%Y-%m-%d").date()

                birthday_this_year = birthday.replace(year=today.year)
                birthday_next_year = birthday.replace(year=today.year + 1)

                if today.date() < birthday_this_year <= last_day.date():
                    day_of_week = birthday_this_year.strftime("%d %B (%A)")
                    if day_of_week not in birthdays_dict:
                        birthdays_dict[key] = None
                    birthdays_dict[key] = obj
                elif today.date() < birthday_next_year <= last_day.date():
                    day_of_week = birthday_next_year.strftime("%d %B (%A)")
                    if day_of_week not in birthdays_dict:
                        birthdays_dict[key] = None
                    birthdays_dict[key] = obj
                elif today.date() == birthday_this_year:
                    day_of_week = birthday_this_year.strftime("%d %B (%A)")
                    if day_of_week not in today_birthday:
                        today_birthday[key] = None
                    today_birthday[key] = obj

        if not any(birthdays_dict.items()) and not any(today_birthday.items()):
            print(f"\nNone of your contacts have upcoming birthdays in this period.")
        else:
            print(
                "   O O O O \n" "  _|_|_|_|_\n" " |         |\n",
                "|         |\n",
                "|_________|\n",
            )
        if any(today_birthday.items()):
            print('Someone has birthday today, so wish "HAPPY BIRTHDAY" today to:')
            DataPresentation.pretty_view_contacts(today_birthday)
        if any(birthdays_dict.items()):
            print("\nSend birthday wishes to your contact on the upcoming days:")
            DataPresentation.pretty_view_contacts(birthdays_dict)
