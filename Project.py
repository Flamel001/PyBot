import database as db
from user import Librarian
from user import Student
from documents import Book
from user import Faculty
import booking
import json
import bot
import utilities

# lib = Librarian("testName", "testMail", "9898938485", "testAlias")
#
# db.insert_librarian("349870347940874ID", lib.summary())
#
# student = Student("testNameStudent", "testMailStudent", "29387947", "testAliasStudent")
# #
#
# #student.add_document("Thinking in Java")
#
# #db.insert_patron("27478298348874729ID", student.summary())
# #
# book = Book("Introduction to Algorithm", "author", "someCompany", "edition", "genre")
# #
# # db.insert_book("Introduction to Algorithm", book.summary())
#
# faculty = Faculty("userNameFaculty", "userMailFaculty", "userNumberFaculty", "userAliasFaculty")

#faculty.add_document("Introduction to Algorithm#1")

#db.insert_patron("9038594898558545ID", faculty.summary())

#print(str(db.get_book("j")))

# print(str(booking.book_doc(student, book)))
#
# print(str(booking.book_doc(student, book)))
#
# print(str(student.has_book(book.get_title())))
#
# print(str(student.get_docs_list()))
#
# book.add_copy("1")
#
# print(str(book.get_list_of_copies()))
#
# dictionary = dict()
# dictionary["hello"] = "world"
# dictionary["marco"] = "polo"
#
# print(str(dictionary))
#
# dictionary1 = dict()
# dictionary1["hello"] = "world!!!"
# dictionary1["yo"] = "wasup"
#
# dictionary.update(dictionary1)
#
#
# print(str(dictionary))

# db.insert_patron(123456789, student.summary())
#
# print(str(student.summary()))
#
# student_gotten = Student()
# student_gotten.setData(dict(db.get_patron(123456789)))
#
# print(str(student_gotten.summary()))

# print(str(book.summary()))
# print(str(type(student.summary())))
#
# # json_string = json.dumps(dict(book.summary()))
# #
# # print(str(json_string))
#
# db.insert_book("Introduction to Algorithm", book.summary())
#
# print(str(book.summary()))
#
# book_gotten = Book()
# book_gotten.setData(db.get_book("Introduction to Algorithm"))
#
# print(str(book_gotten.summary()))

# b = utilities.list_of_books[0]
# b1 = utilities.list_of_books[1]
# # d = dict()
# # d["copies"] = b.get_list_of_copies()
# # db.update_book(b.get_title(), d)
# print(str(b.summary()))
# print(str(b1.summary()))
# db.insert_user(utilities.user2.get_alias(), utilities.user2.summary())

# b = Book("someBook2", "someAuthor", "somePublisher", "someEdition", "someGenre")
# b.add_copy("1")
# print(str(b.summary()))
#
# db.insert_book(b.get_title(),  b.summary())


# list_of_books = db.get_all_books()
# list_of_books[0].add_copy("1")
# list_of_books[0].add_copy("2")
# list_of_books[0].add_copy("3")
# list_of_books[0].add_copy("4")
# list_of_books[0].add_copy("5")
# d = dict()
# d["copies"] = list(list_of_books[0].get_list_of_copies())
# db.update_book(list_of_books[0].get_title(), d)

# librarian = Librarian("12345678", "lib", "libatinnopoilis", "777897890", "lib")
# def return_user(number):
#     if number == 1:
#         return student
#     elif number == 2:
#         return faculty
#     elif number == 3:
#         return librarian
#
#
# print(str(return_user(1).summary()))
# print(str(return_user(2).summary()))
# print(str(return_user(3).summary()))

# str = "/remove       someone and something"
# str = str.strip().split()
# print(str)
#
# d = dict()
# d["copy"] = "something"
# d1 = dict()
# d1["hello"] = d
# dictionary = json.loads(d["copy"])
# print(str(type(dictionary)))

d = dict()
d["something_1"] = "hello"
d1 = dict()
d1["j"] = d
d2 = d1["j"]
for key in d2.keys():
    if "something" == key.split("_")[0]:
        print("True")
    else:
        print("False")
