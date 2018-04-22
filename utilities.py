from telebot import *
from user import *
from documents import *
import datetime as dt

greeting = """Welcome to Innopolis Library Management System.
              Please enter your e-mail address.
              Remember it should contain @innopolis.ru domain, otherwise you won't be able
              to authorise.
              Please press /setup to setup your profile."""

verification_err_mail = "Invalid e-mail"

booking_success = "DONE. You will have to return this book until:"
booking_book_is_unavailable = "The book is unavailable"
booking_no_copies = "No copies."
booking_already_have_it = "You are owning this book already"

keyboard_button_back = [["Back", "Back"]]

keyboard_buttons_choice = [["Librarian", "Librarian"], ["Patron", "Patron"]]

keyboard_buttons_library = [["Books", "Books"], ["Articles", "Articles"], ["Audio/Video", "Audio/Video"],
                            ["Back", "Back"]]

"LIBRARIAN"
keyboard_librarian_buttons_home = [["Actions with Patrons", "Actions with Patrons"], ["Manage Docs", "Library"],
                                   ["Docs on hands", "Docs on hands"]]
keyboard_librarian_buttons_library = [["Add", "Add doc"], ["Manage docs", "Library"]]
keyboard_librarian_buttons_manage = [["Edit", "Edit"], ["Get information", "Get information"], ["Delete", "Delete"],
                                     ["Return to home page", "Back"]]
keyboard_librarian_buttons_edit = [["Name", "Name"], ["Surname", "Surname"], ["mail", "mail"], ["number", "number"],
                                   ["alias", "alias"], ["address", "address"], ["Back", "Back"]]
keyboard_librarian_buttons_confirmation = [["Add", "Add"], ["Back", "Actions with Patrons"]]

"PATRON"
keyboard_patron_buttons_home = [["Library", "Library"], ["My docs", "My docs"], ["Tech support", "Tech support"]]
keyboard_patron_buttons_library = [["Books", "Books"], ["Articles", "Articles"], ["Audio/Video", "Audio/Video"],
                                   ["Back", "Back"]]
keyboard_patron_buttons_reserve = [["Reserve", "Reserve"], ["Back", "Back"]]
keyboard_patron_buttons_doc = [["Return", "Return"], ["Renew", "Renew"], ["Back", "Back"]]

"ADMIN"
keyboard_admin_buttons_privileges = [["1", "1"], ["2", "2"], ["3", "3"]]
keyboard_admin_buttons_home = [["Manage Librarians", "Manage Librarians"], ["Action Log", "Action Log"]]

# current_email = ""
# field = ""
# # is_librarian = False
# db_to_search = []
# current_object = dict
# current_type = ""
# title_or_name = ""

def get_date():
    date = str(dt.datetime.now())
    a = len(date)

    return (date[:a - 7])


class current:
    current_email = ""
    title_or_name = ""
    field = ""
    db_to_search = []
    current_object = ""
    current_type = ""
    pin = ""
    temp_user_date = dict()
    auth_arr = ["name","number","address"]
    auth_val_arr = []
    time = ""
    user = ""


multithreading = dict()

# title, author, publisher, edition, genre

# book4 = Book("Jane Eyre", "Charlotte Bronte", "SomePublisher", "1", "SomeGenre")
# book2 = Book("Thinking in Java", "Bruce Eckel", "Innopolis", "4th", "Computer Science")
# book3 = Book("Think python", "Allen B. Downey", "O'REILEY", "2nd", "Computer Science")
# book1 = Book("One Hundred Years of Solitude", "Gabriel García Márquez", "Innopolis", "1", "Magical Realism")
# # book1.add_copy("1")
# # book1.add_copy("2")
# # book1.add_copy("3")
# # book1.add_copy("4")
# # book1.add_copy("5")
# book1.set_bestseller(True)
# user1 = Student("314603915", "Dalbaeb", "jsifj@iinno.ru", "+231312394", "@eblaneeshe")
# user2 = Faculty("314603916", "BigBrother", "9afiwe@ifrefre", "+013123", "@hahhahaha")
# # book1 = Book()
# # book1.setData(db.get_book("One Hundred Years of Solitude"))
#
# list_of_books = [book1, book2, book3, book4]

# auth literals
step0 = "Enter you email"
step1 = "Now enter your Name: "
step2 = "Wonderful! Now your surname: "
step3 = "Excellent! Now the last step. Leave your number: "
step4 = "Congratulations! Your sign up has been done!"
verification_succeed = "Great!"
verification_failed = "It's not that PIN that I've sent you :( "
domain = "@innopolis.ru"
pin_enter = "Please enter PIN I've sent to you. "

tempData = {'userId': '0'}


keyboard_initial = [["p1", "1010"], ["p2", "1011"], ["p3", "1100"], ["l", "l"], ["s", "1101"], ["v", "1110"]]
current_id = ""


