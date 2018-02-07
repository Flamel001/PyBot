from telebot import *
import database as db
import booking as b
greeting = """Welcome to Innopolis Library Management System.
              Please enter your e-mail address.
              Remember it should contain @innopolis.ru domain, otherwise you won't be able
              to authorise.
              Please press /setup to setup your profile."""

err_mail = "Invalid e-mail"

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

"Keybord for main menu"
reply = types.ReplyKeyboardMarkup(True, False)
docs_btn = types.KeyboardButton(text="Docs")
my_books_btn = types.KeyboardButton(text="My books")
help_btn = types.KeyboardButton(text="Help")
reply.add(docs_btn, my_books_btn, help_btn)
"counter for books"

list_of_books = [b.book1,b.book2,b.book3]

number = 0
max = len(list_of_books)
exp = '{}/{}'.format(number+1, max)

markup = types.InlineKeyboardMarkup()
callback_btn = types.InlineKeyboardButton(text="Reserve", callback_data="Book")
left_btn = types.InlineKeyboardButton(text="3 left", callback_data="Left")
next_btn = types.InlineKeyboardButton(text="➡", callback_data='next')
counter = types.InlineKeyboardButton(text=exp, callback_data='counter')
prev_btn = types.InlineKeyboardButton(text='⬅', callback_data='prev')
markup.add(callback_btn)
markup.add(left_btn)
markup.add(prev_btn, counter, next_btn)

tempData = {'userId': '0'}