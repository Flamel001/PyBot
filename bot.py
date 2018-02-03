import types

import config
from telebot import *
import telegraph
import datetime as date
import DataBase as db

bot = TeleBot(config.token2)
ph = telegraph.Telegraph()


@bot.message_handler(commands=["start"])
def greeting(message):
    bot.send_message(message.chat.id,"Welcome to Innopolis Library Management System."
                                     "\nPlease enter your e-mail address."
                                     "\nRemember it should contain @innopolis.ru domain, otherwise you won't be able"
                                     "to authorise."
                                     "\nPlease press /setup to setup your profile.")


@bot.message_handler(command=["setup"])
def call_f(message):
    authentication(email=message)

@bot.message_handler(func=lambda command)
def authentication(email):
    domain = "@blablabla.ru"
    if email.text[11:] != domain:
        bot.send_message(email.chat.id, "Invalid e-mail")
    else:
        db.insertUser(email.chat.id, email)




@bot.message_handler(commands=["options"])
def keyboard(message):
    reply = types.ReplyKeyboardMarkup(True,False)

    button1 = types.KeyboardButton(text="Docs")
    button2 = types.KeyboardButton(text="My books")
    button3 = types.KeyboardButton(text="Help")
    reply.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Please choose options bellow", reply_markup=reply)



"""
    Usage of Telegraph api. Integration of telegraph api for "about" features.
    
"""
ph.create_account(short_name='InnoLib')
response = ph.create_page('Bruce Eckels Thinking in Java',
                          html_content="<p> Thinking in Java should be read cover to cover by every Java programmer, "
                                       "then kept close at hand for frequent reference. The exercises are challenging,"
                                       " and the chapter on Collections is superb!"
                                       " Not only did this book help me to pass the Sun Certified Java Programmer exam;"
                                       " it’s also the first book I turn to whenever I have a Java question. </p>")


@bot.message_handler(regexp="Docs")
def telegraph_func(message):
    markup = types.InlineKeyboardMarkup()
    callback_btn = types.InlineKeyboardButton(text="Reserve",callback_data="Book")
    left_btn = types.InlineKeyboardButton(text="3 left", callback_data="Left")
    markup.add(callback_btn)
    markup.add(left_btn)
    bot.send_message(message.chat.id, 'http://telegra.ph/Bruce-Eckels-Thinking-in-Java-4th-editon-01-29',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'Book')
def left(call):
    init_date = date.datetime.toordinal(date.datetime.today())
    exp_date = date.datetime.fromordinal(init_date + 14)
    bot.send_message(call.message.chat.id, "You have been ordered a book on: " + "\n" + str(date.date.today()) +
                                           "\nYour book will expire on: " + "\n" + str(exp_date))



@bot.message_handler(regexp='help')
def help_func(message):
    bot.reply_to(message, "Help func is currently unavailable")


if __name__ == '__main__':
    bot.polling(none_stop=True)