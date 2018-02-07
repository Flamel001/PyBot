from database import *
from user import *
from documents import *
import documents as docs
import database as db

import datetime as date

# title, author, publisher, edition, genre

book2 = Book("Thinking in Java", "Bruce Eckel", "Innopolis", "4th", "Computer Science")
book3 = Book("Think python", "Allen B. Downey", "O'REILEY", "2nd", "Computer Science")
book1 = Book("One Hundred Years of Solitude", "Gabriel García Márquez", "Innopolis", "1", "Magical Realism")
book1.set_bestseller(True)
user1 = Student("Dalbaeb", "jsifj@iinno.ru", "+231312394", "@eblaneeshe")
user2 = Faculty("BigBrother", "9afiwe@ifrefre", "+013123", "@hahhahaha")

print(user1 == Student)


def check_out(user, book):
    user.add_document(book)

