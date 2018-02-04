from telebot import *
greeting = """Welcome to Innopolis Library Management System.
              Please enter your e-mail address.
              Remember it should contain @innopolis.ru domain, otherwise you won't be able
              to authorise.
              Please press /setup to setup your profile."""

err_mail = "Invalid e-mail"

# auth literals
step0 = "Enter you email"
step1 = "Great! Now enter your Name: "
step2 = "Wonderful! Now your surname: "
step3 = "Excellent! Now the last step. Leave your number: "
step4 = "Congratulations! Your sign up has been done!"
verification_succeed = "Great!"
verification_failed = "It's not that PIN that I've sent you :( "
domain = "@innopolis.ru"
pin_enter = "Please enter PIN I've sent to you. "

"Keybord for main menu"
reply = types.ReplyKeyboardMarkup(True,False)
docs_btn = types.KeyboardButton(text="Docs")
my_books_btn = types.KeyboardButton(text="My books")
help_btn = types.KeyboardButton(text="Help")
reply.add(docs_btn, my_books_btn, help_btn)


tempData = {'userId': '0'}