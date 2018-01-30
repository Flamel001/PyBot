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

def insertUser(id, json_string):
    __db.child("Users").child("" + id).set(json_string)


def insertBook(name, json):
    __db.child("Books").child("" + name).set(json)


def getUser(id):
    return __db.child("Users").child("" + id).get().val()


def getBook(name):
    return __db.child("Books").child("" + name).get().val()


def create_json_stirng(name, email, rank):
    d = {}
    d["name"] = name
    d["email"] = email
    d["rank"] = rank
    return json.dumps(d)


def separate_json(json_string):
    return json.loads(json_string)


def updateRank(id, new_rank):
    d = separate_json(getUser("" + id))
    d["rank"] = new_rank
    __db.child("Users").child("" + id).update(d)