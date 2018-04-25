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

keyboard_buttons_library = [["Books", "Book"], ["Articles", "Article"], ["Audio/Video", "AV"],
                            ["Back", "Back"]]

"LIBRARIAN"
keyboard_librarian_buttons_home = [["Actions with Patrons", "Actions with Patrons"], ["Manage Docs", "Library"]]#,["Docs on hands", "Docs on hands"]
keyboard_librarian_buttons_library = [["Add", "Add doc"], ["Manage docs", "Library"]]
keyboard_librarian_buttons_manage = [["Get information", "Get information"], ["Edit", "Edit"],  ["Delete", "Delete"]]
keyboard_librarian_buttons_edit = [["Name", "Name"], ["Surname", "Surname"], ["mail", "mail"], ["number", "number"],
                                   ["alias", "alias"], ["address", "address"], ["Back", "Back"]]
keyboard_librarian_buttons_confirmation = [["Add", "Add"], ["Back", "Back"]]
keyboard_librarian_buttons_add_new_type = [["Student","Student"], ["Professor","Professor"], ["TA","TA"], ["VP","VP"], ["Instructor","Instructor"], ["Book", "Book"], ["Article", "Article"], ["Audio/Video", "AV"]]

"PATRON"
keyboard_patron_buttons_home = [["Library", "Library"], ["My docs", "My docs"], ["Tech support", "Tech support"]]
# keyboard_patron_buttons_library = [["Books", "Book"], ["Articles", "Article"], ["Audio/Video", "AV"],
#                                    ["Back", "Back"]]
keyboard_patron_buttons_reserve = [["Reserve", "Reserve"], ["Back", "Back"]]
keyboard_patron_buttons_doc = [["Return", "Return"], ["Renew", "Renew"], ["Back", "Back"]]

"ADMIN"
keyboard_admin_buttons_privileges = [["1", "1"], ["2", "2"], ["3", "3"]]
keyboard_admin_buttons_home = [["Manage Librarians", "Manage Librarians"], ["Action Log", "Action Log"]]

def get_buttoms(name: str):
    if name == "Emails":#"Student" or name == "Instructor" or name == "TA" or name == "Professor" or name == "VP"
        result = []
        temp = ['id', 'Alias', 'Name',  'Phone_number', 'Address','Mail']
        for x in temp:
            result.append([x, "$" + x])
        return result
    elif name == "Librarian":
        result = []
        temp = ['id', 'Alias', 'Name', 'Phone_number', 'Address', 'Privilege','Mail']
        for x in temp:
            result.append([x, "$" + x])
        return result
    elif name == "Book":
        result = []
        temp = ['Author', 'Publisher', 'Year', 'Edition', 'Genre', 'Bestseller', 'Reference','Price', 'Copies']#'Title',
        for x in temp:
            result.append([x, "$" + x])
        return result
    elif name == "Article":
        result = []
        temp = [ 'Author', 'Journal', 'Pub_Date', 'Editor', 'Price', 'Url','Price','Copies']#'Title',
        for x in temp:
            result.append([x, "$" + x])
        return result
    elif name == "AV":
        result = []
        temp = ['Author', 'Price','Copies']#'Title',
        for x in temp:
            result.append([x, "$" + x])
        return result
    else:
        return None

# def edit_attr(attr,new_attr):
#     "BOOK"
#     if attr == "Title":
#         current.object.set_title(new_attr)
#     elif attr == "Author":
#         current.object.set_author(new_attr)
#     elif attr == "Publisher":
#         current.object.set_publisher(new_attr)
#     elif attr == "Year":
#         current.object.set_year(new_attr)
#     elif attr == "Edition":
#         current.object.set_edition(new_attr)
#     elif attr == "Genre":
#         current.object.set_genre(new_attr)
#     elif attr == "Bestseller":
#         current.object.set_bestseller(new_attr)
#     elif attr == "Reference":
#         current.object.set_reference(new_attr)
#     elif attr == "Price":
#         current.object.set_price(new_attr)
#
#         "ARTICLE"
#
#     elif attr == "Journal":
#         current.object.set_journal(new_attr)
#     elif attr == "Pub_Date":
#         current.object.set_pub_date(new_attr)
#     elif attr == "Editor":
#         current.object.set_editor(new_attr)
#
#         "PATRON"
#
#     elif attr == "id":
#         current.object.set_id(new_attr)
#     elif attr == "Alias":
#         current.object.set_alias(new_attr)
#     elif attr == "Name":
#         current.object.set_name(new_attr)
#     elif attr == "Mail":
#         current.object.set_mail(new_attr)
#     elif attr == "Phone_number":
#         current.object.set_number(new_attr)
#     elif attr == "Address":
#         current.object.set_address(new_attr)
#
#         "LIBRARIAN"
#     elif attr == "Privilege":
#         current.object.set_priv(new_attr)
#
# def is_human():
#     if current.type == "Emails" or current.type == "Librarian":
#         return True
#     else:
#         return False

def get_date():
    date = str(dt.datetime.now())
    a = len(date)

    return (date[:a - 7])


class current:
    attr = ""
    email = ""
    title_or_name = ""
    # field = ""#
    db_to_search = []
    # object = ""#saves object from db
    type = ""
    pin = ""
    temp_user_date = dict()
    auth_arr = ["name", "number", "address"]
    auth_val_arr = []
    time = ""
    user = ""
    name = ""


multithreading = dict()

# title, author, publisher, edition, genre

# book4 = Book("Jane Eyre", "Charlotte Bronte", "SomePublisher", "1", "SomeGenre","")
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
