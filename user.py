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
user_registration_date = "registration_date"


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
        self.__info = dict()
        self.__info[user_name] = name
        self.__info[user_mail] = mail
        self.__info[user_number] = number
        self.__info[user_alias] = alias
        self.__info[user_rating] = 5
        self.__info[user_document_list] = dict()
        self.__info[user_registration_date] = datetime.datetime.now()
        self.__info[user_rank] = 0
        self.__info[user_debt] = 0

    def setData(self, dictionary):
        temp = dict(dictionary)
        self.set_name(temp[user_name])
        self.set_mail(temp[user_mail])
        self.set_number(temp[user_number])
        self.set_alias(temp[user_alias])
        self.set_rating(temp[user_rating])
        self.set_docs_list(temp[user_document_list])
        self.__info[user_registration_date] = temp[user_registration_date]
        self.set_rank(temp[user_rank])
        self.set_debt(temp[user_debt])

    def dictionary_constructor(self, dictionary):
        self.__info = dict(dictionary)

    # name = temp.pop("User name")
    # mail = temp.pop("User mail")
    # number = temp.pop("User number")
    # alias = temp.pop("User alias")
    # self.__user_name = name
    # self.__user_mail = mail
    # self.__phone_number = number
    # self.__user_alias = alias
    # self.__user_rating = temp.pop("")
    # self.__user_documents = dict()
    # self.__registration_date = datetime.datetime.now()

    def get_name(self):
        return self.__info[user_name]

    def set_name(self, new_name):
        self.__info[user_name] = new_name

    def get_mail(self):
        return self.__info[user_mail]

    def set_mail(self, new_mail):
        self.__info[user_mail] = new_mail

    def get_number(self):
        return self.__info[user_number]

    def set_number(self, new_number):
        self.__info[user_number] = new_number

    def get_alias(self):
        return self.__info[user_alias]

    def set_alias(self, new_alias):
        self.__info[user_alias] = new_alias

    def decrease_rating(self):
        self.__info[user_rating] = self.__info[user_rating] - 1

    # def set_id(self, ID):
    #     self.__user_ID = ID

    # def get_id(self):
    #     return self.__user_ID

    def add_document(self, book, count):
        string = ""
        try:
            string = str(self.__user_documents[str(book.get_title())])
        except:
            print("Poshel noj")
        if not string:
            if count > 0:
                if not book.is_reference():
                    init_date = datetime.datetime.toordinal(datetime.datetime.today())
                    print("Rank " + str(self.get_rank()))
                    if (self.get_rank() == 1):
                        exp_date = datetime.datetime.fromordinal(init_date + 28)
                    else:
                        if book.is_bestseller():
                            exp_date = datetime.datetime.fromordinal(init_date + 14)
                        else:
                            exp_date = datetime.datetime.fromordinal(init_date + 21)
                    self.__user_documents[book.get_title()] = exp_date
                    return "DONE. You will have to return this book untill:" + str(exp_date)
                else:
                    return "The book is unavailable"
            else:
                return "No copies"
        else:
            return "You are owning this book already"

    def remove_document(self, id):
        self.__info[user_document_list].pop(id)

    def get_docs_list(self):
        temp = dict(self.__info[user_document_list])
        return str(temp)

    def set_docs_list(self, new_list):
        temp = dict(new_list)
        self.__info[user_document_list] = temp


    def get_rating(self):
        return self.__info[user_rating]

    def set_rating(self, rating):
        self.__info[user_rating] = rating

    def get_registration_date(self):
        return self.__info[user_registration_date]

    def set_documents_duration(self, dur):
        self.__info[user_document_duration] = dur

    def get_documents_duration(self):
        return self.__info[user_document_duration]

    def get_rank(self):
        return self.__info[user_rank]

    def increase_debt(self, value):
        self.__info[user_debt] = self.__info[user_debt] + value

    def decrease_debt(self, value):
        self.__info[user_debt] = self.__info[user_debt] - value

    def get_debt(self):
        return self.__info[user_debt]
    def set_debt(self,debt):
        self.__info[user_debt] = debt

    def summary(self):
        return self.__info

    def set_rank(self, rank):
        self.__info[user_rank] = rank


class Student(Patron):

    def __init__(self, name, mail, number, alias):
        super().__init__(name, mail, number, alias)
        self.set_documents_duration(3)
        self.set_rank(0)

    def setData(self, dictionary):
        temp = dict(dictionary)
        name = temp.pop(user_name)
        mail = temp[user_mail]
        number = temp[user_number]
        alias = temp[user_alias]
        super().__init__(name, mail,number,alias)
        self.set_rank(0)
        self.set_documents_duration(3)



        # debt = temp.pop("User debt")
        # super().__init__(name, mail, number, alias)
        # self.set_documents_duration(3)
        # self.__rank = 0
        # self.increase_debt(debt)


class Faculty(Patron):

    def __init__(self, name, mail, number, alias):
        super().__init__(name, mail, number, alias)
        self.set_documents_duration(4)
        self.set_rank(1)

    def setData(self, dictionary):
        temp = dict(dictionary)
        name = temp(user_name)
        mail = temp(user_mail)
        number = temp(user_number)
        alias = temp(user_alias)

        super().__init__(name, mail, number, alias)
        self.set_documents_duration(4)
        self.set_rank(1)
        # self.increase_debt(debt)
