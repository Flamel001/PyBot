import pyrebase
import json
from documents import *
from user import *

__config = {
    "apiKey": "AIzaSyATPtq7AeRK5D4u6rP4BhEoPSA3ofiqDaE",
    "authDomain": "telegrambotproject-8f30f.firebaseapp.com",
    "databaseURL": "https://telegrambotproject-8f30f.firebaseio.com",
    "projectId": "telegrambotproject-8f30f",
    "storageBucket": "telegrambotproject-8f30f.appspot.com"
}

__firebase = pyrebase.initialize_app(__config)
__db = __firebase.database()
__users = "Users"
__books = "Books"
__amount_of_books = 0
__list_of_books_available = list()


def insert_user(user_alias, dictionary):
    __db.child(__users).child(str(user_alias)).set(dictionary)


def insert_book(name, dictionary):
    global __amount_of_books, __list_of_books_available
    __amount_of_books += 1
    __list_of_books_available = list()
    __db.child(__books).child(str(name)).set(dictionary)


def get_user(user_alias):
    dictionary = __db.child(__users).child(str(user_alias)).get().val()
    if "student" in dictionary.values():
        student = Student()
        student.setData(dictionary)
        return student
    elif "faculty" in dictionary.values():
        faculty = Faculty()
        faculty.setData(dictionary)
        return faculty
    elif "librarian" in dictionary.values():
        librarian = Librarian()
        librarian.setData(dictionary)
        return librarian


def get_book(name):
    return __db.child(__books).child(str(name)).get().val()


def get_all_librarians_ids():
    all_libs = __db.child(__users).get()
    a = list()
    for lib in all_libs.each():
        if "librarian" in lib.val().values():
            a.append(lib.val()["id"])
    return a


def remove_user(user_alias):
    __db.child(__users).child(str(user_alias)).remove()


def remove_book(name):
    global __amount_of_books, __list_of_books_available
    __amount_of_books -= 1
    __list_of_books_available = list()
    __db.child(__books).child(str(name)).remove()


def separate_json(json_string):
    return json.loads(json_string)


def update_user(user_alias, new_info):
    dictionary = get_user(user_alias)
    print("This is dictionary " + str(dictionary))
    if isinstance(dict, str):
        d = separate_json(dictionary)
    else:
        d = dictionary
    d.update(new_info)
    __db.child(__users).child(str(user_alias)).update(d)


def update_book(name, new_info):
    dictionary = get_book(name)
    if isinstance(dict, str):
        d = separate_json(dictionary)
    else:
        d = dictionary
    d.update(new_info)
    __db.child(__books).child(str(name)).update(d)


def get_all_books():
    global __list_of_books_available
    if not __list_of_books_available:
        all_books = __db.child(__books).get()
        for book in all_books.each():
            print("book is " + str(book.val()))
            book1 = Book()
            book1.setData(book.val())
            __list_of_books_available.append(book1)
    return __list_of_books_available


def get_count_of_different_books():
    global __amount_of_books
    if __amount_of_books == 0:
        __amount_of_books = len(__db.child(__books).get().key())
    return __amount_of_books
