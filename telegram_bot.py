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
    type_to_add = ""


@bot.message_handler(commands=["start"])
def start(message):
    user_type = message.text.split(" ")[1]
    users[message.chat.id] = user_info()
    if user_type == "admin":
        users[message.chat.id].user = Admin()
        bot.send_message(message.chat.id, "Choose action",
                         reply_markup=bot_features.get_inline_markup(u.keyboard_admin_buttons_home))
    elif user_type == "student":
        users[message.chat.id].user = Student(id=message.chat.id, alias=message.chat.username,
                                              name=(message.chat.first_name + message.chat.last_name), mail="somemail",
                                              number="someNumber", address="SomeAddress")
        bot.send_message(message.chat.id, "Now choose what you want to do",
                         reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))
    elif user_type == "librarian":
        users[message.chat.id].user = Librarian(id=message.chat.id, alias=message.chat.username,
                                                name=(message.chat.first_name + message.chat.last_name),
                                                mail="somemail", number="someNumber", address="SomeAddress", priv=3)
        bot.send_message(message.chat.id, "Now choose what you want to do",
                         reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))
    # print(str(users[message.chat.id].user.summary()))


@bot.callback_query_handler(func=lambda call: call.data == "Manage Librarians")
def man_lib(call):
    users[call.message.chat.id].list_of_object_to_search = db.get(type_user="Librarian")
    users[call.message.chat.id].action = call.data
    emails_of_librarians = [users[call.message.chat.id].list_of_object_to_search[i].get_mail() for i in
                            range(len(users[call.message.chat.id].list_of_object_to_search))]
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

    doc = open('log.txt', mode='rb')
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
    users[call.message.chat.id].type_to_add = call.data
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
                              u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Reserve" or call.data == "To waiting list" or call.data == "Renew")
def reserve(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=booking.booking(users[call.message.chat.id].user, users[call.message.chat.id].object,
                                               call.data),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


# @bot.callback_query_handler(func=lambda call: call.data == "To waiting list")
# def patron_waiting_list(call):
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text=booking.booking(users[call.message.chat.id].user, users[call.message.chat.id].object,
#                                                "Hello", 1),
#                           reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
#
#
# @bot.callback_query_handler(func=lambda call: call.data == "Renew")
# def renew(call):
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text=booking.booking(users[call.message.chat.id].user, users[call.message.chat.id].object,
#                                                "Hello", 2),#ZDAROVA
#                           reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


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
    users[call.message.chat.id].list_of_object_to_search = db.get(type_user="Student") + db.get(
        type_user="Instructor") + db.get(
        type_user="Professor") + db.get(type_user="TA") + db.get(type_user="VP")
    users[call.message.chat.id].action = "Actions with Patrons"
    patrons = users[call.message.chat.id].list_of_object_to_search
    if not patrons:
        list_of_patrons = "Now list of patrons is empty. They can be added by typing email"
    else:
        list_of_patrons = "Enter email from list\n"
        for i in range(len(patrons)):
            list_of_patrons += ("{}\n".format(get_property(patrons[i], 1)))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=list_of_patrons,
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Get information")
def get_info(call):
    temp_dict = users[call.message.chat.id].object.summary()
    text = "\n".join([":".join([str(list(temp_dict.keys())[i]), str(list(temp_dict.values())[i])]) for i in
                      range(len(temp_dict))])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text,
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Add")
def add(call):
    list = ""
    attr = u.get_buttoms(users[call.message.chat.id].type_to_add)
    for i in range(len(attr)):
        list += "{}, ".format(attr[i][0])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                            text="Enter values for the following fields using new line and commas: {}".format(list[:-1],
                            reply_markup=bot_features.get_inline_markup(
                            u.keyboard_button_back)))
    bot.register_next_step_handler(call.message, adding)


def adding(message):
    # TODO: Вроде норм, но возможно лучше отрефакторить
    array_of_values = message.text.split("\n")
    # while len(array_of_values) < 10:
    #     array_of_values.append("0")
    if array_of_values[0] == "Book":
        users[message.chat.id].user.new_book(title=array_of_values[1], author=array_of_values[2],
                                             publisher=array_of_values[3], year=array_of_values[4],
                                             edition=array_of_values[5], genre=array_of_values[6],
                                             url=array_of_values[7],
                                             bestseller=True if array_of_values[8] == "True" else False,
                                             reference=True if array_of_values[9] == "True" else False)
    elif array_of_values[0] == "AV":
        users[message.chat.id].user.new_AV_material(title=array_of_values[1], author=array_of_values[2],
                                                    price=array_of_values[3], url=array_of_values[4])
    elif array_of_values[0] == "Article":
        users[message.chat.id].user.new_article(title=array_of_values[1], author=array_of_values[2],
                                                journal=array_of_values[3], publication_date=array_of_values[4],
                                                editor=array_of_values[5], url=array_of_values[6])
    elif array_of_values[0] == "Librarians":
        users[message.chat.id].user.add_librarian(id=int(array_of_values[1]), alias=array_of_values[2],
                                                  name=array_of_values[3],
                                                  mail=array_of_values[4], number=array_of_values[5],
                                                  address=array_of_values[6],
                                                  priv=int(array_of_values[7]))
    elif array_of_values[0] == "Instructor":
        users[message.chat.id].user.new_instructor(id=int(array_of_values[1]), alias=array_of_values[2],
                                                   name=array_of_values[3], mail=array_of_values[4],
                                                   number=array_of_values[5], address=array_of_values[6])
    elif array_of_values[0] == "TA":
        users[message.chat.id].user.new_ta(id=int(array_of_values[1]), alias=array_of_values[2],
                                           name=array_of_values[3], mail=array_of_values[4], number=array_of_values[5])
    elif array_of_values[0] == "Professor":
        users[message.chat.id].user.new_professor(id=int(array_of_values[1]), alias=array_of_values[2],
                                                  name=array_of_values[3], mail=array_of_values[4],
                                                  number=array_of_values[5], address=array_of_values[6])
    elif array_of_values[0] == "VP":
        users[message.chat.id].user.new_vp(id=int(array_of_values[1]), alias=array_of_values[1],
                                           name=array_of_values[2], mail=array_of_values[3], number=array_of_values[3])
    else:
        users[message.chat.id].user.new_student(id=int(array_of_values[1]), alias=array_of_values[2],
                                                name=array_of_values[3], mail=array_of_values[4],
                                                number=array_of_values[5], address=array_of_values[6])
    bot.send_message(message.chat.id, "Addition to database was successful",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Edit")
def edit(call):
    buttons = u.get_buttoms(users[call.message.chat.id].object.summary()["type"])
    buttons += [["Back", "Back"]]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose parameter to edit:",
                          reply_markup=bot_features.get_inline_markup(buttons), parse_mode="markdown")


@bot.callback_query_handler(func=lambda call: call.data[0] == "$")
def editing(call):
    users[call.message.chat.id].attr = call.data[1:]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter new parameter for {} of {}".format(call.data[1:], get_property(users[call.message.chat.id].object, 2)),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, edited)


def edited(message):
    getattr(users[message.chat.id].object, "set_" + str(users[message.chat.id].attr).lower())(message.text)

    date = get_date()
    id_str = str(message.chat.id)
    us_id = str(users[message.chat.id].object.get_id())
    attrib = str(users[message.chat.id].attr)
    cur_type = type(users[message.chat.id].user)
    new_attr = message.text
    if cur_type == Librarian:
        db.insert_log(
            date + " | " + cur_type + " with ID(" + id_str + ") changed user's " + attrib + " with ID: " + us_id + " to " + new_attr)
    else:
        db.insert_log(
            date + " | Admin changed Librarian's " + attrib + " with ID: " + us_id + " to " + new_attr)

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
    queue = users[call.message.chat.id].object.get_queue()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} are now in the waiting list".format(queue),
                          reply_markup=bot_features.get_inline_markup(
                              [["Make request", "Outstanding Request"],
                               ["OK", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Outstanding Request")
def initialize_librarian(call):
    users[call.message.chat.id].user.set_outstanding(get_property(users[call.message.chat.id].object, 0))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Request is done",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


def search(message):
    if users[message.chat.id].action == "Library":
        docs = find(message, 0)
        if len(docs) <= 1:
            doc = docs[0] if len(docs)>0 else None
            if type(users[message.chat.id].user) == Librarian:
                if doc:
                    message_text = "Choose action to do with :"
                    markup = distribute_by_privilege(users[message.chat.id].user.get_priv(), False)
                else:
                    if users[message.chat.id].user.get_priv() > 1:
                        message_text = "Do you want to add {} to database?".format(message.text)
                        markup = u.keyboard_librarian_buttons_confirmation + [["Return to home page", "Back"]]
                    else:
                        message = "Sorry, you don't have permissions for addition".format(message.text)
                        markup = u.keyboard_button_back
            else:
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
        else:
            bot.send_message(text="Please look through suggestions and select one. These are suggestions " + str(docs), chat_id=message.chat.id)
            bot.register_next_step_handler(message, search)
            return
    elif users[message.chat.id].action == "My docs":
        if message.text in users[message.chat.id].user.get_docs_list().keys():
            message_text = "What do you want to do with this document?"
            markup = u.keyboard_patron_buttons_doc
        else:
            message_text = "Sorry, doc with such title is not in your list, but you can try to find it in the Library."
            markup = u.keyboard_patron_buttons_home
        users[message.chat.id].object = db.get(title=message.text)
    elif users[message.chat.id].action == "Manage Librarians":
        libs = find(message, 1)
        if len(libs) <= 1:
            lib = libs[0] if len(libs)>0 else None
            if lib:
                message_text = "Choose action to do with {}".format(message.text)
                markup = u.keyboard_librarian_buttons_manage
            else:
                message_text = "Do you want to add {} to database?".format(message.text)
                markup = u.keyboard_librarian_buttons_confirmation
                users[message.chat.id].type_to_add = "Librarian"
            users[message.chat.id].object = lib
        else:
            bot.send_message(text="Please look through suggestions and select one. These are suggestions " + str(libs), chat_id=message.chat.id)
            bot.register_next_step_handler(message, search)
            return
    elif users[message.chat.id].action == "Actions with Patrons":
        patrons = find(message, 1)
        if len(patrons) <= 1:
            patron = patrons[0] if len(patrons)>0 else None
            if patron:
                message_text = "Choose action to do"
                markup = distribute_by_privilege(users[message.chat.id].user.get_priv(), True)
            else:
                message_text = "Do you want to add {} to database?".format(message.text)
                markup = u.keyboard_librarian_buttons_confirmation
                users[message.chat.id].type_to_add = "Student"
            users[message.chat.id].object = patron
        else:
            bot.send_message(text="Please look through suggestions and select one. These are suggestions " + str(patrons), chat_id=message.chat.id)
            bot.register_next_step_handler(message, search)
            return
    bot.send_message(message.chat.id, message_text, reply_markup=bot_features.get_inline_markup(markup))


def find(message, code: int):
    object_list = users[message.chat.id].list_of_object_to_search
    object_titles = db.search(message.text.split(", ")[0], [get_property(object_list[i], code) for i in range(0, len(object_list))])
    if len(object_titles) == 1:
        for object in object_list:
            if get_property(object, code) == object_titles[0]:
                return [object]
    elif len(object_titles) == 0:
        return list()
    else:
        return object_titles



def get_property(obj, code):
    if code == 0:
        return obj.get_title()
    elif code == 1:
        return obj.get_mail()
    elif code == 2:
        return obj.get_id()


def distribute_by_privilege(priv: int, user: bool):
    markup = u.keyboard_librarian_buttons_manage[0:1]
    if priv == 3:
        markup += u.keyboard_librarian_buttons_manage[2]
    if not user:
        if priv == 1:
            markup += [["Waiting list", "Waiting list"]]
        elif priv == 2:
            markup += [["Waiting list", "Waiting list"], ["Outstanding Request", "Outstanding Request"]]
        else:
            markup += [["Waiting list", "Waiting list"], ["Outstanding Request", "Outstanding Request"]]
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
