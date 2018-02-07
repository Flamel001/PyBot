import pyrebase
import json
import types

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


def insert_user(id, dict):
    __db.child(__users).child(str(id)).set(dict)


def insert_book(name, dict):
    __db.child(__books).child(str(name)).set(dict)


def get_user(id):
    return __db.child(__users).child(str(id)).get().val()


def get_book(name):
    return __db.child(__books).child(str(name)).get().val()


def remove_user(id):
    __db.child(__users).child(str(id)).remove()


def remove_book(name):
    __db.child(__books).child(str(name)).remove()


def separate_json(json_string):
    return json.loads(json_string)


def update_user(id, new_info):
    dict = get_user(str(id))
    if isinstance(dict, str):
        d = separate_json(dict)
    else:
        d = dict
    d.update(new_info)
    __db.child(__users).child(str(id)).update(d)


def update_book(name, new_info):
    dict = get_book(name)
    if isinstance(dict, str):
        d = separate_json(dict)
    else:
        d = dict
    d.update(new_info)
    __db.child(__books).child(str(name)).update(d)


def dict_for_book(description=None, ref=None):
    d = dict()
    if description:
        d["description"] = description
    if ref:
        d["reference"] = ref
    return d


def dict_for_user(email=None, name=None, surname=None, number=None):
    d = dict()
    if email:
        d["email"] = email
    if name:
        d["name"] = name
    if surname:
        d["surname"] = surname
    if number:
        d["number"] = number
    return d


def all_books():
    dict={}
    all_books = __db.child(__books).get()
    for book in all_books.each():
        dict[book.key()] = book.val()
    return dict

def list_of_all_books():
    books_list=[]
    for key in all_books().keys():
        books_list.append(key)
    return books_list


def print_all_users():
    all_users = __db.child(__users).get()
    for user in all_users.each():
        print("UserKey " + user.key())
        print("UserVal " + json.dumps(user.val()))


def print_all_books():
    all_books = __db.child(__books).get()
    for book in all_books.each():
       print("BookKey " + book.key())
       print("BookVal " + json.dumps(book.val()))