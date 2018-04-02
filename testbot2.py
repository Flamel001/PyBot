import types
import config
import database as db
from telebot import *
import telegraph
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

@bot.message_handler(commands=["start"])
def greeting(message):
    # TODO: Проверить, есть ли чел в дб, если да, то на его стартовый экран, если нет - то инициализация
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
    if call.text[-13:] == u.domain and len(call.text)>13:
        u.current_email=call.text
        u.pin = veri.pin_generator()
        veri.pin_sender(call.text,u.pin)
        bot.send_message(call.chat.id, "Enter code that we send to your email")
        bot.register_next_step_handler(call,pin_checker)
    else:
        bot.send_message(call.chat.id, "Please try again")
        bot.register_next_step_handler(call, auth)



def pin_checker(call):
    if call.text == u.pin:
            # reply = types.ReplyKeyboardMarkup(True, False, True, 1)
            # reply.add(types.KeyboardButton(text="Send phone number",request_contact=True))
            # bot.send_message(call.chat.id, "Enter your name",reply_markup=reply)
        u.auth_val_arr.clear()
        bot.send_message(call.chat.id, "Enter your name")
        bot.register_next_step_handler(call, name)
    else:
        bot.send_message(call.chat.id, "Please try again")
        bot.register_next_step_handler(call, pin_checker)


def name(call):
    print(call.text)
    u.auth_val_arr.append(call.text)
    #TODO: сохранить имя(call.text) в дб
    bot.send_message(call.chat.id, "Enter your number")
    bot.register_next_step_handler(call, number)


def number(call):
    print(call.text)
    u.auth_val_arr.append(call.text)
    #TODO: сохранить номер(call.text) в дб
    bot.send_message(call.chat.id, "Enter your address")
    bot.register_next_step_handler(call, address)


def address(call):
    print(call.text)
    u.auth_val_arr.append(call.text)
    #TODO: сохранить адрес(call.text) в дб
    temp = dict()
    for i in range(3):
        temp[u.auth_arr[i]] = u.auth_val_arr[i]
    temp["id"] = str(call.chat.id)
    temp["alias"] = call.from_user.username
    temp["mail"] = u.current_email

    id = temp["id"]
    name = temp["name"]
    mail = temp["mail"]
    number = temp["number"]
    alias = temp["alias"]
    address = temp["address"]

    if facbase.is_instructor(mail):
        usr = Instructor(id,alias,name,mail,number,address)
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



@bot.callback_query_handler(func=lambda call: call.data == "Patron")
def initialize_patron(call):
    u.is_librarian = False  # TODO: сделать через проверку типа в дб, думаю
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "My docs")
def my_docs(call):
    u.field = "Patron docs"  # TODO: обратиться в дб по полю
    u.db_to_search = get_db(u.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter doc from list {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Reserve")
def renew(call):
    u.field = "Patron docs"  # TODO: обратиться в дб по полю
    u.db_to_search = get_db(u.field)
    u.db_to_search.append(u.current_object.text)
    print(u.db_to_search)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is added to {}".format(u.current_object.text, u.field))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "To waiting list")
def patron_waiting_list(call):
    # TODO:прикрутить сам вейтинг лист и какое то уведомление молодого о том, когда появится книга
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="You are added to the waiting list for {}".format(u.current_object.text))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Return")
def return_doc(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Please, go to the Library and return your book")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Renew")
def renew(call):
    # TODO: update time
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Time for your doc updated")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Tech support")
def tech_sup(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Here are aliases of tech support:\n @N_Flamel\n@jopa_enota",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


"LIBRARIAN"


@bot.callback_query_handler(func=lambda call: call.data == "Librarian")
def initialize_librarian(call):
    u.is_librarian = True  # TODO: проверка типов(мб нет)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "Docs on hands")
def docs_on_hands(call):
    u.field = "Patron docs"  # TODO: обратиться по типу
    u.db_to_search = get_db(u.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="docs of user xyuzer are {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Library")
def library(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose type of doc")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_buttons_library))


@bot.callback_query_handler(func=lambda call: call.data == "Waiting list")
def initialize_librarian(call):
    # TODO: прикрутить сам лист
    list = ["patron1", "faculty2", "Ramil-pezduk999"]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} now in the waiting list".format(list))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(
                                      [["Make  ebenii request", "Outstanding Request"],
                                       ["Spasibo-dosvidaniya", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Outstanding Request")
def initialize_librarian(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Molodec, sdelal request, proizoshlo tseloe nixoya")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup([["Spasibo-dosvidaniya", "Back"]]))


"METHODS FOR SEARCH"


@bot.callback_query_handler(func=lambda call: call.data == "Actions with Patrons")
def search_patron(call):
    u.field = "Emails"  # TODO: угадай что?
    u.db_to_search = get_db(u.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter e-mail from list {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(
    func=lambda call: call.data == "Books" or call.data == "Articles" or call.data == "Audio/Video")
def search_doc(call):
    u.field = call.data  # TODO: и тут то же самое
    u.db_to_search = get_db(u.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter name of doc from list {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


def search(call):
    u.db_to_search = get_db(u.field)
    ID = call.chat.id
    mail = db.get(id=ID)[0].get_mail()
    u.current_object = call  # TODO: ага
    if call.text in u.db_to_search:
        if facbase.is_librarian(mail):
            message = "Choose action to do with {}".format(call.text)
            markup = u.keyboard_librarian_buttons_manage
            if u.field == "Books":  # костыльная проверка на док
                markup = u.keyboard_librarian_buttons_manage[:-1] + [
                    ["Waiting list", "Waiting list"]] + u.keyboard_librarian_buttons_manage[-1:]

        else:
            if u.field == "Patron docs":
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
        if facbase.is_librarian(mail):
            message = "Do you want to add {} to database?".format(call.text)
            markup = u.keyboard_librarian_buttons_cobfirmation
        else:
            if u.field == "Patron docs":
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
        # "Articles": ["Article1", "Article2"],
        # "Audio/Video": ["Audio/Video1", "Audio/Video2"]


"METHODS FOR EDIT"


@bot.callback_query_handler(func=lambda call: call.data == "Edit")
def edit(call):
    types = get_type(u.field)
    text_types = ""  # TODO: тут к полям привязать, по которым искать я их хитромудро к инлайновым кнопкам привязал
    for i in types:
        text_types += ("{}\n".format(i[0]))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose parameter to edit:".format(text_types))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(types))


@bot.callback_query_handler(func=lambda
        call: call.data == "Imya" or call.data == "Familiya" or call.data == "title" or call.data == "author")  # TODO: следствие метода выше
def editing(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter new parameter for {} of {}".format(call.data, u.current_object.text))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, edited)


def edited(call):
    # TODO: Изменить поле u.field объекта u.current_object на call.text
    bot.send_message(call.chat.id, "Field {} of {} now equals to {}".format(u.field, u.current_object.text, call.text),
                     reply_markup=bot_features.get_inline_markup([["ebanumba, zaebis", "Back"]]))


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
    u.db_to_search.remove(u.current_object.text)
    print(u.db_to_search)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is deleted from {}".format(u.current_object.text, u.field))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Add")
def add(call):
    # TODO: и добавить
    u.db_to_search.append(u.current_object.text)
    print(u.db_to_search)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is added to {}".format(u.current_object.text, u.field))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Get information")
def get_info(call):
    # TODO: получить инфо объекта u.current_object
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is zaebis".format(u.current_object.text))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"BACK"


@bot.callback_query_handler(func=lambda call: call.data == "Back")
def back(call):
    ID = call.message.chat.id
    mail = db.get(id=ID)[0].get_mail()
    # TODO: наверно нужно перепривязать костыльную проверку к дб, но тут сам решай
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do")
    if not facbase.is_librarian(mail):
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))
    else:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))


if __name__ == '__main__':
    bot.polling(none_stop=True)
