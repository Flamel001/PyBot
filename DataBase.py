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
    __db.child("Users").child("" + id).set(dict)


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
    __db.child("Users").child("" + id).update(d)