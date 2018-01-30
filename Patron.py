import datetime


class Patron():

    def __init__(self, name, mail, number, alias):
        self.__user_name = name
        self.__user_mail = mail
        self.__phone_number = number
        self.__user_alias = alias
        self.__user_rating = 5
        self.__user_documents = dict
        self.__registration_date = datetime.datetime.now()

    def get_name(self):
        return self.__user_name

    def set_name(self, new_name):
        self.__user_name = new_name

    def get_mail(self):
        return self.__user_mail

    def set_mail(self, new_mail):
        self.__user_mail = new_mail

    def get_number(self):
        return self.__phone_number

    def set_number(self, new_number):
        self.__phone_number = new_number

    def get_alias(self):
        return self.__user_alias

    def set_alias(self, new_alias):
        self.__user_alias = new_alias

    def decrease_rating(self):
        self.__user_rating -= 1

    def set_id(self, ID):
        self.__user_ID = ID

    def get_id(self):
        return self.__user_ID

    def add_document(self, id):
        current_date = datetime.datetime.now()
        self.__user_documents[id] = current_date

    def remove_document(self, id):
        self.__user_documents.pop(id)

    def get_rating(self):
        return self.__user_rating

    def get_registration_date(self):
        return self.__registration_date

    def set_documents_duration(self, dur):
        self.__documents_duration = dur

    def get_documents_duration(self):
        return self.__documents_duration


class Student(Patron):

    def __init__(self, name, mail, number, alias):
        super().__init__(name, mail, number, alias)
        self.set_documents_duration(3)

class Professor(Patron):

    def __init__(self, name, mail, number, alias):
        super().__init__(name, mail, number, alias)
        self.set_documents_duration(4)

