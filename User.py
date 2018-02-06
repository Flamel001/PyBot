import datetime
import Documents as dc


class User:
    pass


class Librarian(User):

    def __init__(self, name, mail, number, alias, ID):
        self.__librarian_name = name
        self.__librarian_mail = mail
        self.__phone_number = number
        self.__librarian_alias = alias
        self.__librarian_id = ID
        self.__rank = 2

    def __init__(self, dictionary):
        temp = dict(dictionary)
        name = temp.pop("Librarian name")
        mail = temp.pop("Librarian mail")
        number = temp.pop("Librarian number")
        alias = temp.pop("Librarian alias")

        self.__librarian_name = name
        self.__librarian_mail = mail
        self.__phone_number = number
        self.__librarian_alias = alias
        self.__rank = 2

    def new_book(self, title, author, publisher, edition, genre):
        new = dc.Book
        new.__init__(title, author, publisher, edition, genre)
        return new

    def set_book_bestseller(self, book, is_not):
        book.set_bestseller(is_not)

    def new_article(self, title, author, journal, publication_date, editor):
        new = dc.Article
        new.__init__(title, author, journal, publication_date, editor)
        return new

    def new_AV_material(self, title, author, value):
        new = dc.AV_Materials
        new.__init__(title, author, value)
        return new

    def get_name(self):
        return self.__librarian_name

    def get_mail(self):
        return self.__librarian_mail

    def get_number(self):
        return self.__phone_number

    def get_alias(self):
        return self.__librarian_alias

    def get_rank(self):
        return self.__rank

    def get_ID(self):
        return self.__librarian_id

    def summary(self):
        d = dict()
        d["Librarian name"] = self.get_name()
        d["Librarian mail"] = self.get_mail()
        d["Librarian number"] = self.get_number()
        d["Librarian alias"] = self.get_alias()
        d["Librarian ID"] = self.get_ID()
        return d

class Patron(User):

    def __init__(self, name, mail, number, alias):
        self.__user_name = name
        self.__user_mail = mail
        self.__phone_number = number
        self.__user_alias = alias
        self.__user_rating = 5
        self.__user_documents = dict
        self.__registration_date = datetime.datetime.now()
        self.__user_debt = 0

    def __init__(self, dictionary):
        temp = dict(dictionary)
        name = temp.pop("User name")
        mail = temp.pop("User mail")
        number = temp.pop("User number")
        alias = temp.pop("User alias")
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

    def get_docs_list(self):
        list = []
        for doc in self.__user_documents:
            list.append(doc)
        return list

    def get_rating(self):
        return self.__user_rating

    def get_registration_date(self):
        return self.__registration_date

    def set_documents_duration(self, dur):
        self.__documents_duration = dur

    def get_documents_duration(self):
        return self.__documents_duration

    def get_rank(self):
        return self.__rank

    def increase_debt(self, value):
        self.__user_debt += value

    def decrease_debt(self,value):
        self.__user_debt -= value

    def get_debt(self):
        return self.__user_debt

    def summary(self):
        d = dict()
        d["User name"] = self.get_name()
        d["User mail"] = self.get_mail()
        d["User number"] = self.get_number()
        d["User alias"] = self.get_alias()
        d["User rating"] = self.get_rating()
        d["User ID"] = self.get_id()
        d["User's books duration"] = self.get_documents_duration()
        d["Users documents"] = self.get_docs_list()
        d["Users rank"] = self.get_rank()
        d["User debt"] = self.get_debt()
        return d


class Student(Patron):

    def __init__(self, name, mail, number, alias):
        super().__init__(name, mail, number, alias)
        self.set_documents_duration(3)
        self.__rank = 0

    def __init__(self, dictionary):
        temp = dict(dictionary)
        name = temp.pop("User name")
        mail = temp.pop("User mail")
        number = temp.pop("User number")
        alias = temp.pop("User alias")
        debt = temp.pop("User debt")
        super().__init__(name, mail, number, alias)
        self.set_documents_duration(3)
        self.__rank = 0
        self.increase_debt(debt)


class Faculty(Patron):

    def __init__(self, name, mail, number, alias):
        super().__init__(name, mail, number, alias)
        self.set_documents_duration(4)
        self.__rank = 1

    def __init__(self, dictionary):
        temp = dict(dictionary)
        name = temp.pop("User name")
        mail = temp.pop("User mail")
        number = temp.pop("User number")
        alias = temp.pop("User alias")
        debt = temp.pop("User debt")
        super().__init__(name, mail, number, alias)
        self.set_documents_duration(4)
        self.__rank = 1
        self.increase_debt(debt)
