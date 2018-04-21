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

bot = TeleBot(config.token2)
map_of_users = dict()
next_doc_message_id = 0
userEmail = ""
userName = ""
userSurname = ""
userNumber = ""


@bot.message_handler(commands=["admin"])
def admin(call):
    u.current.user = "admin"
    #ne pishy na full potomu 4to nado bydet link s bd tyt srazy i 4ek na libra
    bot.send_message(call.chat.id, "Choose action",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_admin_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "Manage Librarians")
def man_lib(call):
    u.current.field = "Librarians"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Type name(or smthg else, we wil choose what) of Librarian from list\n{}".format(get_db(u.current.field)),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call, search)


@bot.callback_query_handler(func=lambda call: call.data == "Action Log")
def log(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Tyt bydet log",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))



# @bot.callback_query_handler(func=lambda call: call.data == "Privilegies")#mb nahoi, prosto 4erez edit bydem nazna4at
# def privileges(call):
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text="Choose level of previlegies for this Librarian",
#                           reply_markup=bot_features.get_inline_markup(u.keyboard_admin_buttons_privileges))
#
#
# @bot.callback_query_handler(func=lambda call: call.data == "1" or call.data == "2" or call.data == "3")
# def set_privileges(call):
#     #set privileges = call.data
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text="Zbc krasava, teper choose action",
#                           reply_markup=bot_features.get_inline_markup(u.keyboard_admin_buttons_home))


@bot.message_handler(commands=["start"])
def greeting(message):
    exist = aut.check(message.chat.id)
    if not exist:
        print(message)
        message = bot.send_message(message.chat.id, "Please send your e-mail with @innopolis.ru")
        bot.register_next_step_handler(message, auth)
    else:
        if facbase.is_librarian(message.chat.id):
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))
        else:
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


def auth(call):
    if call.text[-13:] == u.domain and len(call.text) > 13:
        u.current_email = call.text
        u.pin = veri.pin_generator()
        veri.pin_sender(call.text, u.current.pin)
        bot.send_message(call.chat.id, "Enter code that we send to your email")
        bot.register_next_step_handler(call, pin_checker)
    else:
        bot.send_message(call.chat.id, "Please try again")
        bot.register_next_step_handler(call, auth)

def pin_checker(call):
    if call.text == u.current.pin:
        u.current.auth_val_arr.clear()
        bot.send_message(call.chat.id, "Enter your name")
        bot.register_next_step_handler(call, name)
    else:
        bot.send_message(call.chat.id, "Please try again")
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
    temp["mail"] = u.current.current_email

    id = temp["id"]
    name = temp["name"]
    mail = temp["mail"]
    number = temp["number"]
    alias = temp["alias"]
    address = temp["address"]

    if facbase.is_instructor(mail):#TODO: /можно ООП-шнее? аля usr=patron(x,y,z)
        usr = Instructor(id, alias, name, mail, number, address)
    elif facbase.is_ta(mail):
        usr = TA(id, alias, name, mail, number, address)
    elif facbase.is_professor(mail):
        usr = Professor(id, alias, name, mail, number, address)
    elif facbase.is_vp(mail):
        usr = VP(id, alias, name, mail, number, address)
    else:
        usr = Student(id, alias, name, mail, number, address)

    db.insert(usr.summary())
    print(temp)

    bot.send_message(call.chat.id, "Congratulations, registration is finished. Now choose, what do you want to do",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "My docs")
def my_docs(call):
    u.field = "Patron docs"  # TODO: обратиться в дб по полю
    u.db_to_search = get_db(u.current.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter doc from list {}".format(u.current.db_to_search),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    # bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                               reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Reserve")
def reserve(call):
    u.field = "Patron docs"  # TODO: обратиться в дб по полю
    u.db_to_search = get_db(u.current.field)
    u.current.db_to_search.append(u.current.current_object.text)
    print(u.current.db_to_search)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is added to {}".format(u.current.current_object.text, u.current.field),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "To waiting list")
def patron_waiting_list(call):
    # TODO:прикрутить сам вейтинг лист и какое то уведомление молодого о том, когда появится книга
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="You are added to the waiting list for {}".format(u.current.current_object.text),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Return")
def return_doc(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Please, go to the Library and return your book",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Renew")
def renew(call):
    # TODO: update time
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Time for your doc updated",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Tech support")
def tech_sup(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Here are aliases of tech support:\n @N_Flamel",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


"LIBRARIAN"


@bot.callback_query_handler(func=lambda call: call.data == "Librarian")
def initialize_librarian(call):
    u.is_librarian = True  # TODO: проверка типов(мб нет)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "Docs on hands")
def docs_on_hands(call):
    u.field = "Patron docs"  # TODO: обратиться по типу
    u.db_to_search = get_db(u.current.field)
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
    # TODO: прикрутить сам лист
    list = ["patron1", "faculty2", "Ramil-pezduk999"]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} now in the waiting list".format(list),
                          reply_markup=bot_features.get_inline_markup(
                              [["Make request", "Outstanding Request"],
                               ["OK", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Outstanding Request")
def initialize_librarian(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Request is done",
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"METHODS FOR SEARCH"


@bot.callback_query_handler(func=lambda call: call.data == "Actions with Patrons")
def search_patron(call):
    u.current.field = "Emails"  # TODO: обратиться по типу
    u.db_to_search = get_db(u.current.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter e-mail from list {}".format(u.current.db_to_search),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(
    func=lambda call: call.data == "Books" or call.data == "Articles" or call.data == "Audio/Video")
def search_doc(call):
    u.field = call.data  # TODO: обратиться по типу
    u.db_to_search = get_db(u.current.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter name of doc from list {}".format(u.current.db_to_search),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


def search(call):
    u.db_to_search = get_db(u.current.field)
    ID = call.chat.id
    mail = db.get(id=ID)[0].get_mail()
    u.current_object = call  # TODO: обратиться по типу
    if call.text in u.current.db_to_search:
        if u.current.user == "admin":
            message = "Choose action to do with {}".format(call.text)
            markup = u.keyboard_librarian_buttons_manage
        elif facbase.is_librarian(mail):
            message = "Choose action to do with {}".format(call.text)
            markup = u.keyboard_librarian_buttons_manage
            if u.current.field == "Books":  # костыльная проверка на док
                markup = u.keyboard_librarian_buttons_manage[:-1] + [
                    ["Waiting list", "Waiting list"]] + u.keyboard_librarian_buttons_manage[-1:]

        else:
            if u.current.field == "Patron docs":
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
        if u.current.user == "admin":
            message = "Do you want to add {} to database?".format(call.text)
            markup = u.keyboard_librarian_buttons_confirmation
        elif facbase.is_librarian(mail):
            message = "Do you want to add {} to database?".format(call.text)
            markup = u.keyboard_librarian_buttons_confirmation
        else:
            if u.current.field == "Patron docs":
                message = "Sorry, {} is not in your list, but you can try to find it in the Library".format(call.text)
                markup = u.keyboard_patron_buttons_home
            else:
                message = "Sorry, {} is not available. Try again. Choose needed type".format(call.text)
                markup = u.keyboard_buttons_library
    bot.send_message(call.chat.id, message, reply_markup=bot_features.get_inline_markup(markup))


def get_db(db):  # дешево-сердито, расписал только для патрона и книги
    if db == "Emails":
        return ["patron1", "patron2"]
    if db == "Books":
        return ["Book1", "Book2"]
    if db == "Patron docs":
        return ["doc1", "doc2"]
    if db == "Librarians":
        return ["lib1","lib2"]
        # "Articles": ["Article1", "Article2"],
        # "Audio/Video": ["Audio/Video1", "Audio/Video2"]


"METHODS FOR EDIT"


@bot.callback_query_handler(func=lambda call: call.data == "Edit")
def edit(call):
    types = get_type(u.current.field)
    text_types = ""  # TODO: тут к полям привязать, по которым искать я их хитромудро к инлайновым кнопкам привязал
    for i in types:
        text_types += ("{}\n".format(i[0]))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose parameter to edit:".format(text_types),
                          reply_markup=bot_features.get_inline_markup(types))


@bot.callback_query_handler(func=lambda
        call: call.data == "Imya" or call.data == "Familiya" or call.data == "title" or call.data == "author")  # TODO: следствие метода выше
def editing(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter new parameter for {} of {}".format(call.data, u.current.current_object.text),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, edited)


def edited(call):
    # TODO: Изменить поле u.field объекта u.current_object на call.text
    bot.send_message(call.chat.id,
                     text="Field {} of {} now equals to {}".format(u.current.field, u.current.current_object.text, call.text),
                     reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"KbIK db"


def get_type(obj):
    if obj == "Emails":
        return [["Imya", "Imya"], ["Familiya", "Familiya"]]
    if obj == "Books":
        return [["title", "title"], ["author", "author"]]


"DELETE, GETINFO AND ADD"


@bot.callback_query_handler(func=lambda call: call.data == "Delete")
def delete(call):
    # TODO: примерно как выше, но удалить
    u.current.db_to_search.remove(u.current.current_object.text)
    print(u.current.db_to_search)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is deleted from {}".format(u.current.current_object.text, u.current.field),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Add")
def add(call):
    list = ""
    print(u.current.field)
    print(get_type(u.current.field)[1][0])
    for i in range(len(get_type(u.current.field))):
        list+="{}, ".format(get_type(u.current.field)[i][0])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter values for the following fields using new line and commas: {}".format(list),#(get_type(u.current_object)))#TODO: fields этого объекта
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, adding)


def adding(call):
    array_of_values = call.text.split("\n")
    print(array_of_values)
    if u.current.field == "Book":
        doc = Book(title=u.current.title_or_name,author=array_of_values[0],publisher=array_of_values[1],year=array_of_values[2],edition=array_of_values[3],genre=array_of_values[4])
    elif u.current.field == "AV":
        doc = AV_Materials(title=u.current.title_or_name,author=array_of_values[0],price=array_of_values[1])
    elif u.current.field == "Aricle":
        doc = Article(title=u.current.title_or_name,author=array_of_values[0],journal=array_of_values[1],publication_date=array_of_values[2],editor=array_of_values[3])
    else:
        doc = "bla-bla"
    db.insert(doc.summary())

    print('SUCCESS')
    print(u.current.db_to_search)
    bot.send_message(call.chat.id, "Addition to database was successful",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))



@bot.callback_query_handler(func=lambda call: call.data == "Get information")
def get_info(call):
    # TODO: получить инфо объекта u.current_object
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is zaebis".format(u.current.current_object.text),
                          reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"BACK"


@bot.callback_query_handler(func=lambda call: call.data == "Back")
def back(call):
    ID = call.message.chat.id
    mail = db.get(id=ID)[0].get_mail()
    # TODO: наверно нужно перепривязать костыльную проверку к дб, но тут сам решай
    if u.current.user == "admin":
        markup = bot_features.get_inline_markup(u.keyboard_admin_buttons_home)
    elif not facbase.is_librarian(mail):
        markup = bot_features.get_inline_markup(u.keyboard_patron_buttons_home)
    else:
        markup = bot_features.get_inline_markup(u.keyboard_librarian_buttons_home)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do",
                          reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
