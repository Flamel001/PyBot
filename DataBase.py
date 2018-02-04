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
    d = separate_json(getUser("" + id))
    d.update(new_info)
    __db.child("Users").child("" + str(id)).update(d)


def dictForBook(description, ref):
    d = {}
    d["description"] = description
    d["reference"] = ref
    return d


def user_name(name):
    return name


def user_surname(surname):
    return surname


def user_mail(mail):
    return mail


def user_num(number):
    return number


def dictForUser(email, name, surname, number):
    d = {}
    d["email"] = user_mail(email)
    d["name"] = user_name(name)
    d["surname"] = user_surname(surname)
    d["number"] = user_num(number)
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