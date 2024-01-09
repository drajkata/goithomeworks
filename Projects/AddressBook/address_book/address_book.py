from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime, timedelta
import pickle
from pathlib import Path
from test_data import TestData
from record import Record, Name, Phone, Email, Birthday, Address, Tag, Notes
import view

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
    def check_if_object_exists(self, contact_name):
        results = {}
        if not isinstance(contact_name, str):
            contact_name = contact_name.value
        for key, obj in self.contacts.items():
            obj_name = getattr(obj, "name")
            if contact_name.lower() in obj_name.value.lower():
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
    - show - to display N contacts from the Address Book,
    - show notes - to display contact name with tag and notes,
    - add - to add new contact to the Address Book,
    - edit - to modify attribute of the user,
    - delete - to remove attribute of the user or remove contact from the Address Book
    - birthday - to display days to birthday of the user,
    - upcoming birthdays - to check upcoming birthdays from your conatct from the Address Book
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
            name = getattr(obj, "name")
            if contact_name.lower() in name.value.lower():
                results_for_search[key] = obj
        return results_for_search

    @input_error
    def search(self, keyword):
        results_for_keyword = {}
        attributes_to_search = ["name", "phone", "email", "birthday", "address", "tag", "notes"]
        for key, obj in self.contacts.items():
            for attribute in attributes_to_search:
                contact = getattr(obj, attribute)
                if contact.value is not None and keyword.lower() in contact.value.lower():
                    results_for_keyword[key] = obj
                    break 
        return results_for_keyword

############################################################################  
#### ADD FUNCTION

    @input_error
    def add(self, name: Name, phone: Phone, email: Email, birthday: Birthday, address: Address, tag: Tag, notes: Notes):
        id = int(self.check_latest_id() + 1)
        new_contact = Record(name, phone, email, birthday, address, tag, notes)
        self.contacts[id] = new_contact
        return dict(filter(lambda item: item[0] == id, self.contacts.items()))

############################################################################  
#### EDIT FUNCTION

    @input_error
    def edit(self, contact_obj, name: Name, phone: Phone, email: Email, birthday: Birthday, address: Address, tag: Tag, notes: Notes):
        if name: contact_obj.edit_name(name)
        if phone : contact_obj.edit_phone(phone)
        if email : contact_obj.edit_email(email)
        if birthday : contact_obj.edit_birthday(birthday)
        if address : contact_obj.edit_address(address)
        if tag : contact_obj.edit_tag(tag)
        if notes : contact_obj.edit_notes(notes)
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
        # def month_sort_key(date_str):
        #     date = datetime.strptime(date_str, "%d %B (%A)")
        #     current_month = datetime.now().month
        #     return (date.month - current_month) % 12
        today = datetime.now()
        formatted_date = today.strftime("%d %B %Y")
        days = int(days_str)
        last_day = today + timedelta(days=days)
        formatted_last_day = last_day.strftime("%d %B %Y")
        print(
            f"\nChecking period ({formatted_date} - {formatted_last_day}).\n")

        today_dict = {}
        upcoming_dict= {}

        for key, obj in self.contacts.items():
            
            if obj.birthday is not None:
                birthday = datetime.strptime(obj.birthday, "%Y-%m-%d").date()

                birthday_this_year = birthday.replace(year=today.year)
                birthday_next_year = birthday.replace(year=today.year + 1)

                if today.date() < birthday_this_year <= last_day.date():
                    day_of_week = birthday_this_year.strftime("%d %B (%A)")
                    if day_of_week not in upcoming_dict:
                        upcoming_dict[key] = None
                    upcoming_dict[key] = obj
                elif today.date() < birthday_next_year <= last_day.date():
                    day_of_week = birthday_next_year.strftime("%d %B (%A)")
                    if day_of_week not in upcoming_dict:
                        upcoming_dict[key] = None
                    upcoming_dict[key] = obj
                elif today.date() == birthday_this_year:
                    day_of_week = birthday_this_year.strftime("%d %B (%A)")
                    if day_of_week not in today_dict:
                        today_dict[key] = None
                    today_dict[key] = obj

        return [today_dict, upcoming_dict]
