class Document:
    def __init__(self, title, author):
        self.__doc_title = title
        self.__doc_author = author
        self.__doc_owner = None
        self.__keywords = dict
        self.__keywords_count = 0

    def set_title(self, new_title):
        self.__doc_title = new_title

    def get_title(self):
        return self.__doc_title

    def set_author(self, new_author):
        self.__doc_author = new_author

    def get_author(self):
        return self.__doc_author

    def set_value(self, new_value):
        self.__doc_value = new_value

    def get_value(self):
        return self.__doc_value

    def set_owner(self, new_owner):
        self.__doc_owner = new_owner

    def get_owner(self):
        return self.__doc_owner

    def remove_owner(self):
        self.__doc_owner = None

    def add_keyword(self, word):
        self.__keywords_count += 1
        self.__keywords[word] = self.__keywords_count

    def remove_keyword(self, word):
        self.__keywords.pop(word)
        self.__keywords_count -= 1


class Book(Document):
    def __init__(self, title, author, publisher, edition, genre):
        super.__init__(title, author)
        self.__publisher = publisher
        self.__edition = edition
        self.__genre = genre
        self.__is_bestseller = False

    def set_publisher(self, new_publisher):
        self.__publisher = new_publisher

    def get_publisher(self):
        return self.__publisher

    def set_edition(self, new_edition):
        self.__edition = new_edition

    def get_edition(self):
        return self.__edition

    def set_genre(self, new_genre):
        self.__genre = new_genre

    def get_genre(self):
        return self.__genre

    def set_bestseller(self, is_it):
        self.__is_bestseller = is_it

    def get_is_bestseller(self):
        return self.__is_bestseller


class Article(Document):
    def __init__(self, title, author, journal, publication_date, editor):
        super.__init__(title, author)
        self.__journal = journal
        self.__publication_date = publication_date
        self.__editor = editor

    def set_journal(self, new_journal):
        self.__journal = new_journal

    def get_journal(self):
        return self.__journal

    def set_pub_date(self, new_date):
        self.__publication_date = new_date

    def get_pub_date(self):
        return self.__publication_date

    def set_editor(self, new_editor):
        self.__editor = new_editor

    def get_editor(self):
        return self.__editor


class AV_Materials(Document):
    def __init__(self, title, author, value):
        super.__init__(title, author)
        self.set_value(value)
