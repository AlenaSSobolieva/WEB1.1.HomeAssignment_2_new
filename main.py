from collections import UserDict
from datetime import datetime
import pickle

class Field():
    def __init__(self, value):
        self.__value = None
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    @property
    def phone(self):
        return self.__value

    @phone.setter
    def phone(self, value):
        if len(value) > 0:
            self.__value = value
        else:
            raise ValueError('You should enter the phone number!')

class Birthday(Field):
    @property
    def birthday(self):
        return self.__value

    @birthday.setter
    def birthday(self, value):
        if len(value) > 0:
            self.__value = value
        else:
            raise ValueError('You should enter the date of birthday!')


class Record():

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)


    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)


    def remove_phone(self, phone):
        self.phones.remove(phone)


    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def days_to_birthday(self, birthday):
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_year = current_date.year

        date_of_birthday = datetime.date(birthday)

        current_birthday = date_of_birthday.replace(year=current_year).date()
        days_left = current_birthday - current_date
        return days_left


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, name):
        record = self.data.get(name)
        if record is None:
            return ValueError(f'Record for  {name} not exists')
        return record

    def dump(self):
        with open(self.file, 'wb') as file:
            pickle.dump((self.last_record_id, self.records), file)

    def load(self):
        if not self.file.exists():
            return
        with open(self.file, 'rb') as file:
            self.last_record_id, self.records = pickle.load(file)

    def search(self, search_str):
        result = []
        for record_id, record in self.records.items():
            if search_str in record:
                result.append(record_id)
        return result

class Iterator(AddressBook):
    def __init__(self, quantity):
        self.quantity = quantity
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if self.count > self.quantity:
            raise StopIteration
        else:
            print(record * quantity)




if __name__ == "__main__":

    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'
    print('All Ok)')