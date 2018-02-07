import datetime
import documents as dc


class User:
    pass


user_name = "name"
user_mail = "mail"
user_number = "phoneNumber"
user_alias = "alias"
user_rating = "rating"
user_document_duration = "document_duration"
user_document_list = "document_list"
user_rank = "rank"
user_debt = "debt"


class Librarian(User):

    def __init__(self, name, mail, number, alias):
        self.__librarian_name = name
        self.__librarian_mail = mail
        self.__phone_number = number
        self.__librarian_alias = alias
        # self.__librarian_id = ID
        self.__rank = 2

    def setData(self, dictionary):
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

    # def get_ID(self):
    #     return self.__librarian_id

    def summary(self):
        d = dict()
        d["Librarian name"] = self.get_name()
        d["Librarian mail"] = self.get_mail()
        d["Librarian number"] = self.get_number()
        d["Librarian alias"] = self.get_alias()
        # d["Librarian ID"] = self.get_ID()
        return d


class Patron(User):

    def __init__(self, name, mail, number, alias):
        self.__user_name = name
        self.__user_mail = mail
        self.__phone_number = number
        self.__user_alias = alias
        self.__user_rating = 5
        self.__user_documents = dict()
        self.__registration_date = datetime.datetime.now()
        self.__user_debt = 0
        self.__rank = 3

    def setData(self, dictionary):
        temp = dict(dictionary)
        name = temp.pop("User name")
        mail = temp.pop("User mail")
        number = temp.pop("User number")
        alias = temp.pop("User alias")
        self.__user_name = name
        self.__user_mail = mail
        self.__phone_number = number
        self.__user_alias = alias
        self.__user_rating = temp.pop("")
        self.__user_documents = dict()
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

    # def set_id(self, ID):
    #     self.__user_ID = ID

    # def get_id(self):
    #     return self.__user_ID

    def add_document(self, book):
        if not book.get_is_reference():
            init_date = datetime.datetime.toordinal(datetime.datetime.today())
            if(self.get_rank() == 1):
                exp_date = datetime.datetime.fromordinal(init_date + 28)
            elif(self.get_rank() == 0):
                if book.get_is_bestseller():
                    exp_date = datetime.datetime.fromordinal(init_date + 14)
                else:
                    exp_date = datetime.datetime.fromordinal(init_date + 21)

            self.__user_documents[str(book.get_title())] = book.get_title() + " " + str(exp_date.date())
            return "DONE. You will have to return this book untill:" + str(exp_date)
        else:
            return "The book is unavailable"

    def remove_document(self, id):
        self.__user_documents.pop(id)

    def get_docs_list(self):
        return str(self.__user_documents.values())

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

    def decrease_debt(self, value):
        self.__user_debt -= value

    def get_debt(self):
        return self.__user_debt

    def summary(self):
        d = dict()
        d[user_name] = self.get_name()
        d[user_mail] = self.get_mail()
        d[user_number] = self.get_number()
        d[user_alias] = self.get_alias()
        d[user_rating] = self.get_rating()
        d[user_document_duration] = self.get_documents_duration()
        d[user_document_list] = self.get_docs_list()
        d[user_rank] = self.get_rank()
        d[user_debt] = self.get_debt()
        return d


class Student(Patron):

    def __init__(self, name, mail, number, alias):
        super().__init__(name, mail, number, alias)
        self.set_documents_duration(3)
        self.__rank = 0

    def setData(self, dictionary):
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

    def setData(self, dictionary):
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
