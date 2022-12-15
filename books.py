import json

class Book:
    def __init__(self):
        self.name = "Без названия"
        self.description = "Без описания"
        self.price = 0.0
        
        self.content = "Без содержимого"
        
    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            
            "content": self.content
        }
    
    def from_json(self, data):
        self.name = data["name"]
        self.description = data["description"]
        self.price = data["price"]
        
        self.content = data["content"]

    def from_input(self):
        self.name = input("Название: ") or self.name
        self.description = input("Описание: ") or self.description
        
        while True:
            self.price = input("Цена: ") or self.price
            
            try:
                float(self.price)
                
                break
            except ValueError:
                print("Неправильно введена цена.")
                
                continue

        self.content = input("Содержимое: ") or self.content
        
    def __str__(self):
        return "%s: %s - %s \nЦена: %s" % (self.name, self.description, self.content, self.price)
        
class AudioBook(Book):
    def __init__(self):
        super().__init__()
        
        self.speaker = "Unnamed"
    
    def to_json(self):
        book_json = super().to_json()
        
        return book_json | { "speaker": self.speaker }
    
    def from_json(self, data):
        super().from_json(data)
        
        self.speaker = data["speaker"]

    def from_input(self):
        self.speaker = input("Диктор: ") or self.speaker

        super().from_input()
        
    def __str__(self):
        return super().__str__() + (" - Читает: %s" % (self.speaker))

class ElectronicBook(Book):
    def __init__(self):
        super().__init__()
        
        self.host = "www.google.com"
        self.page = "/books/?"
        
    def to_json(self):
        book_json = super().to_json()
        
        return book_json | { 
            "host": self.host,
            "page": self.page            
        }
    
    def from_json(self, data):
        super().from_json(data)
        
        self.host = data["host"]
        self.page = data["page"]

    def from_input(self):
        self.host = input("Домен: ") or self.host
        self.page = input("Веб-страница: ") or self.page

        super().from_input()
        
    def __str__(self):
        return super().__str__() + (" - Находится по адресу %s%s" % (self.host, self.page))

file = None
library = []

try:
    file = open("books.json", 'r')
    
    library_json = json.loads(file.read())

    file.close()

    for book in library_json:
        if book.get("host", None) is not None:
            electronic_book = ElectronicBook()
            electronic_book.from_json(book)
            
            library.append(electronic_book)
        else:
            audio_book = AudioBook()
            audio_book.from_json(book)
            
            library.append(audio_book)

except FileNotFoundError:
    file = open("books.json", 'w')
    file.write(json.dumps(library, indent=4))

    file.close()
    
def insert_book_to_library(book):
    book.from_input()
    for other_book in library:
        if other_book.name == book.name:
            print("Книга с таким именем уже существует!")
            
            return

    print("Добавлена книга: %s" % str(book))

    library.append(book)

def add_book():
    print()
    print("1. Добавить аудиокнигу")
    print("2. Добавить электронную книгу")
    print("3. Выйти в меню")
    print()

    selection = input("Ваш выбор: ")

    if selection == '1':
        book = AudioBook()
        
        insert_book_to_library(book)
    elif selection == '2':
        book = ElectronicBook()
        
        insert_book_to_library(book)
    elif selection == '3':
        return
    else:
        print("Неверный ввод, повторите попытку")

def lookup_library():
    print("Книги: ")
    for book in library:
        print(str(book))
        print()

def edit_book():
    name = input("Введите название книги: ")
    
    editing_book = None
    for book in library:
        if book.name == name:
            editing_book = book
            
            break

    if editing_book is not None:
        print("Редактируем книгу %s..." % name)
        
        editing_book.from_input()
        
        print(str(editing_book))
    else:
        print("Книга %s не найдена" % name)

def delete_book():
    name = input("Введите название книги: ")

    for book in library:
        if book.name == name:
            library.remove(book)
            
            print("Книга %s удалена" % name)
            
            return
            
    print("Книга %s не найдена" % name)

while True:
    print()
    print("1. Добавить книгу")
    print("2. Посмотреть магазин")
    print("3. Редактировать книгу")
    print("4. Удалить книгу")
    print("5. Выйти")
    print()

    selection = input("Ваш выбор: ")

    if selection == '1':
        add_book()
    elif selection == '2':
        lookup_library()
    elif selection == '3':
        edit_book()
    elif selection == '4':
        delete_book()
    elif selection == '5':
        break
    else: 
        print("Неверный ввод, повторите попытку")

library_json = [book.to_json() for book in library]

file = open("books.json", 'w')
file.write(json.dumps(library_json, indent=4))

file.close()
