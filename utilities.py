from telebot import *
import database as db
from user import *
from documents import *

greeting = """Welcome to Innopolis Library Management System.
              Please enter your e-mail address.
              Remember it should contain @innopolis.ru domain, otherwise you won't be able
              to authorise.
              Please press /setup to setup your profile."""

verification_err_mail = "Invalid e-mail"

booking_success = "DONE. You will have to return this book until:"
booking_book_is_unavailable = "The book is unavailable"
booking_no_copies = "No copies."
booking_already_have_it = "You are owning this book already"

keyboard_buttons_home = ["Library", "My docs", "Help"]
keyboard_buttons_docs = ["Books", "Magazines", "Audio/Video", "Back"]
keyboard_buttons_choice = ["Librarian", "Student", "Faculty"]



# title, author, publisher, edition, genre

book4 = Book("Jane Eyre", "Charlotte Bronte", "SomePublisher", "1", "SomeGenre")
book2 = Book("Thinking in Java", "Bruce Eckel", "Innopolis", "4th", "Computer Science")
book3 = Book("Think python", "Allen B. Downey", "O'REILEY", "2nd", "Computer Science")
book1 = Book("One Hundred Years of Solitude", "Gabriel García Márquez", "Innopolis", "1", "Magical Realism")
# book1.add_copy("1")
# book1.add_copy("2")
# book1.add_copy("3")
# book1.add_copy("4")
# book1.add_copy("5")
book1.set_bestseller(True)
user1 = Student("314603915", "Dalbaeb", "jsifj@iinno.ru", "+231312394", "@eblaneeshe")
user2 = Faculty("314603916", "BigBrother", "9afiwe@ifrefre", "+013123", "@hahhahaha")
# book1 = Book()
# book1.setData(db.get_book("One Hundred Years of Solitude"))

list_of_books = [book1, book2, book3, book4]

# auth literals
step0 = "Enter you email"
step1 = "Now enter your Name: "
step2 = "Wonderful! Now your surname: "
step3 = "Excellent! Now the last step. Leave your number: "
step4 = "Congratulations! Your sign up has been done!"
verification_succeed = "Great!"
verification_failed = "It's not that PIN that I've sent you :( "
domain = "@innopolis.ru"
pin_enter = "Please enter PIN I've sent to you. "

tempData = {'userId': '0'}
