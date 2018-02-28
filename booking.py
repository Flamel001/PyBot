from user import *
from documents import *
import datetime
import utilities

# title, author, publisher, edition, genre

book2 = Book("Thinking in Java", "Bruce Eckel", "Innopolis", "4th", "Computer Science")
book3 = Book("Think python", "Allen B. Downey", "O'REILEY", "2nd", "Computer Science")
book1 = Book("One Hundred Years of Solitude", "Gabriel García Márquez", "Innopolis", "1", "Magical Realism")
book1.set_bestseller(True)
user1 = Student("Dalbaeb", "jsifj@iinno.ru", "+231312394", "@eblaneeshe")
user2 = Faculty("BigBrother", "9afiwe@ifrefre", "+013123", "@hahhahaha")


def book_doc(user, book):
    has = user.has_book(book.get_title())
    number_of_copies = book.get_number_of_copies()
    if not has:
        if number_of_copies > 0:
            if not book.is_reference():

                init_date = datetime.datetime.toordinal(datetime.datetime.today())

                if user.get_rank() == 1:
                    exp_date = datetime.datetime.fromordinal(init_date + 28)
                else:
                    if book.is_bestseller():
                        exp_date = datetime.datetime.fromordinal(init_date + 14)
                    else:
                        exp_date = datetime.datetime.fromordinal(init_date + 21)
                    user.add_document(book.get_title(), str(exp_date))
                return utilities.booking_success + str(exp_date)
            else:
                return utilities.booking_book_is_unavailable
        else:
            return utilities.booking_no_copies
    else:
        return utilities.booking_already_have_it
