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


def insertUser(id, dict):
    __db.child("Users").child("" + str(id)).set(dict)


def insertBook(name, dict):
    __db.child("Books").child("" + name).set(dict)


def getUser(id):
    return __db.child("Users").child("" + id).get().val()


def getBook(name):
    return __db.child("Books").child("" + name).get().val()


def separate_json(json_string):
    return json.loads(json_string)


def updateRank(id, new_info):
    dict = getUser(str(id))
    if(type(dict)==type("")):
        d = separate_json(dict)
    else:
        d = dict
    d.update(new_info)
    __db.child("Users").child("" + str(id)).update(d)


def dictForBook(description=None, ref=None):
    d = dict()
    if description:
        d["description"] = description
    if ref:
        d["reference"] = ref
    return d


def dictForUser(email=None, name=None, surname=None, number=None):
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


def printAllUsers():
    allUser = __db.child("Users").get()
    for user in allUser.each():
        print("UserKey " + user.key())
        print("UserVal " + json.dumps(user.val()))


def printAllBooks():
    allBooks = __db.child("Books").get()
    for book in allBooks.each():
       print("BookKey " + book.key())
       print("BookVal " + json.dumps(book.val()))