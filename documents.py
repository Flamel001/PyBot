from dict_keys import *
import database as db
from verification import mesage_sender as sm


class Document:

    def __init__(self, title=None, author=None, queue=None):
        self.__info = dict()
        self.__info[document_title] = title
        self.__info[document_author] = author
        self.__info[document_owner] = None
        self.__info[document_url] = ""
        self.__info[document_type] = ""
        self.__info[document_queue] = queue
        self.__info[document_copies] = list()

    def set_title(self, new_title):
        if new_title != "" or new_title != None:
            db.update(title=self.get_title(), new_title=new_title)
        self.__info[document_title] = new_title

    def get_title(self):
        return self.__info[document_title]

    def set_author(self, new_author):
        if new_author != "" or new_author != None:
            db.update(title=self.get_title(), author=new_author)
        self.__info[document_author] = new_author

    def get_author(self):
        return self.__info[document_author]

    def set_price(self, new_value):
        if new_value != "" or new_value != None:
            db.update(title=self.get_title(), price=new_value)
        self.__info[document_price] = new_value

    def get_price(self):
        return self.__info[document_price]

    def set_owner(self, new_owner):
        if new_owner != "" or new_owner != None:
            db.update(title=self.get_title(), owner=new_owner)
        self.__info[document_owner] = new_owner

    def get_owner(self):
        return self.__info[document_owner]

    def remove_owner(self):
        db.update(title=self.get_title(), owner=None)
        self.__info[document_owner] = None

    def add_copy(self, id):
        print("this is id " + id)
        self.__info[document_copies].append(str(id))
        new_copies = self.get_list_of_copies()
        db.update(title=self.get_title(), copies=new_copies)

    def get_list_of_copies(self):
        return self.__info[document_copies]

    def get_number_of_copies(self):
        return len(self.__info[document_copies])

    def set_list_of_copies(self, copies):
        if copies != "" or copies != None:
            db.update(title=self.get_title(), copies=copies)
        self.__info[document_copies] = copies

    def set_url(self, url):
        if url != "" or url != None:
            db.update(title=self.get_title(), url=url)
        self.__info[document_url] = url

    def get_url(self):
        return self.__info[document_url]

    def set_queue(self, queue):
        if queue != "" or queue != None:
            db.update(title=self.get_title(), queue=queue)
        self.__info[document_queue] = queue

    def get_queue(self):
        return self.__info[document_queue]

    def summary(self):
        return self.__info


class Book(Document):
    def __init__(self, title=None, author=None, publisher=None, year=None, edition=None, genre=None, url=None,
                 bestseller=False, reference=False, copies=None, queue=None):
        if copies:
            super().__init__(title, author, queue)
            self.__info = super().summary()
            self.set_publisher(publisher)
            self.set_year(year)
            self.set_edition(edition)
            self.set_genre(genre)
            self.set_bestseller(bestseller)
            self.set_is_reference(reference)
            self.set_url(url)
            self.set_list_of_copies(copies)
        else:
            super().__init__(title, author, queue)
            self.__info = super().summary()
            self.set_publisher(publisher)
            self.set_year(year)
            self.set_edition(edition)
            self.set_genre(genre)
            self.set_bestseller(bestseller)
            self.set_is_reference(reference)
            self.set_url(url)
        self.set_type("Book")

    def set_type(self, type):
        self.__info[document_type] = type

    def get_type(self):
        return self.__info[document_type]

    def set_publisher(self, new_publisher):
        if new_publisher != "" or new_publisher != None:
            db.update(title=self.get_title(), publisher=new_publisher)
        print("this is type of a publisher " + str(type(self.__info)))
        self.__info[book_publisher] = new_publisher

    def get_publisher(self):
        return self.__info[book_publisher]

    def set_year(self, year):
        if year != "" or year != None:
            db.update(title=self.get_title(), year=year)

        self.__info[book_year] = year

    def get_year(self):
        return self.__info[book_year]

    def set_edition(self, new_edition):
        if new_edition != "" or new_edition != None:
            db.update(title=self.get_title(), edition=new_edition)

        self.__info[book_edition] = new_edition

    def get_edition(self):
        return self.__info[book_edition]

    def set_genre(self, new_genre):
        if new_genre != "" or new_genre != None:
            db.update(title=self.get_title(), genre=new_genre)

        self.__info[book_genre] = new_genre

    def get_genre(self):
        return self.__info[book_genre]

    def set_bestseller(self, is_it):
        if is_it != "" or is_it != None:
            db.update(title=self.get_title(), bestseller=is_it)

        self.__info[book_bestseller] = is_it

    def is_bestseller(self):
        return self.__info[book_bestseller]

    def get_duration(self):
        if self.is_bestseller():
            return 2
        else:
            return 3

    def set_is_reference(self, is_not):
        if is_not != "" or is_not != None:
            db.update(title=self.get_title(), reference=is_not)
        self.__info[book_is_reference] = is_not

    def is_reference(self):
        return self.__info[book_is_reference]

    def set_outstanding(self):
        db.update(title=self.get_title(), queue=[])
        if self.get_owner() != None:
            mail = str(self.get_owner().get_mail())
            title_str = self.get_title()
            message = "You need to return book: " + title_str + " due that this is book is outstanding now"
            sm(mail, message)

    def summary(self):
        return self.__info


class Article(Document):
    def __init__(self, title=None, author=None, journal=None, publication_date=None, editor=None, url=None,
                 copies=None, queue=None):
        if copies:
            super().__init__(title, author, queue)
            self.__info = super().summary()
            self.set_journal(journal)
            self.set_pub_date(publication_date)
            self.set_editor(editor)
            self.set_url(url)
            self.set_list_of_copies(copies)
        else:
            super().__init__(title, author, queue)
            self.__info = super().summary()
            self.set_journal(journal)
            self.set_pub_date(publication_date)
            self.set_editor(editor)
            self.set_url(url)

        self.set_type("Article")

    def set_type(self, type):
        self.__info[document_type] = type

    def get_type(self):
        return self.__info[document_type]

    def set_journal(self, new_journal):
        if new_journal != "" or new_journal != None:
            db.update(title=self.get_title(), journal=new_journal)
        self.__info[article_journal] = new_journal

    def get_journal(self):
        return self.__info[article_journal]

    def set_pub_date(self, new_date):
        if new_date != "" or new_date != None:
            db.update(title=self.get_title(), publication_date=new_date)

        self.__info[article_pub_date] = new_date

    def get_pub_date(self):
        return self.__info[article_pub_date]

    def set_editor(self, new_editor):
        if new_editor != "" or new_editor != None:
            db.update(title=self.get_title(), editor=new_editor)

        self.__info[article_editor] = new_editor

    def get_editor(self):
        return self.__info[article_editor]

    def get_duration(self):
        return 2

    def summary(self):
        return self.__info


class AV_Materials(Document):
    def __init__(self, title=None, author=None, price=None, url=None, copies=None):
        if copies:
            super().__init__(title, author)
            self.__info = super().summary()
            self.set_price(price)
            self.set_url(url)
            self.set_list_of_copies(copies)
        else:
            super().__init__(title, author)
            self.__info = super().summary()
            self.set_price(price)
            self.set_url(url)

        self.set_type("AV")

    def set_type(self, type):
        self.__info[document_type] = type

    def get_type(self):
        return self.__info[document_type]

    def get_author(self):
        return self.__info[document_author]

    def get_duration(self):
        return 2

    def summary(self):
        return self.__info
