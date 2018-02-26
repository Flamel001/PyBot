from database import *
from user import *
from documents import *
import documents as docs
import database as db
from bot import *
import datetime

# title, author, publisher, edition, genre

book2 = Book("Thinking in Java", "Bruce Eckel", "Innopolis", "4th", "Computer Science")
book3 = Book("Think python", "Allen B. Downey", "O'REILEY", "2nd", "Computer Science")
book1 = Book("One Hundred Years of Solitude", "Gabriel García Márquez", "Innopolis", "1", "Magical Realism")
book1.set_bestseller(True)
user1 = Student("Dalbaeb", "jsifj@iinno.ru", "+231312394", "@eblaneeshe")
user2 = Faculty("BigBrother", "9afiwe@ifrefre", "+013123", "@hahhahaha")


def book_doc(user, book):
    string = ""
    string = book.get_title()
    print(string)
    print(user)
    cnt = 2
    if string:
        if cnt > 0:
            if not book.is_reference():
                print("Book is not reference")

                init_date = datetime.datetime.toordinal(datetime.datetime.today())

                print("Rank " + str(user.get_rank()))
                if user.get_rank() == 1:
                    exp_date = datetime.datetime.fromordinal(init_date + 28)
                else:
                    if book.is_bestseller():
                        exp_date = datetime.datetime.fromordinal(init_date + 14)
                    else:
                        exp_date = datetime.datetime.fromordinal(init_date + 21)

                return "DONE. You will have to return this book until:" + str(exp_date)
            else:
                return "The book is unavailable"
        else:
            return "No copies."
    else:
        return "You are owning this book already"


def check_out(user, book):
    user.add_doc(book)
