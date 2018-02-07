from user import *
from documents import *
from database import *
import datetime as date


def check_out(user, book):
    init_date = date.datetime.toordinal(date.datetime.today())
    exp_date = date.datetime.fromordinal(init_date + 14)

    if user == Patron:
        get_book(book)
        print(user + ' checked out the book called ' + book + ' on: ' + str(init_date) + '. Expiry date is: ' + str(exp_date))
    elif user == Faculty:
        get_book(book)
        print(user + ' checked out the book called ' + book + ' on: ' + str(init_date) + '. Expiry date is: ' + str(exp_date))
