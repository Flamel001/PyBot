import types

import config
from telebot import *
import telegraph
import datetime as date
import database as db
import utilities as u
import verification as veri
import booking as b
import bot_features
from documents import *
from user import *


bot = TeleBot(config.token2)
ph = telegraph.Telegraph()


"""
    Usage of Telegraph api. Integration of telegraph api for "about" features. SCRATCH FOR FUTURE FEATURES
"""
ph.create_account(short_name='InnoLib')
response = ph.create_page('Bruce Eckels Thinking in Java',
                          html_content="<p> Thinking in Java should be read cover to cover by every Java programmer, "
                                       "then kept close at hand for frequent reference. The exercises are challenging,"
                                       " and the chapter on Collections is superb!"
                                       " Not only did this book help me to pass the Sun Certified Java Programmer exam;"
                                       " it’s also the first book I turn to whenever I have a Java question. </p>")


map_of_users = dict()
next_doc_message_id = 0


@bot.message_handler(commands=["start"])
def greeting(message):
    print(str(message.from_user.username))
    print(str(message.text.strip().split(" ")))
    bot.send_message(message.chat.id, u.greeting, reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_home))
    librarian = Librarian("librarian", "librarian", "librarian", "librarian", "librarian")
    map_of_users[message.from_user.username] = librarian


userEmail = ""
userName = ""
userSurname = ""
userNumber = ""


@bot.message_handler(commands=["setup"])
def authentication(email):
    msg = bot.send_message(email.chat.id, u.step0)
    bot.register_next_step_handler(msg, auth)


def auth(msg):
    if msg.text[-13:] != u.domain:
        bot.send_message(msg.chat.id, u.verification_err_mail)

    else:
        pin = veri.pin_generator()
        veri.pin_sender(msg.text, pin)
        u.tempData['userId'] = pin
        userEmail = msg.text
        print(userEmail)
        m = bot.send_message(msg.chat.id, u.pin_enter)
        bot.register_next_step_handler(m, auth_1)


def auth_1(pin):
    if verification(pin):
        m = bot.send_message(pin.chat.id, u.step1)
        print(userEmail)
        bot.register_next_step_handler(m, auth_2)


def auth_2(msg):
    userName = msg.text
    reply = bot.send_message(msg.chat.id, u.step2)
    bot.register_next_step_handler(reply, auth3)


def auth3(message):
    userSurname = message.text
    print(userSurname)
    reply = bot.send_message(message.chat.id, u.step3)
    bot.register_next_step_handler(reply, auth4)


def auth4(message):
    userNumber = message.text
    print(userNumber)
    db.insert_patron(message.chat.id, db.dict_for_user(userEmail, userName, userSurname, userNumber))
    bot.send_message(message.chat.id, u.step4)


def verification(pin):
    if pin.text == u.tempData['userId']:
        bot.send_message(pin.chat.id, u.verification_succeed)
        return True
    else:
        m = bot.send_message(pin.chat.id, u.verification_failed)
        bot.register_next_step_handler(m, verification)
        return False


@bot.message_handler(commands=["get_user"])
def get_user(message):
    if message.from_user.username in map_of_users:
        user = map_of_users[message.from_user.username]
        if user.summary()["type"] == "librarian":
            bot.send_message(message.chat.id, "This user's summary " + str(user.get_user(message.text.strip().split(" ")[-1][1:]).summary()))
        else:
            bot.send_message(message.chat.id, "You do not have the access")


@bot.message_handler(commands=["get_book"])
def get_user(message):
    if message.from_user.username in map_of_users:
        user = map_of_users[message.from_user.username]
        if user.summary()["type"] == "librarian":
            bot.send_message(message.chat.id, "Summary of this book: " + str(user.get_book(message.text.strip().split(" ")[-1])))
        else:
            bot.send_message(message.chat.id, "You do not have the access")


@bot.message_handler(commands=["remove_user"])
def remove_user(message):
    if message.from_user.username in map_of_users:
        user = map_of_users[message.from_user.username]
        if user.summary()["type"] == "librarian":
            user.remove_user(message.text.strip().split(" ")[-1][1:])
            bot.send_message(message.chat.id, "You have deleted user with alias " + str(message.text.strip.split(" ")[-1]))
        else:
            bot.send_message(message.chat.id, "You do not have the right to remove another user")


@bot.message_handler(commands=["remove_book"])
def remove_book(message):
    if message.from_user.username in map_of_users:
        user = map_of_users[message.from_user.username]
        if user.summary()["type"] == "librarian":
            user.remove_document(message.text.strip().split(" ")[-1])
            bot.send_message(message.chat.id, "You have deleted book with name " + str(message.text.strip().split(" ")[-1]))
        else:
            bot.send_message(message.chat.id, "You do not have the right to remove a book")


@bot.message_handler(commands=["add_book"])
def add_book(message):
    if message.from_user.username in map_of_users:
        user = map_of_users[message.from_user.username]
        if user.summary()["type"] == "librarian":
            message = bot.send_message(message.chat.id,
                                       "In the next message please provide:\ntitle\nauthor\npublisher\nedition\ngenre\nurl")
            bot.register_next_step_handler(message, create_book)
        else:
            bot.send_message(message.chat.id, "You do not have the right to add a new book")


def create_book(message):
    message_split = message.text.split("\n")
    if len(message_split) == 6:
        if message.from_user.username in map_of_users:
            user = map_of_users[message.from_user.username]
            if user.summary()["type"] == "librarian":
                user.new_book(message_split[0].strip(), message_split[1].strip(), message_split[2].strip(), message_split[3].strip(), message_split[4].strip(), message_split[5])
                bot.send_message(message.chat.id, "You have successfully added a book")
            else:
                bot.send_message(message.chat.id, "You do not have the right to add a new book")
    else:
        bot.send_message(message.chat.id, "The format of the message does not suit. Please try again.")


@bot.message_handler(regexp='help')
def help_func(message):
    bot.reply_to(message, "Help func is currently unavailable")


@bot.message_handler(regexp='Docs')
def genres(message):
    print("Something goes wrong")
    bot.send_message(message.chat.id, "Choose category", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_docs))


@bot.message_handler(commands=["options"])
def keyboard(message):
    bot.send_message(message.chat.id, "Please choose options bellow", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_home))


@bot.message_handler(regexp='Back')
def back(message):
    bot.send_message(message.chat.id, "Please choose options bellow", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_home))


# 'http://telegra.ph/Bruce-Eckels-Thinking-in-Java-4th-editon-01-29'
@bot.message_handler(regexp="Books")
def telegraph_func(message):
    global next_doc_message_id
    book = db.get_all_books()[bot_features.get_current_book_number()]
    message = bot.send_message(message.chat.id, book.get_title(), reply_markup=bot_features.get_inline_markup(book.get_number_of_copies()))
    next_doc_message_id = message.message_id


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def to_right(call):
    bot_features.increment_book_number()
    book = db.get_all_books()[bot_features.get_current_book_number()]
    bot.edit_message_text(chat_id=call.message.chat.id, text=book.get_title(), message_id=next_doc_message_id)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=next_doc_message_id, reply_markup=bot_features.get_inline_markup(book.get_number_of_copies()))


@bot.callback_query_handler(func=lambda call: call.data == 'prev')
def to_left(call):
    bot_features.decrement_book_number()
    book = db.get_all_books()[bot_features.get_current_book_number()]
    bot.edit_message_text(chat_id=call.message.chat.id, text=book.get_title(), message_id=next_doc_message_id)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=next_doc_message_id, reply_markup=bot_features.get_inline_markup(book.get_number_of_copies()))


@bot.callback_query_handler(func=lambda call: call.data == 'Book')
def booking(call):
    bot.send_message(call.message.chat.id, b.book_doc(u.user1, db.get_all_books()[bot_features.get_current_book_number()]))


@bot.message_handler(regexp='author')
def author(message):
    bot.send_message(message.chat.id, "Enter author's name")
    @bot.message_handler(content_types=["text"])
    def get_author(message):
        book_exist = False
        for i in range(len(u.list_of_books)):
            if u.list_of_books[i].get_author() == message.text:
                book_exist = True
                bot.send_message(message.chat.id, "Book {} of author {} exist".format(u.list_of_books[i].get_title(),
                                                                                      u.list_of_books[i].get_author()))
        if not book_exist:
            bot.send_message(message.chat.id, "There is no book with this author")


def send(userid, message):
    bot.send_message(314603914, message)



@bot.message_handler(regexp='Librarian')
def librarian(message):
    librarian = Librarian(444,"Vasyan","vasya@innopolis.ru", 123123, "@greatoption", "Pypkina street")
    bot.send_message(message.chat.id, "Please choose options bellow", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib))

    @bot.message_handler(regexp='To beginning')
    def back(message):
        bot.send_message(message.chat.id, "Please choose options bellow",
                         reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib))

    @bot.message_handler(regexp='Adding')
    def adding(message):
        bot.send_message(message.chat.id, "What do you want to add?", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib_add))


    @bot.message_handler(regexp='Add dock')
    def adding_dock(message):
        bot.send_message(message.chat.id, "Choose dock to add", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib_dock))
        bot.register_next_step_handler(message, add_dock)


    def add_dock(message):
        bot.send_message(message.chat.id, "Enter information of the {} using space".format(message.text))
        if message.text=="Book":
            bot.send_message(message.chat.id, "Publisher, edition, genre, is it bestceller, is it reference, it's url, number of copies")
            bot.register_next_step_handler(message, add_book)
        elif message.text=="Video":
            bot.send_message(message.chat.id, "Information, price, url, number of copies")
            bot.register_next_step_handler(message, add_video)
        elif message.text=="Article":
            pass

    def add_book(message):
        info = message.text.split(" ")
        print(info)
        librarian.new_book(info[0], info[1], info[2], info[3], info[4], info[5], int(info[6]))
        bot.send_message(message.chat.id, "Please choose options bellow",
                         reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib))


    def add_video(message):
        info = message.text.split(" ")
        print(info)
        librarian.new_AV_material(info[0], info[1], info[2], int(info[3]))


    "TODO: add article"

    @bot.message_handler(regexp='Add patron')
    def adding_patron(message):
        bot.send_message(message.chat.id, "Enter information of Patron".format(message))
        bot.register_next_step_handler(message, add_patron)

    def add_patron(message):
        pass


    @bot.message_handler(regexp='Removing')
    def removing(message):
        bot.send_message(message.chat.id, "What do you want to remove?", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib_remove))


    @bot.message_handler(regexp='Remove dock')
    def removing_dock(message):
        bot.send_message(message.chat.id, "Type title of dock to remove")#, reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib_dock)
        bot.register_next_step_handler(message, remove_dock)

    def remove_dock(message):
        librarian.remove_document(message.text)
        bot.send_message(message.chat.id, "Please choose options bellow",
                         reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib))
        # if message.text == "Book":
        #     bot.register_next_step_handler(message, remove_book)
        # elif message.text == "Video":
        #     bot.register_next_step_handler(message, remove_video)
        # elif message.text == "Article":
        #     pass
        #
    # def remove_book(message):
    #     librarian.
    #
    #
    # def remove_video(message):
    #


    @bot.message_handler(regexp='Remove patron')
    def removing_patron(message):
        bot.send_message(message.chat.id, "Enter alias of Patron".format(message))
        bot.register_next_step_handler(message, remove_patron)


    def remove_patron(message):
        librarian.remove_user(message.text)
        bot.send_message(message.chat.id, "Please choose options bellow",
                         reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib))


    @bot.message_handler(regexp='Checking')
    def checking(message):
        bot.send_message(message.chat.id, "What do you want to check?", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib_check))


    @bot.message_handler(regexp='Check dock')
    def checking_dock(message):
        bot.send_message(message.chat.id, "Choose dock to check", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib_dock))
        bot.register_next_step_handler(message, check_dock)

    def check_dock(message):
        pass


    @bot.message_handler(regexp='Check patron')
    def checking_patron(message):
        bot.send_message(message.chat.id, "Enter alias of Patron".format(message))
        bot.register_next_step_handler(message, remove_patron)


    def check_patron(message):
        a = librarian.get_user(message.text)
        if a!=None:
            bot.send_message(message.chat.id, a, reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib))
        else:
            bot.send_message(message.chat.id, "No user with this alias", reply_markup=bot_features.get_reply_markup(u.keyboard_buttons_lib))


if __name__ == '__main__':
    bot.polling(none_stop=True)
