import types
import config
import database as db
from telebot import *
import datetime as date
import utilities as u
import verification as veri
import booking as b
import bot_features
from documents import *
from user import *
import authentification as aut
import faculties_base as facbase

bot = TeleBot(config.token)
map_of_users = dict()
next_doc_message_id = 0
userEmail = ""
userName = ""
userSurname = ""
userNumber = ""

user = dict()

class user_info():
    list_of_objects = list()
    object = None
    me = None
    action = ""
    title_or_name = ""
    type = ""
    attr = ""


@bot.message_handler(commands=["start"])
def greeting(message):
    user[message.chat.id] = user_info()
    exist = aut.check(message.from_user.username)
    print(db.get(alias=message.from_user.username))
    if not exist:
        print(message)
        message = bot.send_message(message.chat.id, "Please send your e-mail with @innopolis.ru")
        bot.register_next_step_handler(message, auth)
    else:
        user[message.chat.id].me = db.get(alias=message.from_user.username)[0]
        print(type(user[message.chat.id].me))
        if type(user[message.chat.id].me) == Librarian:
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))
        else:
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))

@bot.message_handler(commands=["admin"])
def admin(call):
    user[call.chat.id] = user_info()
    user[call.chat.id].me = Admin()
    bot.send_message(call.chat.id, "Choose action",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_admin_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "Manage Librarians")
def man_lib(call):

    user[call.message.chat.id].list_of_objects = db.get(type_user="Librarian")  # TODO: Проверить, работает ли с пустым списком лайбрерианов
    user[call.message.chat.id].type = "Librarian"
    list_of_libs = [user[call.message.chat.id].list_of_objects[i].get_mail() for i in
                    range(len(user[call.message.chat.id].list_of_objects))]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="type email of Librarian from list\n{}".format(list_of_libs),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Action Log")
def log(call):
    date = get_date()
    get_log()
    doc = open('log.txt', mode='rb')
    bot.send_document(chat_id=call.message.chat.id, data=doc)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Log for: " + date,
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))



def auth(call):
    if call.text[-13:] == u.domain and len(call.text) > 13:
        u.current.email = call.text.lower()
        u.current.pin = veri.pin_generator()
        veri.pin_sender(u.current.email, u.current.pin)
        bot.send_message(call.chat.id, "Enter code that we send to your email")
        bot.register_next_step_handler(call, pin_checker)
    else:
        bot.send_message(call.chat.id, "Your email does not belong to @innopolis.ru. Please try again")
        bot.register_next_step_handler(call, auth)


def pin_checker(call):
    if call.text == u.current.pin:
        u.current.auth_val_arr.clear()
        bot.send_message(call.chat.id, "Enter your name")
        bot.register_next_step_handler(call, name)
    else:
        bot.send_message(call.chat.id, "Incorrect pin. Please, try again")
        bot.register_next_step_handler(call, pin_checker)


def name(call):
    print(call.text)
    u.current.auth_val_arr.append(call.text)
    bot.send_message(call.chat.id, "Enter your number")
    bot.register_next_step_handler(call, number)


def number(call):
    print(call.text)
    u.current.auth_val_arr.append(call.text)
    bot.send_message(call.chat.id, "Enter your address")
    bot.register_next_step_handler(call, address)


def address(call):
    print(call.text)
    u.current.auth_val_arr.append(call.text)
    temp = dict()
    for i in range(3):
        temp[u.current.auth_arr[i]] = u.current.auth_val_arr[i]
    temp["id"] = str(call.chat.id)
    temp["alias"] = call.from_user.username
    temp["mail"] = u.current.email

    id = temp["id"]
    name = temp["name"]
    mail = temp["mail"]
    number = temp["number"]
    alias = temp["alias"]
    address = temp["address"]
    if facbase.is_instructor(mail):
        usr = Instructor(id, alias, name, mail, number, address)
        temp_type = "Instructor"
    elif facbase.is_ta(mail):
        usr = TA(id, alias, name, mail, number, address)
        temp_type = "TA"
    elif facbase.is_professor(mail):
        usr = Professor(id, alias, name, mail, number, address)
        temp_type = "Professor"
    elif facbase.is_vp(mail):
        usr = VP(id, alias, name, mail, number, address)
        temp_type = "VP"
    else:
        usr = Student(id, alias, name, mail, number, address)
        temp_type = "Student"
    date = get_date()
    db.insert(usr.summary())
    db.insert_log(date + " | " + temp_type + "with ID: " + str(id) + " added")
    print(temp)
    user[id].me = usr
    bot.send_message(call.chat.id, "Congratulations, registration is finished. Now choose, what do you want to do",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "My docs")
def my_docs(call):
    # u.field = "Patron docs"  # TODO: проверить работоспособность метода
    user[call.message.chat.id].list_of_objects = db.get(id=call.message.chat.id)[0].get_docs_list()
    print(type(user[call.message.chat.id].list_of_objects)==dict)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter doc from list {}".format(user[call.message.chat.id].list_of_objects),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Reserve" or call.data == "To waiting list" or call.data == "Renew")
def reserve(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=b.booking(user[call.message.chat.id].me, user[call.message.chat.id].object,
                                               call.data),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


# @bot.callback_query_handler(func=lambda call: call.data == "To waiting list")
# def patron_waiting_list(call):
#     # TODO:прикрутить сам вейтинг лист и какое то уведомление молодого о том, когда появится книга
#     doc = user[call.chat.id].object
#     print(user[call.chat.id].object)
#     print(user[call.chat.id].object.get_title())
#     usr = db.get(id=call.message.chat.id)[0]  # TODO: подумать, мб можно без обращения к дб и доделать, чтоб работало
#     # result_text = "You are added to the waiting list for {}".format(user[call.chat.id].object.get_title()) # this text is redundant
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text=b.booking(usr, doc, "time doesn't matter", 1),
#                           reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Return")
def return_doc(call):
    libs = db.get(type_user="Librarian")
    for i in libs:
        bot.send_message(chat_id=i.get_id(),
                         text="User with alias {} will return book soon".format(call.from_user.username))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Please, go to the Library and return your book",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


# @bot.callback_query_handler(func=lambda call: call.data == "Renew")
# def renew(call):
#     # TODO: update time
#     usr = db.get(id=call.message.chat.id)
#     msg = (call.message.text).split(", ")  # eto ne to
#     doc = user[call.chat.id].object
#     # result_text = "Time for your doc updated" # this is text is redundant
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text=b.booking(usr, doc, msg[1], 2),
#                           reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Tech support")
def tech_sup(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Here are aliases of tech support:\n @N_Flamel",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


"LIBRARIAN"


@bot.callback_query_handler(func=lambda call: call.data == "Docs on hands")
def docs_on_hands(call):
    u.field = "Patron docs"  # TODO: обратиться по типу                 DEFUNCT (slojna)
    # u.db_to_search = get_db(id=call.message.chat.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="docs of user users are {}".format(),
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Library")
def library(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose type of doc",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_buttons_library))


@bot.callback_query_handler(func=lambda call: call.data == "Waiting list")
def initialize_librarian(call):
    # TODO: прикрутить метод waiting list   DEFUNCT
    queue = user[call.message.chat.id].object.get_queue()
    if not queue:
        message = "There are no patrons in waiting list"
        markup = [["OK", "Back"]]
    else:
        message = "{} now in the waiting list".format(queue)
        markup = [["Make outstanding request", "Outstanding Request"],["OK", "Back"]]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=message,
                          reply_markup=bot_features.get_inline_markup(markup))


@bot.callback_query_handler(func=lambda call: call.data == "Outstanding Request")
def initialize_librarian(call):
    # TODO: проверить работоспособность
    user[call.message.chat.id].me.set_outstanding(user[call.message.chat.id].object.get_title())
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Request is done",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"METHODS FOR SEARCH"


@bot.callback_query_handler(func=lambda call: call.data == "Actions with Patrons")
def search_patron(call):
    user[call.message.chat.id].type = "Emails"
    user[call.message.chat.id].list_of_objects = db.get(type_user="Student") + db.get(type_user="Instructor") + db.get(
        type_user="Professor") + db.get(type_user="TA") + db.get(type_user="VP")
    if user[call.message.chat.id].list_of_objects == []:
        list_of_patrons = "Now list of patrons is empty. They can be added by typing email"
    else:
        list_of_patrons = "Enter email from list:\n"
        for i in range(len(user[call.message.chat.id].list_of_objects)):
            list_of_patrons += ("{}\n".format(user[call.message.chat.id].list_of_objects[i].get_mail()))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=list_of_patrons,
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Book" or call.data == "Article" or call.data == "AV")
def search_doc(call):
    user[call.message.chat.id].type = call.data
    user[call.message.chat.id].list_of_objects = db.get(type_book=call.data)

    if not user[call.message.chat.id].list_of_objects:
        if user[call.message.chat.id].me.get_type() == "Librarian":
            msg = "They can be added by typing title"
        else:
            msg = "Try to check later"
        list_of_docs = "Now list of {}s is empty. {}".format(call.data, msg)
    else:
        list_of_docs = "Enter title of doc from list\nTitle              -                                     Author\n"
        for i in range(len(user[call.message.chat.id].list_of_objects)):
            list_of_docs += ("{}-{}\n".format(user[call.message.chat.id].list_of_objects[i].get_title(),
                                              user[call.message.chat.id].list_of_objects[i].get_author()))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=list_of_docs,
                          reply_markup=bot_features.get_inline_markup(
                              u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


def search(call):  # TODO: пройтись по if связанным с букингом
    user[call.chat.id].title_or_name = call.text

    exist = False
    for i in user[call.chat.id].list_of_objects:
        if user[call.chat.id].type == "Librarian" or user[call.chat.id].type == "Emails":
            if i.get_mail() == call.text:
                exist = True
                user[call.chat.id].object = i
        elif type(user[call.chat.id].list_of_objects)==dict:
            if i == call.text:
                exist = True
                i = db.get(title=i)
                print(i)
                user[call.chat.id].object = i
        else:
            print(i.get_title(), call.text)
            if i.get_title() == call.text:
                exist = True
                user[call.chat.id].object = i
    if exist:
        if type(user[call.chat.id].me) == Admin:
            message = "Choose action to do with {}".format(call.text)
            markup = u.keyboard_librarian_buttons_manage
        elif type(user[call.chat.id].me) == Librarian:
            message = "Choose action to do with {}".format(call.text)
            priv = user[call.chat.id].me.get_priv()
            markup = u.keyboard_librarian_buttons_manage[0:1].copy()
            if priv == 1:
                if user[call.chat.id].type == "Book" or user[call.chat.id].type == "Article" or user[call.chat.id].type == "AV":
                    markup += [["Waiting list", "Waiting list"]]
            elif priv == 2:
                if user[call.chat.id].type == "Book" or user[call.chat.id].type == "Article" or user[call.chat.id].type == "AV":
                    markup += [["Waiting list", "Waiting list"]]
                    if len(user[call.chat.id].object.get_list_of_copies()) < 1:
                        markup += [["Outstanding Request", "Outstanding Request"]]
            else:
                markup = u.keyboard_librarian_buttons_manage.copy()
                if (user[call.chat.id].type == "Book" or user[call.chat.id].type == "Article" or user[call.chat.id].type == "AV"):
                    markup += [["Waiting list", "Waiting list"]]
                    if len(user[call.chat.id].object.get_list_of_copies()) < 1:
                        markup += [["Outstanding Request", "Outstanding Request"]]
            markup += [["Return to home page", "Back"]]

        else:
            if user[call.chat.id].type == "Emails":
                message = "What do you want to do with {}?".format(call.text)
                markup = u.keyboard_patron_buttons_doc
            else:
                if len(user[call.chat.id].object.get_list_of_copies()) > 0:  # TODO: проверить работоспособность
                    message = "Do you want to reserve {}?".format(call.text)
                    button = "Reserve"
                else:
                    message = "Do you want to be added to the waiting list to take {} when it will be availible?".format(
                        call.text)
                    button = "To waiting list"
                markup = [[button, button]]
    else:
        if type(user[call.chat.id].me) == Admin or (type(user[call.chat.id].me) == Librarian and
                                                    user[call.chat.id].me.get_priv() > 1):
            message = "Do you want to add {} to database?".format(call.text)
            markup = u.keyboard_librarian_buttons_confirmation# + [["Return to home page", "Back"]]

        elif type(user[call.chat.id].me) == Librarian:
            message = "Sorry, you don't have permissions for addition".format(call.text)
            markup = u.keyboard_button_back
        else:#TODO: fix 2 if's below
            if user[call.chat.id].list_of_objects == "Patron docs":  # eto ne to, menyai
                message = "Sorry, {} is not in your list, but you can try to find it in the Library".format(call.text)
                markup = u.keyboard_patron_buttons_home
            else:
                message = "Sorry, {} is not available. Try again. Choose needed type".format(call.text)
                markup = u.keyboard_buttons_library
    bot.send_message(call.chat.id, message, reply_markup=bot_features.get_inline_markup(markup))


"METHODS FOR EDIT"


@bot.callback_query_handler(func=lambda call: call.data == "Edit")
def edit(call):
    print(user[call.message.chat.id].type)
    buttons = u.get_buttoms(user[call.message.chat.id].type)
    buttons += [["Back","Back"]]
    print(buttons)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose parameter to edit:",
                          reply_markup=bot_features.get_inline_markup(buttons), parse_mode="markdown")


@bot.callback_query_handler(func=lambda call: call.data[0] == "$")
def editing(call):
    user[call.message.chat.id].attr = call.data[1:]

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter new parameter for {} of {}".format(call.data[1:], user[call.message.chat.id].title_or_name),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, edited)


def edited(call):
    edit_attr(user[call.chat.id].attr, call.text, call.chat.id)
    bot.send_message(call.chat.id,
                     text="This field is now equals to {}".format(call.text),
                     reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"DELETE, GETINFO AND ADD"


@bot.callback_query_handler(func=lambda call: call.data == "Delete")
def delete(call):
    print(user[call.message.chat.id].type)
    print(user[call.message.chat.id].object)
    print(user[call.message.chat.id].object.summary())
    if is_human(call.message.chat.id):
        u.current.name = user[call.message.chat.id].object.get_id()
        db.delete(id=user[call.message.chat.id].object.get_id())
    else:
        u.current.name = user[call.message.chat.id].object.get_title()
        db.delete(title=user[call.message.chat.id].object.get_title())
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is deleted from list of {}".format(u.current.name, user[call.message.chat.id].type),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Add")
def add(call):
    list = ""
    if is_human(call.message.chat.id):
        attr = u.get_buttoms(user[call.message.chat.id].type)[0:-1]
    else:
        attr = u.get_buttoms(user[call.message.chat.id].type)
    print(attr)
    for i in range(len(attr)):
        list += "{}, ".format(attr[i][0])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          # TODO:возможно сделать более приятный интерфейс
                          text="Enter values for the following fields using new line and commas: {}".format(list[:-1]),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, adding)


def adding(call):
    # TODO: Вроде норм, но возможно лучше отрефакторить
    array_of_values = call.text.split("\n")
    print(array_of_values)
    print(user[call.chat.id].type)
    while len(array_of_values) < 10:
        array_of_values.append("0")
    if user[call.chat.id].type == "Book":
        user[call.chat.id].me.new_book(title=user[call.chat.id].title_or_name, author=array_of_values[0], publisher=array_of_values[1],
                   year=array_of_values[2], edition=array_of_values[3], genre=array_of_values[4])
    elif user[call.chat.id].type == "AV":
        user[call.chat.id].me.new_AV_material(title=user[call.chat.id].title_or_name, author=array_of_values[0], price=array_of_values[1])
    elif user[call.chat.id].type == "Article":
        user[call.chat.id].me.new_article(title=user[call.chat.id].title_or_name, author=array_of_values[0], journal=array_of_values[1],
                      publication_date=array_of_values[2], editor=array_of_values[3], url="")
    elif user[call.chat.id].type == "Librarian":
        user[call.chat.id].me.add_librarian(id=array_of_values[0], alias=array_of_values[1], name=array_of_values[2],
                        mail=user[call.chat.id].title_or_name, number=array_of_values[3], address=array_of_values[4],
                        priv=int(array_of_values[5]))
    else:

        if array_of_values[0] == "Instructor":
            user[call.chat.id].me.new_instructor(int(array_of_values[1]), array_of_values[2], array_of_values[3], user[call.chat.id].title_or_name,
                             array_of_values[4], array_of_values[5])
        elif array_of_values[0] == "TA":
            user[call.chat.id].me.new_ta(int(array_of_values[1]), array_of_values[2], array_of_values[3], user[call.chat.id].title_or_name,
                     array_of_values[4], array_of_values[5])
        elif array_of_values[0] == "Professor":
            user[call.chat.id].me.new_professor(int(array_of_values[1]), array_of_values[2], array_of_values[3], user[call.chat.id].title_or_name,
                            array_of_values[4], array_of_values[5])
        elif array_of_values[0] == "VP":
            user[call.chat.id].me.new_vp(int(array_of_values[1]), array_of_values[2], array_of_values[3], user[call.chat.id].title_or_name,
                     array_of_values[4], array_of_values[5])
        else:
            user[call.chat.id].me.new_student(int(array_of_values[1]), array_of_values[2], array_of_values[3], user[call.chat.id].title_or_name,
                          array_of_values[4], array_of_values[5])


    print('SUCCESS')
    bot.send_message(call.chat.id, "Addition to database was successful",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Get information")
def get_info(call):
    temp = user[call.message.chat.id].object.summary()
    obj = ""
    for i in temp:
        if i != "queue":
            obj += str(i) + " : " + str(temp.get(i)) + "\n"
    obj.strip()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=obj,
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"BACK"


@bot.callback_query_handler(func=lambda call: call.data == "Back")
def back(call):
    print(type(user[call.message.chat.id].me))
    if type(user[call.message.chat.id].me) == Admin:
        markup = bot_features.get_inline_markup(u.keyboard_admin_buttons_home)
    elif not type(user[call.message.chat.id].me) == Librarian:
        markup = bot_features.get_inline_markup(u.keyboard_patron_buttons_home)
    else:
        markup = bot_features.get_inline_markup(u.keyboard_librarian_buttons_home)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do",
                          reply_markup=markup)


def edit_attr(attr, new_attr, id):
    "BOOK"
    if attr == "Title":
        user[id].me.set_title(new_attr)
    elif attr == "Author":
        user[id].me.set_author(new_attr)
    elif attr == "Publisher":
        user[id].me.set_publisher(new_attr)
    elif attr == "Year":
        user[id].me.set_year(new_attr)
    elif attr == "Edition":
        user[id].me.set_edition(new_attr)
    elif attr == "Genre":
        user[id].me.set_genre(new_attr)
    elif attr == "Bestseller":
        user[id].me.set_bestseller(new_attr)
    elif attr == "Reference":
        user[id].me.set_reference(new_attr)
    elif attr == "Price":
        print(new_attr)
        user[id].me.set_price(new_attr)

        "ARTICLE"

    elif attr == "Journal":
        user[id].me.set_journal(new_attr)
    elif attr == "Pub_Date":
        user[id].me.set_pub_date(new_attr)
    elif attr == "Editor":
        user[id].me.set_editor(new_attr)
    elif attr == "Url":
        user[id].me.set_url(new_attr)

        "PATRON"

    elif attr == "id":
        user[id].me.set_id(new_attr)
    elif attr == "Alias":
        user[id].me.set_alias(new_attr)
    elif attr == "Name":
        user[id].me.set_name(new_attr)
    elif attr == "Mail":
        user[id].me.set_mail(new_attr)
    elif attr == "Phone_number":
        user[id].me.set_number(new_attr)
    elif attr == "Address":
        user[id].me.set_address(new_attr)

        "LIBRARIAN"
    elif attr == "Privilege":
        user[id].me.set_priv(new_attr)

def is_human(id):
    if user[id].type == "Emails" or user[id].type == "Librarian":
        return True
    else:
        return False

if __name__ == '__main__':
    bot.polling(none_stop=True)
