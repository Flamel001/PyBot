import datetime
import utilities
import database as db
import bot


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

                user.add_document(book.get_list_of_copies().pop(0), str(exp_date))
                notify_all(user, book)
                return utilities.booking_success + str(exp_date)
            else:
                return utilities.booking_book_is_unavailable
        else:
            return utilities.booking_no_copies
    else:
        return utilities.booking_already_have_it


def notify_all(user, book):
    d = dict()
    d["document_list"] = user.get_docs_list()
    db.update_user(user.get_alias(), d)
    d.clear()
    d["copies"] = list(book.get_list_of_copies())
    db.update_book(book.get_title(), d)
    list_of_all_librarians = db.get_all_librarians()
    for librarian in list_of_all_librarians:
        bot.send(librarian, "user with alias " + str(user.get_alias()) + " has borrowed a book")
