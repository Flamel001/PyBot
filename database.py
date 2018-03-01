import pyrebase
import json

__config = {
    "apiKey": "AIzaSyATPtq7AeRK5D4u6rP4BhEoPSA3ofiqDaE",
    "authDomain": "telegrambotproject-8f30f.firebaseapp.com",
    "databaseURL": "https://telegrambotproject-8f30f.firebaseio.com",
    "projectId": "telegrambotproject-8f30f",
    "storageBucket": "telegrambotproject-8f30f.appspot.com"
}

__firebase = pyrebase.initialize_app(__config)
__db = __firebase.database()
__patrons = "Patrons"
__books = "Books"
__libs = "Libs"


def insert_patron(patron_id, dictionary):
    __db.child(__patrons).child(str(patron_id)).set(dictionary)


def insert_book(name, dictionary):
    __db.child(__books).child(str(name)).set(dictionary)


def insert_librarian(librarian_id, dictionary):
    __db.child(__libs).child(str(librarian_id)).set(dictionary)


def get_patron(patron_id):
    return __db.child(__patrons).child(str(patron_id)).get().val()


def get_book(name):
    return __db.child(__books).child(str(name)).get().val()


def get_all_librarians():
    all_libs = __db.child(__libs).get()
    a = list()
    for lib in all_libs.each():
        a.append(lib.key())
    return a


def remove_patron(patron_id):
    __db.child(__patrons).child(str(patron_id)).remove()


def remove_book(name):
    __db.child(__books).child(str(name)).remove()


def remove_librarian(librarian_id):
    __db.child(__libs).child(str(librarian_id)).remove()


def separate_json(json_string):
    return json.loads(json_string)


def update_patron(patron_id, new_info):
    dictionary = get_patron(patron_id)
    if isinstance(dict, str):
        d = separate_json(dictionary)
    else:
        d = dictionary
    d.update(new_info)
    __db.child(__patrons).child(str(id)).update(d)


def update_book(name, new_info):
    dictionary = get_book(name)
    if isinstance(dict, str):
        d = separate_json(dictionary)
    else:
        d = dictionary
    d.update(new_info)
    __db.child(__books).child(str(name)).update(d)


def get_all_books():
    dictionary = dict()
    all_books = __db.child(__books).get()
    for book in all_books.each():
        dictionary[book.key()] = book.val()
    return dictionary


def get_list_of_books():
    books = []
    dict = get_all_books()
    for book in dict:
        books.append(book)
    return books