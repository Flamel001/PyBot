import types

import config
from telebot import *
import telegraph
import datetime as date
import DataBase as db
import utilities as u
import Patron as p

bot = TeleBot(config.token2)
ph = telegraph.Telegraph()


@bot.message_handler(commands=["start"])
def greeting(message):
    bot.send_message(message.chat.id, u.greeting)


@bot.message_handler(commands=["setup"])
def authentication(email):
    msg = bot.send_message(email.chat.id, "Enter you email")
    bot.register_next_step_handler(msg, auth)


def auth(msg):
    if msg.text[-13:] != u.domain:
        bot.send_message(msg.chat.id, u.err_mail)
    else:
        split = msg.text.split('@')[0]
        # db.insertUser(msg.chat.id, db.dictForUser(split, "Pidor", "Zashekansky", "+98812312314"))
        db.user_mail(split)
        reply = bot.send_message(msg.chat.id, "Great! Now enter your Name: ")
        bot.register_next_step_handler(reply, auth2)

def auth2(message):
    db.user_name(message)
    reply = bot.send_message(message.chat.id, "Wonderful! Now your surname: ")
    bot.register_next_step_handler(reply, auth3)


def auth3(message):
    db.user_surname(message)
    reply = bot.send_message(message.chat.id, "Excellent! Now the last step. Leave your number: ")
    bot.register_next_step_handler(reply, auth4)


def auth4(message):
    db.insertUser(message.chat.id, db.dictForUser(p.Patron.get_mail()))
    bot.send_message(message.chat.id, "Congratulations! Your sign up has been done!")

@bot.message_handler(commands=["options"])
def keyboard(message):
    bot.send_message(message.chat.id, "Please choose options bellow", reply_markup=u.reply)


@bot.message_handler(regexp='Back')
def back(message):
    bot.send_message(message.chat.id, "Please choose options bellow", reply_markup=u.reply)


@bot.message_handler(regexp='Docs')
def genres(message):
    reply = types.ReplyKeyboardMarkup(True, False, True, 1)
    math_btn = types.KeyboardButton(text="Math")
    java_btn = types.KeyboardButton(text="Java",)
    prog_btn = types.KeyboardButton(text="Programming")
    reply.add(math_btn, java_btn, prog_btn)
    bot.send_message(message.chat.id, "Choose category", reply_markup=reply)








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


@bot.message_handler(regexp='Hooj')
def printAllUsersInBot(message):
    db.printAllUsers()


if __name__ == '__main__':
    bot.polling(none_stop=True)