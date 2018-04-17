import documents as dc
import datetime
import database as db
from dict_keys import *


class User:
    pass


class Librarian(User):

    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None):
        self.__info = dict()
        self.__info[user_id] = id
        self.__info[user_alias] = alias
        self.__info[user_name] = name
        self.__info[user_mail] = mail
        self.__info[user_number] = number
        self.__info[user_address] = address
        self.__info[user_type] = "Librarian"

    def new_book(self, title, author, publisher, year, edition, genre, url, bestseller, reference):
        print(
            "these are the fields " + title + ", " + author + ", " + publisher + ", " + year + "," + edition + ", " + genre + ", " + url)
        new = dc.Book(title, author, publisher, year, edition, genre, url, bestseller, reference)
        print("this is book summary " + str(new.summary()))
        db.insert(new.summary())
        # return new

    def add_copy_for_doc(self, original: dc.Document, copy_id):
        original.add_copy(copy_id)
        self.modify_book(original, original.get_list_of_copies())

    def set_book_bestseller(self, book, is_not):
        book.set_bestseller(is_not)

    def new_article(self, title, author, journal, publication_date, editor, url):
        new = dc.Article(title, author, journal, publication_date, editor, url)
        db.insert(new.summary())
        # return new

    def new_AV_material(self, title, author, value, url):
        new = dc.AV_Materials(title, author, value, url)
        print("avmaterial " + str(new.summary()))
        db.insert(new.summary())
        # return new

    def new_student(self, id, name, mail, number, alias, address):
        new = Student(id, name, mail, number, alias, address)
        db.insert(new.summary())
        # return new

    def new_faculty(self, id, name, mail, number, alias, address):
        new = Faculty(id, name, mail, number, alias, address)
        db.insert(new.summary())
        # return new

    def remove_user(self, alias):
        id = db.get(alias=alias)[0].get_id
        db.delete(id)

    def remove_document(self, title):
        db.delete(title)

    def modify_user(self, user_alias, new_name=None, new_mail=None, new_number=None, new_alias=None, new_rating=None,
                    new_doc_list=None, new_debt=None):
        dictionary = dict()
        if new_name:
            dictionary[user_name] = new_name
        if new_mail:
            dictionary[user_mail] = new_mail
        if new_number:
            dictionary[user_number] = new_number
        if new_alias:
            dictionary[user_alias] = new_alias
        if new_rating:
            dictionary[user_rating] = new_rating
        if new_doc_list:
            dictionary[user_document_list] = new_doc_list
        if new_debt:
            dictionary[user_debt] = new_debt

        db.update_user(user_alias, dictionary)

    def modify_book(self, book_title, new_title=None, new_author=None, new_publisher=None, new_edition=None,
                    new_genre=None, new_price=None, bestseller=None, reference=None, new_keywords=None, new_copies=None,
                    new_duration=None, new_url=None):
        dictionary = dict()
        if new_title:
            dictionary[document_title] = new_title
        if new_author:
            dictionary[document_author] = new_author
        if new_publisher:
            dictionary[book_publisher] = new_publisher
        if new_edition:
            dictionary[book_edition] = new_edition
        if new_genre:
            dictionary[book_genre] = new_genre
        if new_price:
            dictionary[document_price] = new_price
        if bestseller:
            dictionary[book_bestseller] = bestseller
        if reference:
            dictionary[book_is_reference] = reference
        if new_keywords:
            dictionary[document_keywords] = new_keywords
            dictionary[document_keywords_count] = len(new_keywords)
        if new_copies:
            dictionary[document_copies] = new_copies
        if new_duration:
            dictionary[document_duration] = new_duration
        if new_url:
            dictionary[document_url] = new_url

        db.update_book(book_title, dictionary)

    def modify_article(self, article_title, new_title=None, new_author=None, new_journal=None, new_pub_date=None,
                       new_editor=None, new_price=None, new_keywords=None, new_copies=None,
                       new_duration=None, new_url=None):
        dictionary = dict()
        if new_title:
            dictionary[document_title] = new_title
        if new_author:
            dictionary[document_author] = new_author
        if new_journal:
            dictionary[article_journal] = new_journal
        if new_pub_date:
            dictionary[article_pub_date] = new_pub_date
        if new_editor:
            dictionary[article_editor] = new_editor
        if new_price:
            dictionary[document_price] = new_price
        if new_keywords:
            dictionary[document_keywords] = new_keywords
            dictionary[document_keywords_count] = len(new_keywords)
        if new_copies:
            dictionary[document_copies] = new_copies
        if new_duration:
            dictionary[document_duration] = new_duration
        if new_url:
            dictionary[document_url] = new_url
        db.update_book(article_title, dictionary)

    def modify_AV(self, AV_title, new_title=None, new_author=None, new_price=None, new_keywords=None, new_copies=None,
                  new_duration=None, new_url=None):
        dictionary = dict()
        if new_title:
            dictionary[document_title] = new_title
        if new_author:
            dictionary[document_author] = new_author
        if new_price:
            dictionary[document_price] = new_price
        if new_keywords:
            dictionary[document_keywords] = new_keywords
            dictionary[document_keywords_count] = len(new_keywords)
        if new_copies:
            dictionary[document_copies] = new_copies
        if new_duration:
            dictionary[document_duration] = new_duration
        if new_url:
            dictionary[document_url] = new_url

        db.update_book(AV_title, dictionary)

    def get_user(self, alias):
        return db.get(alias=alias)

    def get_doc(self, title):
        return db.get(title=title)

    def get_name(self):
        return self.__info[user_name]

    def set_name(self, new):
        self.__info[user_name] = new

    def get_mail(self):
        return self.__info[user_mail]

    def set_mail(self, new):
        self.__info[user_mail] = new

    def get_number(self):
        return self.__info[user_number]

    def set_number(self, new):
        self.__info[user_number] = new

    def get_alias(self):
        return self.__info[user_alias]

    def set_alias(self, new):
        self.__info[user_alias] = new

    def get_id(self):
        return self.__info[user_id]

    def set_id(self, id):
        self.__info[user_id] = id

    def get_address(self):
        return self.__info[user_address]

    def set_address(self, address):
        self.__info[user_address] = address

    def summary(self):
        return self.__info

    def get_type(self):
        return self.__info[user_type]


class Patron(User):

    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=None):
        if doc_list is None:
            doc_list = dict()
        self.__info = dict()
        self.__info[user_id] = id
        self.__info[user_alias] = alias
        self.__info[user_name] = name
        self.__info[user_mail] = mail
        self.__info[user_number] = number
        self.__info[user_address] = address
        self.__info[user_type] = ""
        if reg_date:
            self.__info[user_registration_date] = reg_date
        else:
            self.__info[user_registration_date] = str(datetime.datetime.now())
        self.__info[user_document_list] = doc_list
        self.__info[user_debt] = debt
        self.__info[user_priority] = 0

    def get_id(self):
        return self.__info[user_id]

    def set_id(self, id):
        db.update(id=self.get_id(), new_id=id)
        self.__info[user_id] = id

    def get_name(self):
        return self.__info[user_name]

    def set_name(self, new_name):
        db.update(id=self.get_id(), name=new_name)
        self.__info[user_name] = new_name

    def get_mail(self):
        return self.__info[user_mail]

    def set_mail(self, new_mail):
        db.update(id=self.get_id(), mail=new_mail)
        self.__info[user_mail] = new_mail

    def get_number(self):
        return self.__info[user_number]

    def set_number(self, new_number):
        db.update(id=self.get_id(), number=new_number)
        self.__info[user_number] = new_number

    def get_alias(self):
        return self.__info[user_alias]

    def set_alias(self, new_alias):
        db.update(id=self.get_id(), alias=new_alias)
        self.__info[user_alias] = new_alias

    def remove_document(self, title):
        self.__info[user_document_list].pop(title)
        new_doc_list = self.get_docs_list()
        db.update(id=self.get_id(), docs=new_doc_list)

    def add_document(self, title, date):
        self.__info[user_document_list][title] = date
        new_doc_list = self.get_docs_list()
        db.update(id=self.get_id(), docs=new_doc_list)

    def has_book(self, title):
        for key in self.__info[user_document_list].keys():
            if title == key.split("_")[0]:
                return True
            else:
                return False

    def get_docs_list(self):
        temp = dict(self.__info[user_document_list])
        print("docs list is " + str(self.__info[user_document_list]))
        return temp

    def set_docs_list(self, new_list):
        print("doc list in user " + str(type(new_list)))
        temp = dict(new_list)
        db.update(id=self.get_id(), docs=new_list)
        self.__info[user_document_list] = temp

    def get_registration_date(self):
        return self.__info[user_registration_date]

    def increase_debt(self, value):
        old_debt = self.get_debt()
        new_debt = old_debt + value
        db.update(id=self.get_id(), debt=new_debt)
        self.__info[user_debt] = new_debt

    def decrease_debt(self, value):
        old_debt = self.get_debt()
        new_debt = old_debt - value
        db.update(id=self.get_id(), debt=new_debt)
        self.__info[user_debt] = new_debt

    def get_debt(self):
        return self.__info[user_debt]

    def set_debt(self, debt):
        db.update(id=self.get_id(), debt=debt)
        self.__info[user_debt] = debt

    def summary(self):
        return self.__info

    def get_address(self):
        return self.__info[user_address]

    def set_address(self, address):
        db.update(id=self.get_id(), address=address)
        self.__info[user_address] = address

    def get_type(self):
        return self.__info[user_type]

    def get_prior(self):
        return self.__info[user_priority]

    def set_prior(self, prior):
        self.__info[user_priority] = prior

    def set_type(self, type):
        self.__info[user_type] = type


class Student(Patron):

    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=list()):
        if reg_date:
            super().__init__(id, alias, name, mail, number, address, reg_date, debt, doc_list)
            self.__info = super().summary()
            self.set_type("Student")
            self.set_prior(5)
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.set_type("Student")
            self.set_prior(5)


class Faculty(Patron):

    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=list()):
        if reg_date:
            super().__init__(id, alias, name, mail, number, address, reg_date, debt, doc_list)
            self.__info = super().summary()
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()


class Instructor(Faculty):
    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=list()):
        if reg_date:
            super().__init__(id, alias, name, mail, number, address, reg_date, debt, doc_list)
            self.__info = super().summary()
            self.set_type("Instructor")
            self.set_prior(4)
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.set_type("Instructor")
            self.set_prior(4)


class TA(Faculty):
    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=list()):
        if reg_date:
            super().__init__(id, alias, name, mail, number, address, reg_date, debt, doc_list)
            self.__info = super().summary()
            self.set_type("TA")
            self.set_prior(3)
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.set_type("TA")
            self.set_prior(3)


class Professor(Faculty):
    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=list()):
        if reg_date:
            super().__init__(id, alias, name, mail, number, address, reg_date, debt, doc_list)
            self.__info = super().summary()
            self.set_type("Professor")
            self.set_prior(1)
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.set_type("Professor")
            self.set_prior(1)


class VP(Faculty):
    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=list()):
        if reg_date:
            super().__init__(id, alias, name, mail, number, address, reg_date, debt, doc_list)
            self.__info = super().summary()
            self.set_type("VP")
            self.set_prior(2)
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.set_type("VP")
            self.set_prior(2)
