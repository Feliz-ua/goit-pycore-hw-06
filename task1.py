from collections import UserDict

# Базовий клас для будь-якого поля запису (ім'я, телефон тощо)
class Field:
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту 
class Name (Field):
    pass

# Клас для зберігання номера телефону із валідацією (10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone must be a string of 10 digits.")
        super().__init__(value)
        
# Клас для зберігання інформації про контакт: ім'я та список телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"        
    
# Клас для зберігання та управління записами
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

# Створюємо декоратор для обробки помилок вводу
def input_error(func):

    def inner(*args, **kwargs):Ну
        try:
            return func(*args, **kwargs)
        # Обробка помилки, коли контакт не знайдено
        except KeyError:
            return "Contact not found, please check the name."
        # Обробка помилки, коли недостатньо аршументів для імені та телефону
        except ValueError:
            return "Give me name and phone please."
        # Обробка помилки, коли відсутнє ім'я для пошуку
        except IndexError:
            return "Enter user name."
    return inner

def parse_input(user_input):
    # Розбиваємо рядок введення на команду та аргументи
    cmd, *args = user_input.split()
    # Приводимо команду до нижнього регістру для уніфікації
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, contacts):
    # Додаємо контакт: потрібно два аргументи - ім'я та телефон
    # якщо аргументів менше 2 - буде ValueError
    name, phone = args  
    # записуємо у словник
    contacts[name] = phone  
    return "Contact added."

@input_error
def change_contact(args, contacts):
    # Змінюємо номер телефону у існуючого контакту
    name, phone = args
    if name not in contacts:
        # якщо немає такого контакту - виняток
        raise KeyError  
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    # Показуємо номер телефону по імені
    # якщо args пустий — буде IndexError
    name = args[0]  
    if name not in contacts:
        # якщо контакт не знайдено - виняток
        raise KeyError  
    return contacts[name]

def show_all(contacts):
    # Показуємо всі контакти у списку
    if not contacts:
        return "Contact list is empty."
    result = []
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)

def main():
    # Основна функція - цикл прийому команд і виклик функцій
    # словник для збереження контактів
    contacts = {}  
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            # Якщо користувач не ввів команду
            print("Invalid command.")
            continue
        # Обробка введеною команди
        command, args = parse_input(user_input)

        # Обробка команд бота
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
