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
__books = "Docs"
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
    print("dict in get_user " + str(dictionary))
    if dictionary:
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
    return None


def get_doc(name):
    dictionary = __db.child(__books).child(str(name)).get().val()
    print("dict in get_doc " + str(dictionary))
    if dictionary:
        if "book" in dictionary.values():
            book = Book()
            book.setData(dictionary)
            return book
        elif "article" in dictionary.values():
            article = Article()
            article.setData(dictionary)
            return article
        elif "av" in dictionary.values():
            av = AV_Materials()
            av.setData(dictionary)
            return av
    return None


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
    user = get_user(user_alias)
    if "document_list" in new_info:
        user.set_docs_list(new_info["document_list"])
        new_info.pop("document_list")
    dictionary = user.summary()
    dictionary.update(new_info)
    # json_str = json.dumps(dictionary)
    # print("This is summary of user " + str(json_str))
    __db.child(__users).child(str(user_alias)).update(dictionary)


def update_book(name, new_info):
    global __list_of_books_available
    print("new_info " + str(new_info))
    doc = get_doc(name)
    if "copies" in new_info:
        print("doc in update book before " + str(doc.get_list_of_copies()))
        print(str(new_info))
        doc.set_list_of_copies(new_info["copies"])
        print("doc in update book " + str(doc.get_list_of_copies()))
        new_info.pop("copies")
    d = doc.summary()
    d.update(new_info)
    __db.child(__books).child(str(name)).update(d)
    __list_of_books_available = list()


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
        __amount_of_books = len(__db.child(__books).get().each())
    return __amount_of_books
