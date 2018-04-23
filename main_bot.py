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


@bot.message_handler(commands=["admin"])
def admin(call):
    u.current.user = Admin()
    bot.send_message(call.chat.id, "Choose action",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_admin_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "Manage Librarians")
def man_lib(call):
    u.current.field = db.get(type_user="Librarian")  # TODO: Проверить, работает ли с пустым списком лайбрерианов
    u.current.type = "Librarian"

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="type email of Librarian from list\n{}".format([u.current.field[i].get_mail()
                                                                               for i in range(len(u.current.field))]),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Action Log")
def log(call):
    date = get_date()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Log for: " + date,  # TODO: пофиксить отображение лога
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    id = call.message.chat.id
    get_log()
    with open('log.txt', encoding='utf-8') as doc:
        bot.send_document(chat_id=id, data=doc)


@bot.message_handler(commands=["start"])
def greeting(message):
    # book = Book("q", "Charlotte Bronte", "SomePublisher", "1337", "first", "SomeGenre","nexo",False,False,["titles","titles"], [])
    # db.insert(book.summary())
    exist = aut.check(message.chat.id)
    if not exist:
        print(message)
        message = bot.send_message(message.chat.id, "Please send your e-mail with @innopolis.ru")
        bot.register_next_step_handler(message, auth)
    else:
        if facbase.is_librarian(
                db.get(id=message.chat.id)[0]):  # TODO: Проверить, не крашится ли с пустым списком лайбрерианов
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))
        else:
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


def auth(call):  # TODO: Прогнать один раз тестово
    if call.text[-13:] == u.domain and len(call.text) > 13:
        u.current.email = call.text.lower()
        u.current.pin = veri.pin_generator()
        veri.pin_sender(u.current.email, u.current.pin)#TODO: пофиксить пин сендер
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
    temp_type = ""
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

    bot.send_message(call.chat.id, "Congratulations, registration is finished. Now choose, what do you want to do",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "My docs")
def my_docs(call):
    # u.field = "Patron docs"  # TODO: проверить работоспособность метода
    u.current.field = db.get(id=call.message.chat.id)[0].get_docs_list()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter doc from list {}".format(u.current.field),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Reserve")
def reserve(call):
    # u.field = "Patron docs"  # TODO: обратиться в дб по полю                  DEFUNCT
    print(u.current.field)
    print(type(u.current.field))
    # msg = (call.message.text).split(", ")#TODO: сделать нормально
    # u.current.field = db.get(title=msg[0])
    result_text = "{} is added to your list".format(u.current.object.get_title()) # this text is redundant
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=b.booking(db.get(id=call.message.chat.id), u.current.field, msg[1], 0),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "To waiting list")
def patron_waiting_list(call):
    # TODO:прикрутить сам вейтинг лист и какое то уведомление молодого о том, когда появится книга
    doc = u.current.object
    print(u.current.object)
    print(u.current.object.get_title())
    usr = db.get(id=call.message.chat.id)[0]#TODO: подумать, мб можно без обращения к дб и доделать, чтоб работало
    # result_text = "You are added to the waiting list for {}".format(u.current.object.get_title()) # this text is redundant
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=b.booking(usr, doc, "time doesn't matter", 1),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Return")
def return_doc(call):
    libs = db.get(type_user="Librarian")
    for i in libs:
        bot.send_message(chat_id=i.get_id(), text="User with alias {} will return book soon".format("Pidoras"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          # TODO  заменить пидорас на алиас
                          text="Please, go to the Library and return your book",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Renew")
def renew(call):
    # TODO: update time
    usr = db.get(id=call.message.chat.id)
    msg = (call.message.text).split(", ")#eto ne to
    doc = u.current.object
    # result_text = "Time for your doc updated" # this is text is redundant
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=b.booking(usr, doc, msg[1], 2),
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


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
                          text="docs of user users are {}".format(u.current.db_to_search),
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Library")
def library(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose type of doc",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_buttons_library))


@bot.callback_query_handler(func=lambda call: call.data == "Waiting list")
def initialize_librarian(call):
    # TODO: прикрутить метод waiting list   DEFUNCT
    list = ["patron1", "faculty2", "Ramil-pezduk999"]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} now in the waiting list".format(list),
                          reply_markup=bot_features.get_inline_markup(
                              [["Make request", "Outstanding Request"],
                               ["OK", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Outstanding Request")
def initialize_librarian(call):
    # TODO: прикрутить метод аутстендинг реквест
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Request is done",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"METHODS FOR SEARCH"


@bot.callback_query_handler(func=lambda call: call.data == "Actions with Patrons")
def search_patron(call):
    u.current.type = "Emails"
    u.current.field = db.get(type_user="Student") + db.get(type_user="Instructor") + db.get(
        type_user="Professor") + db.get(type_user="TA") + db.get(type_user="VP")
    print("{} - eto u.cur.field".format(u.current.field))
    if u.current.field == []:
        list_of_patrons = "Now list of patrons is empty. They can be added by Librarian by typing email"
    else:
        list_of_patrons = "Enter email from list\n"
        for i in range(len(u.current.field)):
            list_of_patrons += ("{}\n".format(u.current.field[i].get_mail()))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=list_of_patrons,
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Book" or call.data == "Article" or call.data == "AV")
def search_doc(call):
    u.current.type = call.data
    u.current.field = db.get(type_book=call.data)
    print("{} - eto u.cur.field".format(u.current.field))
    list_of_docs = ""
    if u.current.field == []:
        if facbase.is_librarian(db.get(id=call.chat.id)[0]):
            msg = "They can be added by typing title"
        else:
            msg = "Try to check later"
        list_of_docs = "Now list of {}s is empty. {}".format(call.data,msg)
    else:
        list_of_docs = "Enter name of doc from list\n"
        for i in range(len(u.current.field)):
            list_of_docs += ("{}\n".format(u.current.field[i].get_title()))
    # "Enter name of doc from list\n{}".format([u.current.field[i].get_title()
    #                                           for i in range(len(u.current.field))])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=list_of_docs,
                          reply_markup=bot_features.get_inline_markup(
                              u.keyboard_button_back))  # TODO: sdelat tak 4tob metod viglyadel ne yebanski
    bot.register_next_step_handler(call.message, search)


def search(call):  # TODO: пройтись по всем возможным if
    u.current.title_or_name = call.text
    print(call.text)
    exist = False
    print(u.current.type)
    for i in u.current.field:
        if u.current.type == "Librarian" or u.current.type == "Emails":
            if i.get_mail() == call.text:
                exist = True
                u.current.object = i
        else:
            print(i.get_title, call.text)
            if i.get_title() == call.text:
                exist = True
                u.current.object = i
    if exist:
        if type(u.current.user) == Admin:
            message = "Choose action to do with {}".format(call.text)
            markup = u.keyboard_librarian_buttons_manage
        elif facbase.is_librarian(db.get(id=call.chat.id)[0]):
            message = "Choose action to do with {}".format(call.text)
            priv = db.get(call.chat.id)[0].get_priv()
            print(priv)
            if priv == 2:  # TODO: ==1, пока так для простоты, в финальной версии заменить на единицу
                markup = u.keyboard_librarian_buttons_manage[[0]]
            elif priv == 2:
                markup = u.keyboard_librarian_buttons_manage[0:2]
            else:
                markup = u.keyboard_librarian_buttons_manage

            if u.current.type == "Book" or "Article" or "AV":
                markup = markup + [["Waiting list", "Waiting list"]] + u.keyboard_librarian_buttons_manage[-1:]

            else:
                markup += u.keyboard_librarian_buttons_manage[-1:]



        else:
            if u.current.type == "Emails":
                message = "What do you want to do with {}?".format(call.text)
                markup = u.keyboard_patron_buttons_doc
            else:
                if False:  # TODO: тут должно чекать, если количество книг>0
                    message = "Do you want to reserve {}?".format(call.text)
                    button = "Reserve"
                else:
                    message = "Do you want to be added to the waiting list to take {} when it will be availible?".format(
                        call.text)
                    button = "To waiting list"
                markup = [[button, button]]
    else:
        if type(u.current.user) == Admin:
            message = "Do you want to add {} to database?".format(call.text)
            markup = u.keyboard_librarian_buttons_confirmation

        elif facbase.is_librarian(db.get(id=call.chat.id)[0]):
            message = "Do you want to add {} to database?".format(call.text)
            markup = u.keyboard_librarian_buttons_confirmation
        else:
            if u.current.field == "Patron docs":#eto ne to, menyai
                message = "Sorry, {} is not in your list, but you can try to find it in the Library".format(call.text)
                markup = u.keyboard_patron_buttons_home
            else:
                message = "Sorry, {} is not available. Try again. Choose needed isinstance".format(call.text)
                markup = u.keyboard_buttons_library
    bot.send_message(call.chat.id, message, reply_markup=bot_features.get_inline_markup(markup))


"METHODS FOR EDIT"


@bot.callback_query_handler(func=lambda call: call.data == "Edit")
def edit(call):
    buttons = u.get_buttoms(u.current.object.get_type())
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose parameter to edit:",
                          reply_markup=bot_features.get_inline_markup(buttons), parse_mode="markdown")


@bot.callback_query_handler(func=lambda call: call.data[0] == "$")
def editing(call):
    u.current.attr = call.data[1:]

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter new parameter for {} of {}".format(call.data[1:], u.current.title_or_name),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, edited)


def edited(call):
    u.edit_attr(u.current.attr, call.text)
    bot.send_message(call.chat.id,
                     text="This field is now equals to {}".format(call.text),
                     reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"DELETE, GETINFO AND ADD"


@bot.callback_query_handler(func=lambda call: call.data == "Delete")
def delete(call):
    print(u.current.type)
    print(u.current.object)
    if u.is_human():
        u.name = u.current.object.get_id()
        db.delete(id=u.current.object.get_id())
    else:
        u.name = u.current.object.get_title()
        db.delete(title=u.current.object.get_title())
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is deleted from list of {}".format(u.name, u.current.type),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Add")
def add(call):
    list = ""
    attr = u.get_buttoms(u.current.type)
    print(attr)
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
    print(array_of_values)
    print(u.current.type)
    while len(array_of_values) < 10:
        array_of_values.append("0")
    if u.current.type == "Book":
        doc = Book(title=u.current.title_or_name, author=array_of_values[0], publisher=array_of_values[1],
                   year=array_of_values[2], edition=array_of_values[3], genre=array_of_values[4])
    elif u.current.type == "AV":
        doc = AV_Materials(title=u.current.title_or_name, author=array_of_values[0], price=array_of_values[1])
    elif u.current.type == "Article":
        doc = Article(title=u.current.title_or_name, author=array_of_values[0], journal=array_of_values[1],
                      publication_date=array_of_values[2], editor=array_of_values[3])
    elif u.current.type == "Librarians":
        doc = Librarian(id=array_of_values[0], alias=array_of_values[1], name=u.current.title_or_name,
                        mail=array_of_values[2], number=array_of_values[3], address=array_of_values[4],
                        priv=int(array_of_values[5]))
    else:

        if array_of_values[0] == "Instructor":
            doc = Instructor(int(array_of_values[1]), array_of_values[2], array_of_values[3], array_of_values[0],
                             array_of_values[4], array_of_values[5])
        elif array_of_values[0] == "TA":
            doc = TA(int(array_of_values[1]), array_of_values[2], array_of_values[3], array_of_values[0],
                     array_of_values[4], array_of_values[5])
        elif array_of_values[0] == "Professor":
            doc = Professor(int(array_of_values[1]), array_of_values[2], array_of_values[3], array_of_values[0],
                            array_of_values[4], array_of_values[5])
        elif array_of_values[0] == "VP":
            doc = VP(int(array_of_values[1]), array_of_values[2], array_of_values[3], array_of_values[0],
                     array_of_values[4], array_of_values[5])
        else:
            doc = Student(int(array_of_values[1]), array_of_values[2], array_of_values[3], u.current.title_or_name,
                          array_of_values[4], array_of_values[5])

    db.insert(doc.summary())

    print('SUCCESS')
    print(doc.summary()["type"])
    bot.send_message(call.chat.id, "Addition to database was successful",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Get information")
def get_info(call):
    obj = str(u.current.object.summary())  # TODO: Сделать более приятный интерфейс
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=obj,
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"BACK"


@bot.callback_query_handler(func=lambda call: call.data == "Back")
def back(call):
    if type(u.current.user) == Admin:
        markup = bot_features.get_inline_markup(u.keyboard_admin_buttons_home)
    elif not facbase.is_librarian(db.get(id=call.message.chat.id)[0]):
        markup = bot_features.get_inline_markup(u.keyboard_patron_buttons_home)
    else:
        markup = bot_features.get_inline_markup(u.keyboard_librarian_buttons_home)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do",
                          reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
