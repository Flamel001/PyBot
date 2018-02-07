document_title = "title"
document_author = "author"
document_owner = "owner"
document_keywords = "keywords"
document_copies = "copies"
document_price = "price"
document_duration = "duration"

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
        self.__doc_title = title
        self.__doc_author = author
        self.__doc_owner = None
        self.__keywords = dict
        self.__keywords_count = 0
        self.__copies_id = []

    def set_title(self, new_title):
        self.__doc_title = new_title

    def get_title(self):
        return self.__doc_title

    def set_author(self, new_author):
        self.__doc_author = new_author

    def get_author(self):
        return self.__doc_author

    def set_price(self, new_value):
        self.__doc_price = new_value

    def get_price(self):
        return self.__doc_price

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

    def add_copy(self, id):
        self.__copies_id.append(str(id))

    def get_copies_id(self):
        return self.__copies_id

    def get_count_of_copies(self):
        return len(self.__copies_id)


class Book(Document):
    def __init__(self, title, author, publisher, edition, genre):
        # super.__init__(title, author)
        self.__doc_title = title
        self.__doc_author = author
        self.__publisher = publisher
        self.__edition = edition
        self.__genre = genre
        self.__is_bestseller = False
        self.__is_reference = False
        self.__number_of_books = 3

    def setData(self, dictionary):
        d = dict(dictionary)
        title = d[document_title]
        author = d[document_author]
        publisher = d[book_publisher]
        edition = d[book_edition]
        genre = d[book_genre]
        super.__init__(title, author)
        self.__publisher = publisher
        self.__edition = edition
        self.__genre = genre
        self.__is_bestseller = False
        self.__is_reference = False

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

    def is_bestseller(self):
        return self.__is_bestseller

    def get_duration(self):
        if self.get_is_bestseller():
            return 2
        else:
            return 3

    def set_is_reference(self, is_not):
        self.__is_reference = is_not

    def is_reference(self):
        return self.__is_reference

    def summary(self):
        d = dict()
        d[document_title] = self.__doc_title
        d[document_author] = self.__doc_author
        d[book_publisher] = self.__publisher
        d[book_edition] = self.__edition
        d[book_genre] = self.__genre
        d[book_bestseller] = self.__is_bestseller
        d[document_duration] = self.get_duration()
        # d["Book owner"] = self.get_owner()
        # d["Book copies"] = self.get_copies_id()
        d[book_is_reference] = self.__is_reference
        d[count_of_books] = self.__number_of_books
        # d["Book value"] = self.get_price()
        return d


class Article(Document):
    def __init__(self, title, author, journal, publication_date, editor):
        self.__doc_title = title
        self.__doc_author = author
        self.__journal = journal
        self.__publication_date = publication_date
        self.__editor = editor

    def setData(self, dictionary):
        d = dict(dictionary)
        title = d["Article title"]
        author = d["Article author"]
        journal = d["Article journal"]
        publication_date = d["Article publication date"]
        editor = d["Aricle editor"]
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

    def get_duration(self):
        return 2

    def summary(self):
        d = dict()
        d["Article title"] = self.get_title()
        d["Article author"] = self.get_author()
        d["Article journal"] = self.get_journal()
        d["Article publication date"] = self.get_pub_date()
        d["Aricle editor"] = self.get_editor()
        d["Article duration"] = self.get_duration()
        d["Article owner"] = self.get_owner()
        d["Article copies ID"] = self.get_copies_id()
        d["Article value"] = self.get_price()
        return d


class AV_Materials(Document):
    def __init__(self, title, author, price):
        super.__init__(title, author)
        self.set_price(price)

    def setData(self, dictionary):
        d = dict(dictionary)
        title = d["AV title"]
        author = d["AV author"]
        value = d["AV value"]
        super.__init__(title, author)
        self.set_price(value)

    def get_duration(self):
        return 2

    def summary(self):
        d = dict()
        d["AV title"] = self.get_title()
        d["AV author"] = self.get_author()
        d["AV value"] = self.get_price()
        d["AV duration"] = self.get_duration()
        d["AV owner"] = self.get_owner()
        d["AV copies"] = self.get_copies_id()
        return d
