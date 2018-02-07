from user import *
import documents as docs
import database as db
import datetime as date
from documents import Book

# title, author, publisher, edition, genre
book1 = Book("One Hundred Years of Solitude", "Gabriel García Márquez", "Innopolis", "1", "Magical Realism")
book2 = Book("Thinking in Java", "q", "Innopolis", "4th", "Computer Science")
book3 = Book("Think python", "Allen B. Downey", "O'REILEY", "2nd", "Computer Science")



def check_out(user, book):
    init_date = date.datetime.toordinal(date.datetime.today())
    exp_date = date.datetime.fromordinal(init_date + 14)

    if user == Patron:
        if book == docs.Book.get_is_bestseller(True):
            db.get_book(book)
            print(user + ' checked out the book called ' + book + ' on: ' + str(init_date) + '. Expiry date is: ' +
                  str(exp_date - 7))
        else:
            db.get_book(book)
            print(user + ' checked out the book called ' + book + ' on: ' + str(init_date) + '. Expiry date is: ' +
                  str(exp_date))
    elif user == Faculty:
        db.get_book(book)
        print(user + ' checked out the book called ' + book + ' on: ' + str(init_date) + '. Expiry date is: ' +
              str(exp_date + 14))


# check_out(db.get_patron("9038594898558545ID")[user_name], db.get_book("Thinking in Java")[docs.Book.get_title()])
print(db.get_patron("9038594898558545ID")[user_name])
print(db.get_book("Thinking in Java"))