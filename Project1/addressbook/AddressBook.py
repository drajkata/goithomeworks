from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime, timedelta
import pickle
from pathlib import Path
from TestData import TestData
from Record import Record, Name, Phone, Email, Birthday, Address, Tag, Notes

############################################################################      
### ABSTRACT CLASS

class AbstractAddressBook(ABC):
    @abstractmethod
    def help(self):
        pass
    
    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def save_data(self):
        pass
    
    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def show_per_page(self):
        pass

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def find(self):
        pass

    @abstractmethod
    def birthday(self):
        pass


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
class AddressBook(AbstractAddressBook):
    def __init__(self):
        self.counter: int
        self.filename = "contacts.bin"
        self.path = Path("./" + self.filename)

    def save_data(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.contacts, file)

    def read_data(self):
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
        contact_name = None
        if isinstance(name, str):
            contact_name = name
        else:
            contact_name = name.value
        for key, obj in self.contacts.items():
            value = getattr(obj, "name")
            if contact_name.lower() in value.lower():
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
    def help(self):
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
    def show(self):
        return self.contacts

    @input_error
    def show_per_page(self, number_of_contacts, new_counting, iterator = None):
        if new_counting == True:
            self.counter = 0
            iterator = iter(sorted(self.contacts.items(), key=lambda x: x[1].name))
        is_last = False
        contacts_to_display = {}
        if self.counter * number_of_contacts < len(self.contacts):
            for _ in range(number_of_contacts):
                try:
                    key, obj = next(iterator)
                    contacts_to_display[key] = obj
                except StopIteration:
                    break        
        self.counter += 1
        if self.counter * number_of_contacts >= len(self.contacts):
            is_last = True 
        return self.counter, iterator, contacts_to_display, is_last

############################################################################      
### SEARCH FUNCTIONS
                
    @input_error
    def find(self, contact_name):
        results_for_search = {}
        for key, obj in self.contacts.items():
            value = getattr(obj, "name")
            if contact_name.lower() in value.lower():
                results_for_search[key] = obj
        return results_for_search

    @input_error
    def search(self, keyword):
        results_for_keyword = {}
        attributes_to_search = ["name", "phone", "email", "birthday", "address", "tag", "notes"]
        for key, obj in self.contacts.items():
            for attribute in attributes_to_search:
                value = getattr(obj, attribute)
                if value is not None and keyword.lower() in value.lower():
                    results_for_keyword[key] = obj
                    break 
        return results_for_keyword

############################################################################  
#### ADD FUNCTION

    @input_error
    def add(self, name, phone, email, birthday, address, tag, notes):
        id = int(self.check_latest_id() + 1)
        new_contact = Record(name.value, phone.value, email.value, birthday.value, address.value, tag.value, notes.value)
        self.contacts[id] = new_contact
        return dict(filter(lambda item: item[0] == id, self.contacts.items()))

############################################################################  
#### EDIT FUNCTION

    @input_error
    def edit(self, contact_obj, name, phone, email, birthday, address, tag, notes):
        if name.value: contact_obj.edit_name(name.value)
        if phone.value : contact_obj.edit_phone(phone.value)
        if email.value : contact_obj.edit_email(email.value)
        if birthday.value : contact_obj.edit_birthday(birthday.value)
        if address.value : contact_obj.edit_address(address.value)
        if tag.value : contact_obj.edit_tag(tag.value)
        if notes.value : contact_obj.edit_notes(notes.value)
        return contact_obj       
    
############################################################################  
#### DELETE FUNCTION

    @input_error
    def delete(self, key, attr):
        delete_operation = {
            "phone" : self.contacts[key].delete_phone,
            "email" : self.contacts[key].delete_email,
            "birthday" : self.contacts[key].delete_birthday,
            "address" : self.contacts[key].delete_address,
            "tag" : self.contacts[key].delete_tag,
            "notes" : self.contacts[key].delete_notes,
        }
        if attr in delete_operation:
            delete_operation[attr]()
        else:
            self.contacts.pop(key)

############################################################################  
#### BIRTHDAY FUNCTIONS   

    @input_error
    def birthday(self, contact_name):
        results_for_birthday = {}
        for key, obj in self.contacts.items():
            if obj.name.lower() == contact_name.lower():
                results_for_birthday[key] = [obj, obj.days_to_birthday(obj.birthday)]
        return results_for_birthday

    @input_error
    def upcoming_birthdays(self, days_str):
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
            View.pretty_view_contacts(today_birthday)
        if any(birthdays_dict.items()):
            print("\nSend birthday wishes to your contact on the upcoming days:")
            View.pretty_view_contacts(birthdays_dict)
