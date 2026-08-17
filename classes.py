from collections import UserDict
import re
from datetime import datetime
from birthday_handlers import get_upcoming_birthdays
from dataclasses import dataclass


phone_regex = r'^\d{10}$'

@dataclass
class Field:
    value: str

    def __str__(self):
        return str(self.value)
@dataclass
class Name(Field):
    value: str

class Phone(Field):
    def __init__(self, value: str):
        if not re.match(phone_regex, value):
            raise ValueError("Invalid phone number format")
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            parsed = datetime.strptime(value, "%d.%m.%Y").date()
            self.value = parsed
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
            else:
                None

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
            return True
        except ValueError as e:
            print(f"Invalid birthday for {self.name.value}: {e}")
            return False

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def show_upcoming_birthdays(self):
        return get_upcoming_birthdays(self.data)

class NotFoundError(Exception):
    def __init__(self, message="Value not found"):
        self.message = message
        super().__init__(self.message)


class NotCorrectArgumentsError(Exception):
    def __init__(self, message="Not enough arguments"):
        self.message = message
        super().__init__(self.message)