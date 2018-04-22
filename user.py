import documents as dc
import datetime
import database as db
from dict_keys import *
from utilities import get_date


class User:
    pass


class Admin(User):

    def __init__(self):
        self.__name = ""
        self.__alias = ""
        self.__address = ""
        self.__mail = ""

    def get_mail(self):
        return self.__mail

    def give_priv(self, librarian_id, priv):
        db.get(id=librarian_id)[0].set_priv(priv)

        lib_id = str(librarian_id)
        priv_str = str(priv)
        date = get_date()
        db.insert_log(date + " |  " + "Admin set to Librarian(" + lib_id + ") priveleg: " + priv_str)

    def add_librarian(self, id, alias, name, mail, number, address, priv):
        new = Librarian(id, alias, name, mail, number, address, priv)
        db.insert(new.summary())

        id_str = str(id)
        date = get_date()
        db.insert_log(date + " | Admin added Librarian with ID: " + id_str)

    def delete_librarian(self, librarian_id):
        db.delete(id=librarian_id)

        id_str = str(librarian_id)
        date = get_date()
        db.insert_log(date + " | Admin deleted Librarian with ID: " + id_str)

    def get_log(self):
        log = db.get_all_similar_info(log="kek")
        log_file = open("log.txt", 'w')
        for record in log:
            log_file.write(record + "\n")
        return log_file


class Librarian(User):

    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, priv=1):
        self.__info = dict()
        self.__info[user_id] = id
        self.__info[user_alias] = alias
        self.__info[user_name] = name
        self.__info[user_mail] = mail
        self.__info[user_number] = number
        self.__info[user_address] = address
        self.__info[user_type] = "Librarian"
        self.__info[librarian_priv] = priv

    def new_book(self, title, author, publisher, year, edition, genre, url, bestseller, reference):
        if self.get_priv() >= 2:
            print(
                "these are the fields " + title + ", " + author + ", " + publisher + ", " + year + "," + edition + ", " + genre + ", " + url)
            new = dc.Book(title, author, publisher, year, edition, genre, url, bestseller, reference)
            print("this is book summary " + str(new.summary()))
            db.insert(new.summary())

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(title)
            db.insert_log(date + " | Librarian(" + id_str + ") added book: " + title_str)
        else:
            return
            # return new

    def add_copy_for_doc(self, original: dc.Document, copy_id):
        if self.get_priv() == 3:
            original.add_copy(copy_id)
            db.update(title=original.get_title(), copies=original.get_list_of_copies())

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(original.get_title())
            db.insert_log(date + " | Librarian(" + id_str + ") added copy for book: " + title_str)
        else:
            return

    def set_book_bestseller(self, book, is_not):
        book.set_bestseller(is_not)

    def new_article(self, title, author, journal, publication_date, editor, url):
        if self.get_priv() >= 2:
            new = dc.Article(title, author, journal, publication_date, editor, url)
            db.insert(new.summary())

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(title)
            db.insert_log(date + " | Librarian(" + id_str + ") added article: " + title_str)
        else:
            return
            # return new

    def new_AV_material(self, title, author, value, url):
        if self.get_priv() >= 2:
            new = dc.AV_Materials(title, author, value, url)
            print("avmaterial " + str(new.summary()))
            db.insert(new.summary())

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(title)
            db.insert_log(date + " | Librarian(" + id_str + ") added AV: " + title_str)
        else:
            return

    def new_student(self, id, alias, name, mail, number, address):
        if self.get_priv() >= 2:
            new = Student(id, alias, name, mail, number, address)
            db.insert(new.summary())

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(id)
            db.insert_log(date + " | Librarian(" + id_str + ") added Student with ID: " + title_str)
        else:
            return

    def new_instructor(self, id, alias, name, mail, number, address):
        if self.get_priv() >= 2:
            new = Instructor(id, alias, name, mail, number, address)
            db.insert(new.summary())

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(id)
            db.insert_log(date + " | Librarian(" + id_str + ") added Instructor with ID: " + title_str)
        else:
            return

    def new_ta(self, id, alias, name, mail, number, address):
        if self.get_priv() >= 2:
            new = TA(id, alias, name, mail, number, address)
            db.insert(new.summary())

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(id)
            db.insert_log(date + " | Librarian(" + id_str + ") added TA with ID: " + title_str)
        else:
            return

    def new_professor(self, id, alias, name, mail, number, address):
        if self.get_priv() >= 2:
            new = Professor(id, alias, name, mail, number, address)
            db.insert(new.summary())

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(id)
            db.insert_log(date + " | Librarian(" + id_str + ") added Professor with ID: " + title_str)
        else:
            return

    def new_vp(self, id, alias, name, mail, number, address):
        if self.get_priv() >= 2:
            new = VP(id, alias, name, mail, number, address)
            db.insert(new.summary())

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(id)
            db.insert_log(date + " | Librarian(" + id_str + ") added Visiting Prof. with ID: " + title_str)
        else:
            return

    def remove_user(self, alias):
        if self.get_priv() == 3:
            id = db.get(alias=alias)[0].get_id
            db.delete(id)

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(db.get(alias=alias)[0].get_id())
            db.insert_log(date + " | Librarian(" + id_str + ") removed user with id: " + title_str)
        else:
            return

    def remove_document(self, title):
        if self.get_priv() == 3:
            db.delete(title)

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(title)
            db.insert_log(date + " | Librarian(" + id_str + ") removed Document with title: " + title_str)
        else:
            return

    def get_user(self, alias):
        return db.get(alias=alias)

    def get_doc(self, title):
        return db.get(title=title)

    def get_name(self):
        return self.__info[user_name]

    def set_name(self, new):
        db.update(id=self.get_id(), name=new)
        self.__info[user_name] = new

    def get_mail(self):
        return self.__info[user_mail]

    def set_mail(self, new):
        db.update(id=self.get_id(), mail=new)
        self.__info[user_mail] = new

    def get_number(self):
        return self.__info[user_number]

    def set_number(self, new):
        db.update(id=self.get_id(), number=new)
        self.__info[user_number] = new

    def get_alias(self):
        return self.__info[user_alias]

    def set_alias(self, new):
        db.update(id=self.get_id(), alias=new)
        self.__info[user_alias] = new

    def get_id(self):
        return self.__info[user_id]

    def set_id(self, id):
        db.update(id=self.get_id(), new_id=id)
        self.__info[user_id] = id

    def get_address(self):
        return self.__info[user_address]

    def set_address(self, address):
        db.update(id=self.get_id(), address=address)
        self.__info[user_address] = address

    def summary(self):
        return self.__info

    def get_type(self):
        return self.__info[user_type]

    def get_priv(self):
        return self.__info[librarian_priv]

    def set_priv(self, new_priv):
        db.update(id=self.get_id(), privilege=new_priv)
        self.__info[librarian_priv] = new_priv

    # TO_DO outstanding request
    def set_outstanding(self, title):
        if self.get_priv() >= 2:
            book = db.get(title=title)[0]
            book.set_outstanding()

            id_str = str(self.get_id())
            date = get_date()
            title_str = str(title)
            db.insert_log(date + " | Librarian(" + id_str + ") marked Document " + title_str + " as outstanding")
        else:
            return


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
        if id != "" or id != None:
            db.update(id=self.get_id(), new_id=id)
        self.__info[user_id] = id

    def get_name(self):
        return self.__info[user_name]

    def set_name(self, new_name):
        if new_name != "" or new_name != None:
            db.update(id=self.get_id(), name=new_name)
        self.__info[user_name] = new_name

    def get_mail(self):
        return self.__info[user_mail]

    def set_mail(self, new_mail):
        if new_mail != "" or new_mail != None:
            db.update(id=self.get_id(), mail=new_mail)
        self.__info[user_mail] = new_mail

    def get_number(self):
        return self.__info[user_number]

    def set_number(self, new_number):
        if new_number != "" or new_number != None:
            db.update(id=self.get_id(), number=new_number)
        self.__info[user_number] = new_number

    def get_alias(self):
        return self.__info[user_alias]

    def set_alias(self, new_alias):
        if new_alias != "" or new_alias != None:
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
        if new_list != "" or new_list != None:
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
        if debt != "" or debt != None:
            db.update(id=self.get_id(), debt=debt)
        self.__info[user_debt] = debt

    def summary(self):
        return self.__info

    def get_address(self):
        return self.__info[user_address]

    def set_address(self, address):
        if address != "" or address != None:
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
            self.__info[user_type] = "Student"
            self.__info[user_priority] = 5
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.__info[user_type] = "Student"
            self.__info[user_priority] = 5


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
            self.__info[user_type] = "Instructor"
            self.__info[user_priority] = 4
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.__info[user_type] = "Instructor"
            self.__info[user_priority] = 4


class TA(Faculty):
    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=list()):
        if reg_date:
            super().__init__(id, alias, name, mail, number, address, reg_date, debt, doc_list)
            self.__info = super().summary()
            self.__info[user_type] = "TA"
            self.__info[user_priority] = 3
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.__info[user_type] = "TA"
            self.__info[user_priority] = 3

class Professor(Faculty):
    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=list()):
        if reg_date:
            super().__init__(id, alias, name, mail, number, address, reg_date, debt, doc_list)
            self.__info = super().summary()
            self.__info[user_type] = "Professor"
            self.__info[user_priority] = 1
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.__info[user_type] = "Professor"
            self.__info[user_priority] = 1


class VP(Faculty):
    def __init__(self, id=None, alias=None, name=None, mail=None, number=None, address=None, reg_date=None, debt=0,
                 doc_list=list()):
        if reg_date:
            super().__init__(id, alias, name, mail, number, address, reg_date, debt, doc_list)
            self.__info = super().summary()
            self.__info[user_type] = "VP"
            self.__info[user_priority] = 2
        else:
            super().__init__(id, alias, name, mail, number, address, debt=debt, doc_list=doc_list)
            self.__info = super().summary()
            self.__info[user_type] = "VP"
            self.__info[user_priority] = 2
