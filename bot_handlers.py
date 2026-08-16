from birthday_handlers import get_upcoming_birthdays
from classes import AddressBook, Record, NotFoundError, NotCorrectArgumentsError


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact is not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
        except NotFoundError as e:
            return e.message
        except NotCorrectArgumentsError as e:
            return e.message

    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
    
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
  
@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise NotCorrectArgumentsError("Not enough arguments. Provide name, old phone, and new phone.")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        raise KeyError(name)
    if record.find_phone(old_phone) is None:
        raise NotFoundError("Old phone number not found.")
    if new_phone:
        record.edit_phone(old_phone, new_phone)
    return message

@input_error
def show_phone(args, book: AddressBook): 
    name, *_ = args
    record = book.find(name)
    phones = []
    if record is None:
        raise KeyError(name)
    for phone in record.phones:
        phones.append(phone.value)
    return ", ".join(phones)

@input_error
def show_all(book: AddressBook): 
    result = []
    for name, record in book.items():
        phones = [phone.value for phone in record.phones]
        result.append(f"{name}: {', '.join(phones)}, Birthday: {record.birthday}")
    return "\n".join(result)

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    if birthday:
        if record.add_birthday(birthday):
            return "Birthday added."
    return ''

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    return record.birthday

@input_error
def birthdays(args, book: AddressBook):
    return get_upcoming_birthdays(book)
