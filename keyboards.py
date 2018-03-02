from telebot import *

"Keybord for main menu"
reply = types.ReplyKeyboardMarkup(True, False)
docs_btn = types.KeyboardButton(text="Docs")
my_books_btn = types.KeyboardButton(text="My books")
help_btn = types.KeyboardButton(text="Help")
reply.add(docs_btn, my_books_btn, help_btn)
"counter for books"

# list_of_books = [b.book1, b.book2, b.book3]

# number = 0
# max = len(list_of_books)
# exp = '{}/{}'.format(number + 1, max)

markup = types.InlineKeyboardMarkup()
callback_btn = types.InlineKeyboardButton(text="Reserve", callback_data="Book")
left_btn = types.InlineKeyboardButton(text="3 left", callback_data="Left")
next_btn = types.InlineKeyboardButton(text="➡", callback_data='next')
counter = types.InlineKeyboardButton(text="retake/36", callback_data='counter')
prev_btn = types.InlineKeyboardButton(text='⬅', callback_data='prev')
markup.add(callback_btn)
markup.add(left_btn)
markup.add(prev_btn, counter, next_btn)