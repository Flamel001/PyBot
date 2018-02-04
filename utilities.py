from telebot import *
greeting = """Welcome to Innopolis Library Management System.
              Please enter your e-mail address.
              Remember it should contain @innopolis.ru domain, otherwise you won't be able
              to authorise.
              Please press /setup to setup your profile."""
err_mail = "Invalid e-mail"
# step1 =
# step2 =
# step3 =
# step4 =
# step5 =
domain = "@innopolis.ru"


"Keybord for main menu"
reply = types.ReplyKeyboardMarkup(True,False)
docs_btn = types.KeyboardButton(text="Docs")
my_books_btn = types.KeyboardButton(text="My books")
help_btn = types.KeyboardButton(text="Help")
reply.add(docs_btn, my_books_btn, help_btn)