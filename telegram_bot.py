import telebot
import config
from user import *
from documents import *
import utilities as u
import bot_features
import database as db
import booking
import datetime

bot = telebot.TeleBot(config.token)
users = dict()


class user_info():
    list_of_object_to_search = list()
    user = None
    action = ""
    object = None
    attr = ""

@bot.message_handler(commands=["start"])
def start(message):
    user_type = message.text.split(" ")[1]
    users[message.chat.id] = user_info()
    if user_type == "admin":
        users[message.chat.id].user = Admin()
        bot.send_message(message.chat.id, "Choose action",
                         reply_markup=bot_features.get_inline_markup(u.keyboard_admin_buttons_home))
    elif user_type == "student":
        users[message.chat.id].user = Student(id=message.chat.id, alias=message.chat.username, name=(message.chat.first_name + message.chat.last_name), mail="somemail", number="someNumber", address="SomeAddress")
        bot.send_message(message.chat.id, "Now choose what you want to do",
                         reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))
    elif user_type == "librarian":
        users[message.chat.id].user = Librarian(id=message.chat.id, alias=message.chat.username, name=(message.chat.first_name + message.chat.last_name), mail="somemail", number="someNumber", address="SomeAddress")
        bot.send_message(message.chat.id, "Now choose what you want to do",
                         reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))
    print(str(users[message.chat.id].user.summary()))


@bot.callback_query_handler(func=lambda call: call.data == "Manage Librarians")
def man_lib(call):
    users[call.message.chat.id].list_of_object_to_search = db.get(type_user=Librarian)
    users[call.message.chat.id].action = call.data
    emails_of_librarians = [users[call.message.chat.id].list_of_object_to_search[i].get_mail() for i in range(0, len(users[call.message.chat.id].list_of_object_to_search))]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="type email of Librarian from list\n{}".format(emails_of_librarians),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Action Log")
def log(call):
    date = get_date()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Log for: " + date,  # TODO: выводить лог файлом
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    get_log()
    with open('log.txt', encoding='utf-8') as doc:
        bot.send_document(chat_id=call.message.chat.id, data=doc)


@bot.callback_query_handler(func=lambda call: call.data == "Library")
def library(call):
    users[call.message.chat.id].action = call.data
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose type of doc",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_buttons_library))


@bot.callback_query_handler(func=lambda call: call.data == "Book" or call.data == "Article" or call.data == "AV")
def search_doc(call):
    users[call.message.chat.id].list_of_object_to_search = db.get(type_book=call.data)
    docs_list = users[call.message.chat.id].list_of_object_to_search
    if not docs_list:
        list_of_docs = "Now list of {}s is empty. They can be added by Librarian by typing title".format(call.data)
    else:
        list_of_docs = "Enter name of doc from list\n"
        for i in range(len(docs_list)):
            list_of_docs += ("{}\n".format(docs_list[i].get_title()))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=list_of_docs,
                          reply_markup=bot_features.get_inline_markup(
                              u.keyboard_button_back))  # TODO: sdelat tak 4tob metod viglyadel ne yebanski
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Reserve")
def reserve(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=booking.booking(users[call.message.chat.id].user, users[call.message.chat.id].object, "Hello", 0),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "To waiting list")
def patron_waiting_list(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=booking.booking(users[call.message.chat.id].user, users[call.message.chat.id].object, "Hello", 1),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Renew")
def renew(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=booking.booking(users[call.message.chat.id].user, users[call.message.chat.id].object, "Hello", 2),
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Return")
def return_doc(call):
    libs = db.get(type_user="Librarian")
    for i in libs:
        bot.send_message(chat_id=i.get_id(),
                         text="User with alias {} will return book soon".format(call.from_user.username))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Please, go to the Library and return your book",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "My docs")
def my_docs(call):
    users[call.message.chat.id].action = call.data
    user_docs = users[call.message.chat.id].user.get_docs_list()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter doc from list {}".format(user_docs),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Tech support")
def tech_sup(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Here are aliases of tech support:\n @N_Flamel",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Actions with Patrons")
def search_patron(call):
    users[call.message.chat.id].list_of_object_to_search = db.get(type_user="Student") + db.get(type_user="Instructor") + db.get(
        type_user="Professor") + db.get(type_user="TA") + db.get(type_user="VP")
    users[call.message.chat.id].action = "Actions with Patrons"
    patrons_and_libs = users[call.message.chat.id].list_of_object_to_search
    if not patrons_and_libs:
        list_of_patrons = "Now list of patrons is empty. They can be added by Librarian by typing email"
    else:
        list_of_patrons = "Enter email from list\n"
        for i in range(len(patrons_and_libs)):
            list_of_patrons += ("{}\n".format(get_property(patrons_and_libs[i], 1)))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=list_of_patrons,
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Get information")
def get_info(call):
    temp_dict = users[call.message.chat.id].object.summary()
    text = "\n".join([":".join([[temp_dict.keys()][i], [temp_dict.values()][i]]) for i in range(0, len(temp_dict))])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text,
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Add")
def add(call):
    list = ""
    attr = u.get_buttoms(users[call.message.chat.id].object.summary()["type"])
    for i in range(1, len(attr)):
        list += "{}, ".format(attr[i][0])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          # TODO:возможно сделать более приятный интерфейс
                          text="Enter values for the following fields using new line and commas: {}".format(list[:-1]),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, adding)


def adding(call):
    # TODO: Вроде норм, но возможно лучше отрефакторить
    array_of_values = call.text.split("\n")
    # while len(array_of_values) < 10:
    #     array_of_values.append("0")
    if array_of_values[0] == "Book":
        users[call.message.chat.id].user.new_book(title=array_of_values[1], author=array_of_values[2], publisher=array_of_values[3], year=array_of_values[4], edition=array_of_values[5], genre=array_of_values[6], url=array_of_values[7], bestseller=True if array_of_values[8]=="True" else False, reference=True if array_of_values[9]=="True" else False)
    elif array_of_values[0] == "AV":
        users[call.message.chat.id].user.new_AV_material(title=array_of_values[1], author=array_of_values[2], price=array_of_values[3], url=array_of_values[4])
    elif array_of_values[0] == "Article":
        users[call.message.chat.id].user.new_article(title=array_of_values[1], author=array_of_values[2], journal=array_of_values[3], publication_date=array_of_values[4], editor=array_of_values[5], url=array_of_values[6])
    elif array_of_values[0] == "Librarians":
        users[call.message.chat.id].user.add_librarian(id=int(array_of_values[1]), alias=array_of_values[2], name=array_of_values[3],
                        mail=array_of_values[4], number=array_of_values[5], address=array_of_values[6],
                        priv=int(array_of_values[7]))
    elif array_of_values[0] == "Instructor":
        users[call.message.chat.id].user.new_instructor(id=int(array_of_values[1]), alias=array_of_values[2], name=array_of_values[3], mail=array_of_values[4], number=array_of_values[5], address=array_of_values[6])
    elif array_of_values[0] == "TA":
        users[call.message.chat.id].user.new_ta(id=int(array_of_values[1]), alias=array_of_values[2], name=array_of_values[3], mail=array_of_values[4], number=array_of_values[5])
    elif array_of_values[0] == "Professor":
        users[call.message.chat.id].user.new_professor(id=int(array_of_values[1]), alias=array_of_values[2], name=array_of_values[3], mail=array_of_values[4], number=array_of_values[5], address=array_of_values[6])
    elif array_of_values[0] == "VP":
        users[call.message.chat.id].user.new_vp(id=int(array_of_values[1]), alias=array_of_values[1], name=array_of_values[2], mail=array_of_values[3], number=array_of_values[3])
    else:
        users[call.message.chat.id].user.new_student(id=int(array_of_values[1]), alias=array_of_values[2], name=array_of_values[3], mail=array_of_values[4], number=array_of_values[5], address=array_of_values[6])
    bot.send_message(call.chat.id, "Addition to database was successful",
                 reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Edit")
def edit(call):
    buttons = u.get_buttoms(users[call.message.chat.id].object.summary()["type"])
    buttons += [["Back","Back"]]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose parameter to edit:",
                          reply_markup=bot_features.get_inline_markup(buttons), parse_mode="markdown")


@bot.callback_query_handler(func=lambda call: call.data[0] == "$")
def editing(call):
    users[call.message.chat.id].attr = call.data[1:]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter new parameter for {} of {}".format(call.data[1:], u.current.title_or_name),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, edited)


def edited(message):
    getattr(users[message.chat.id].object, "set_" + str(users[message.chat.id].attr).lower())(message.text)
    bot.send_message(message.chat.id,
                     text="This field is now equals to {}".format(message.text),
                     reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Delete")
def delete(call):
    if users[call.message.chat.id].object.summary()["type"] in ["Book", "Article", "AV"]:
        id_of_user = get_property(users[call.message.chat.id].object, 2)
        db.delete(id=id_of_user)
    else:
        title_of_doc = get_property(users[call.message.chat.id].object, 0)
        db.delete(id=title_of_doc)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is deleted".format(u.current.name),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Waiting list")
def initialize_librarian(call):
    # TODO: прикрутить метод waiting list   DEFUNCT
    queue = users[call.message.chat.id].object.get_queue()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} are now in the waiting list".format(queue),
                          reply_markup=bot_features.get_inline_markup(
                              [["Make request", "Outstanding Request"],
                               ["OK", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Outstanding Request")
def initialize_librarian(call):
    # TODO: проверить работоспособность
    db.get(id=call.message.chat.id)[0].set_outstanding(u.current.object.get_title())

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Request is done",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


def search(message):
    if users[message.chat.id].action == "Library":
        doc = find(message, 0)
        if type(users[message.chat.id].user) == Librarian:
            if doc:
                message_text = "Choose action to do:"
                markup = distribute_by_privilege(users[message.chat.id].user.get_priv(), False)
            else:
                if users[message.chat.id].user.get_priv() > 1:
                    message_text = "Do you want to add {} to database?".format(message.text)
                    markup = u.keyboard_librarian_buttons_confirmation + [["Return to home page", "Back"]]
                else:
                    message = "Sorry, you don't have permissions for addition".format(message.text)
                    markup = u.keyboard_button_back
        else:
            print("This is doc " + str(doc))
            print(str(doc.summary()))
            if doc:
                if doc.get_number_of_copies() > 0:
                    message_text = "Do you want to reserve {}?".format(message.text)
                    button = "Reserve"
                else:
                    message_text = "Do you want to be added to the waiting list to take {} when it will be availible?".format(
                            message.text)
                    button = "To waiting list"
                markup = [[button, button]]
            else:
                message_text = "Sorry, {} is not available. Try again. Choose needed isinstance".format(message.text)
                markup = u.keyboard_buttons_library
        users[message.chat.id].object = doc
    elif users[message.chat.id].action == "My docs":
        if message.text in users[message.chat.id].user.get_docs_list().keys():
            message_text = "What do you want to do with this document?"
            markup = u.keyboard_patron_buttons_doc
        else:
            message_text = "Sorry, doc with such title is not in your list, but you can try to find it in the Library."
            markup = u.keyboard_patron_buttons_home
        users[message.chat.id].object = db.get(title=message.text)
    elif users[message.chat.id].action == "Manage Librarians":
        lib = find(message, 1)
        if lib:
            message_text = "Choose action to do with {}".format(message.text)
            markup = u.keyboard_librarian_buttons_manage
        else:
            message_text = "Do you want to add {} to database?".format(message.text)
            markup = u.keyboard_librarian_buttons_confirmation
        users[message.chat.id].object = lib
    elif users[message.chat.id].action == "Actions with Patrons":
        patron_or_lib = find(message, 1)
        if patron_or_lib:
            message_text = "Choose action to do"
            markup = distribute_by_privilege(users[message.chat.id].user.get_priv(), True)
        else:
            message_text = "Do you want to add {} to database?".format(message.text)
            markup = u.keyboard_librarian_buttons_confirmation
        users[message.chat.id].object = patron_or_lib
    bot.send_message(message.chat.id, message_text, reply_markup=bot_features.get_inline_markup(markup))


def find(message, code:int):
    object_list = users[message.chat.id].list_of_object_to_search
    for i in range(0, len(object_list)):
        # print("This is object list element's title " + str(object_list[i].get_title()))
        if message.text.split(", ")[0] == get_property(object_list[i], code):
            return object_list[i]
    return None


def get_property(obj, code):
    if code == 0:
        return obj.get_title()
    elif code == 1:
        return obj.get_mail()
    elif code == 2:
        return obj.get_id()


def distribute_by_privilege(priv:int, user:bool):
    markup = list()
    if priv == 1 or priv == 2:
        markup += u.keyboard_librarian_buttons_manage[0:1]
        if not user:
            markup += [["Waiting list", "Waiting list"]]
    else:
        markup += u.keyboard_librarian_buttons_manage
        if not user:
            markup += [["Waiting list", "Waiting list"],["Outstanding Request", "Outstanding Request"]]
    markup += [["Return to home page", "Back"]]
    return markup


@bot.callback_query_handler(func=lambda call: call.data == "Back")
def back(call):
    if type(users[call.message.chat.id].user) == Admin:
        markup = bot_features.get_inline_markup(u.keyboard_admin_buttons_home)
    elif type(users[call.message.chat.id].user) == Librarian:
        markup = bot_features.get_inline_markup(u.keyboard_librarian_buttons_home)
    else:
        markup = bot_features.get_inline_markup(u.keyboard_patron_buttons_home)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do",
                          reply_markup=markup)


if __name__ == "__main__":
    bot.polling(none_stop=True)