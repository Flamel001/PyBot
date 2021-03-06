import database as db
import user


def check(alias):
    if alias:
        info = db.get(alias=alias)
        if len(info)>0:
            return True
        else:
            return False


def check_doc(dictionary):
    if dictionary and "type" in dictionary.keys():
        type = dictionary["type"]
        if type == "Book" or type == "AV" or type == "Article":
            return dictionary["title"]
        else:
            return None


def check_user(dictionary):
    if dictionary and "type" in dictionary.keys():
        type = dictionary["type"]
        if type == "Student" or type == "VP" or type == "TA" or type == "Instructor" or type == "Professor":
            return dictionary["id"]
        else:
            return None