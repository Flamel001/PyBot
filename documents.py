document_title = "title"
document_author = "author"
document_owner = "owner"
document_keywords = "keywords"
document_copies = "copies"
document_price = "price"
document_duration = "duration"
document_keywords_count = "keywords_count"

book_publisher = "publisher"
book_edition = "edition"
book_genre = "genre"
book_bestseller = "bestseller"
count_of_books = "count"
book_is_reference = "reference"

article_journal = "journal"
article_pub_date = "publication"
article_editor = "editor"


class Document:

    def __init__(self, title, author):
        self.__info = dict()
        self.__info[document_title] = title
        self.__info[document_author] = author
        self.__info[document_owner] = None
        self.__info[document_keywords] = dict
        self.__info[document_keywords_count] = 0
        self.__info[document_copies] = []

    def set_title(self, new_title):
        self.__info[document_title] = new_title

    def get_title(self):
        return self.__info[document_title]

    def set_author(self, new_author):
        self.__info[document_author] = new_author

    def get_author(self):
        return self.__info[document_author]

    def set_price(self, new_value):
        self.__info[document_price] = new_value

    def get_price(self):
        return self.__info[document_price]

    def set_owner(self, new_owner):
        self.__info[document_owner] = new_owner

    def get_owner(self):
        return self.__info[document_owner]

    def remove_owner(self):
        self.__info[document_owner] = None

    def add_keyword(self, word):
        self.__info[document_keywords_count] = self.__info[document_keywords_count] + 1
        self.__info[document_keywords][word] = self.__info[document_keywords_count]

    def remove_keyword(self, word):
        self.__info[document_keywords].pop(word)
        self.__info[document_keywords_count] = self.__info[document_keywords_count] - 1

    def add_copy(self, id):
        self.__info[document_copies].append(str(id))

    def get_list_of_copies(self):
        return self.__info[document_copies]

    def get_number_of_copies(self):
        return len(self.__info[document_copies])

    def summary(self):
        return self.__info


class Book(Document):
    def __init__(self, title=None, author=None, publisher=None, edition=None, genre=None):
        if title and author and publisher and edition and genre:
            super().__init__(title, author)
            self.__info = super().summary()
            self.set_publisher(publisher)
            self.set_edition(edition)
            self.set_genre(genre)
            self.set_bestseller(False)
            self.set_is_reference(False)
        else:
            super().__init__("", "")
            self.__info = super().summary()
            self.set_publisher(publisher)
            self.set_edition(edition)
            self.set_genre(genre)
            self.set_bestseller(False)
            self.set_is_reference(False)

    def setData(self, dictionary):
        tmp = dict(dictionary)
        self.set_title(tmp[document_title])
        self.set_author(tmp[document_author])
        self.set_publisher(tmp[book_publisher])
        self.set_edition(tmp[book_edition])
        self.set_genre(tmp[book_genre])
        self.set_bestseller(tmp[book_bestseller])
        self.set_is_reference(tmp[book_is_reference])

    def set_publisher(self, new_publisher):
        self.__info[book_publisher] = new_publisher

    def get_publisher(self):
        return self.__info[book_publisher]

    def set_edition(self, new_edition):
        self.__info[book_edition] = new_edition

    def get_edition(self):
        return self.__info[book_edition]

    def set_genre(self, new_genre):
        self.__info[book_genre] = new_genre

    def get_genre(self):
        return self.__info[book_genre]

    def set_bestseller(self, is_it):
        self.__info[book_bestseller] = is_it

    def is_bestseller(self):
        return self.__info[book_bestseller]

    def get_duration(self):
        if self.is_bestseller():
            return 2
        else:
            return 3

    def set_is_reference(self, is_not):
        self.__info[book_is_reference] = is_not

    def is_reference(self):
        return self.__info[book_is_reference]

    def summary(self):
        return self.__info


class Article(Document):
    def __init__(self, title=None, author=None, journal=None, publication_date=None, editor=None):
        if title and author and journal and publication_date and editor:
            super().__init__(title, author)
            self.__info = super().summary()
            self.__info[article_journal] = journal
            self.__info[article_pub_date] = publication_date
            self.__info[article_editor] = editor
        else:
            super().__init__("", "")
            self.__info = super().summary()
            self.__info[article_journal] = journal
            self.__info[article_pub_date] = publication_date
            self.__info[article_editor] = editor

    def setData(self, dictionary):
        tmp = dict(dictionary)
        self.set_title(tmp[document_title])
        self.set_author(tmp[document_author])
        self.set_journal(tmp[article_journal])
        self.set_pub_date(tmp[article_pub_date])
        self.set_editor(tmp[article_editor])

    def set_journal(self, new_journal):
        self.__info[article_journal] = new_journal

    def get_journal(self):
        return self.__info[article_journal]

    def set_pub_date(self, new_date):
        self.__info[article_pub_date] = new_date

    def get_pub_date(self):
        return self.__info[article_pub_date]

    def set_editor(self, new_editor):
        self.__info[article_editor] = new_editor

    def get_editor(self):
        return self.__info[article_editor]

    def get_duration(self):
        return 2

    def summary(self):
        return self.__info


class AV_Materials(Document):
    def __init__(self, title=None, author=None, price=None):
        if title and author and price:
            super().__init__(title, author)
            self.__info = super().summary()
            self.set_price(price)
        else:
            super().__init__("", "")
            self.__info = super().summary()
            self.set_price(price)

    def setData(self, dictionary):
        tmp = dict(dictionary)
        self.set_title(tmp[document_title])
        self.set_author(tmp[document_author])
        self.set_price(tmp[document_price])

    def get_author(self):
        return self.__info[document_author]

    def get_duration(self):
        return 2

    def summary(self):
        return self.__info
