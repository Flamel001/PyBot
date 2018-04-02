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
        if aut.if_librarian(message.chat.id):
            print("librarian")
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))
        else:
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


def auth(call):
    if call.text[-13:] == u.domain and len(call.text) > 13:
        u.current_email = call.text
        u.pin = veri.pin_generator()
        veri.pin_sender(call.text, u.pin)
        bot.send_message(call.chat.id, "Enter code that we send to your email")
        bot.register_next_step_handler(call, pin_checker)
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
    # TODO: сохранить имя(call.text) в дб
    bot.send_message(call.chat.id, "Enter your number")
    bot.register_next_step_handler(call, number)


def number(call):
    print(call.text)
    u.auth_val_arr.append(call.text)
    # TODO: сохранить номер(call.text) в дб
    bot.send_message(call.chat.id, "Enter your address")
    bot.register_next_step_handler(call, address)


def address(call):
    print(call.text)
    u.auth_val_arr.append(call.text)
    # TODO: сохранить адрес(call.text) в дб
    temp = dict()
    for i in range(3):
        temp[u.auth_arr[i]] = u.auth_val_arr[i]
    temp["id"] = call.chat.id
    temp["alias"] = call.from_user.username
    temp["mail"] = u.current_email

    id = temp["id"]
    name = temp["name"]
    mail = temp["mail"]
    number = temp["number"]
    alias = temp["alias"]
    address = temp["address"]

    if facbase.is_instructor(id):
        usr = Instructor(id, alias, name, mail, number, address)
    elif facbase.is_ta(id):
        usr = TA(id, alias, name, mail, number, address)
    elif facbase.is_professor(id):
        usr = Professor(id, alias, name, mail, number, address)
    elif facbase.is_vp(id):
        usr = VP(id, alias, name, mail, number, address)
    else:
        usr = Student(id, alias, name, mail, number, address)

    db.insert(usr.summary())
    print(temp)

    bot.send_message(call.chat.id, "Congratulations, registration is finished. Now choose, what do you want to do",
                     reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "Patron")
def initialize_patron(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "My docs")
def my_docs(call):
    u.field = "Patron docs"
    u.db_to_search = list(db.get(id=call.message.chat.id)[0].get_docs_list().keys())
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter doc from list {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Reserve")
def renew(call):
    u.field = "Patron docs"  # TODO: обратиться в дб по полю
    # u.db_to_search = get_db(u.field)
    # u.db_to_search.append(u.current_object.text)
    b.booking(usr=db.get(id=call.chat.id)[0], document=u.current_object)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is added to {}".format(u.current_object.get_title(), u.field))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "To waiting list")
def patron_waiting_list(call):
    # TODO:прикрутить сам вейтинг лист и какое то уведомление молодого о том, когда появится книга
    b.booking(usr=db.get(id=call.chat.id)[0], document=u.current_object)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="You are added to the waiting list for {}".format(u.current_object.get_id()))
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
                          text=b.booking(usr=db.get(id=call.chat.id)[0], document=u.current_object))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Tech support")
def tech_sup(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Here are aliases of tech support:\n @N_Flamel",
                          reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


"LIBRARIAN"


@bot.callback_query_handler(func=lambda call: call.data == "Librarian")
def initialize_librarian(call):
    u.is_librarian = aut.if_librarian(call.chat.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "Docs on hands")
def docs_on_hands(call):
    u.field = "Patron docs"  # TODO: обратиться по типу
    all_docs_objects = db.get(type_book="Book") + db.get(type_book="Article") + db.get(type_book="AV")
    u.db_to_search = [all_docs_objects[i].get_title() for i in range(len(all_docs_objects))]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="docs on hands are {}".format(u.db_to_search))
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
    l = list(db.get(title=u.current_object.get_title())[0].get_queue().values())
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} now in the waiting list".format(l))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(
                                      [["Make  ebenii request", "Outstanding Request"],
                                       ["Spasibo-dosvidaniya", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Outstanding Request")
def initialize_librarian(call):
    db.update(title=u.current_object.get_title(), queue=str(dict()))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now, no person waits for the document")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup([["Thanks", "Back"]]))


"METHODS FOR SEARCH"


@bot.callback_query_handler(func=lambda call: call.data == "Actions with Patrons")
def search_patron(call):
    u.field = "Emails"  # TODO: list of emails
    u.db_to_search = db.get_all_similar_info(mail="yes")
    print("Hello, these are emails " + str(u.db_to_search))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter e-mail from list {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(
    func=lambda call: call.data == "Books" or call.data == "Articles" or call.data == "Audio/Video")
def search_doc(call):
    if call.data == "Books":
        u.field = "Book"
    elif call.data == "Articles":
        u.field = "Article"
    elif call.data == "Audio/Video":
        u.field = "AV"
    list_of_docs = db.get(type_book=u.field)
    u.db_to_search = [i.get_title() for i in list_of_docs]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter name of doc from list {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


def search(call):
    if "innopolis.ru" in call.text.split("@"):
        list_of_all_books = db.get(type_user="TA") + db.get(type_user="VP") + db.get(type_user="Instructor") + db.get(
            type_user="Professor") + db.get(type_user="Student")
        u.db_to_search = [i.get_mail() for i in list_of_all_books]
        u.current_object = db.get(mail=call.text)[0]  # Searchit' chto?
    else:
        list_of_all_books = db.get(type_book=u.field)
        u.db_to_search = [i.get_title() for i in list_of_all_books]
        u.current_object = db.get(title=call.text)[0]
    if call.text in u.db_to_search:
        if aut.if_librarian(call.chat.id):
            message = "Choose action to do with {}".format(call.text)
            markup = u.keyboard_librarian_buttons_manage
            if u.field == "Book" or u.field == "Article" or u.field == "AV":  # костыльная проверка на док
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
        if aut.if_librarian(call.chat.id):
            message = "Do you want to add {} to database?".format(call.text)
            markup = u.keyboard_librarian_buttons_confirmation
        else:
            if u.field == "Patron docs":
                message = "Sorry, {} is not in your list, but you can try to find it in the Library".format(call.text)
                markup = u.keyboard_patron_buttons_home
            else:
                message = "Sorry, {} is not available. Try again. Choose needed type".format(call.text)
                markup = u.keyboard_buttons_library
    bot.send_message(call.chat.id, message, reply_markup=bot_features.get_inline_markup(markup))


#
# def get_db(db):  # дешево-сердито, расписал только для патрона и книги
#     if db == "Emails":
#         return ["patron1", "patron2"]
#     if db == "Books":
#         return ["Book1", "Book2"]
#     if db == "Patron docs":
#         return ["doc1", "doc2"]
#         # "Articles": ["Article1", "Article2"],
#         # "Audio/Video": ["Audio/Video1", "Audio/Video2"]


"METHODS FOR EDIT"


@bot.callback_query_handler(func=lambda call: call.data == "Edit")
def edit(call):
    types = get_type(u.field)
    text_types = ""  # TODO: update of one field
    print(str(types))
    for i in range(0, len(types)):
        text_types += ("{}\n".format(types[i][0]))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose parameter to edit:".format(text_types))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(types))


@bot.callback_query_handler(func=lambda
        call: call.data == "id" or call.data == "alias" or call.data == "name" or call.data == "mail" or call.data == "number" or call.data == "address" or call.data == "title" or call.data == "author"
              or call.data == "owner" or call.data == "price" or call.data == "year" or call.data == "publication_date" or call.data == "publisher"
              or call.data == "journal" or call.data == "editor" or call.data == "edition" or call.data == "genre" or call.data == "bestseller" or call.data == "reference")  # TODO: следствие метода выше
def editing(call):
    u.field = call.data
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter new parameter for {} of {}".format(call.data,
                                                                         u.current_object.get_title() if isinstance(
                                                                             u.current_object, Book) or isinstance(
                                                                             u.current_object, Article) or isinstance(
                                                                             u.current_object,
                                                                             AV_Materials) else u.current_object.get_id()))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, edited)


def edited(call):
    # TODO: update u.field field
    print("This is field " + str(u.field) + " this is call.text " + str(call.text) + " " + str(u.current_object))
    if u.field == "id":
        db.update(id=aut.check_user(u.current_object.summary()), new_id=int(call.text))
        u.field = "Emails"
    elif u.field == "alias":
        db.update(id=aut.check_user(u.current_object.summary()), alias=call.text)
        u.field = "Emails"
    elif u.field == "name":
        db.update(id=aut.check_user(u.current_object.summary()), name=call.text)
        u.field = "Emails"
    elif u.field == "mail":
        db.update(id=aut.check_user(u.current_object.summary()), mail=call.text)
        u.field = "Emails"
    elif u.field == "number":
        db.update(id=aut.check_user(u.current_object.summary()), number=call.text)
        u.field = "Emails"
    elif u.field == "address":
        print(str(u.current_object.summary()) + " njd " + str(call.text))
        db.update(id=aut.check_user(u.current_object.summary()), address=call.text)
        print("Hello")
        u.field = "Emails"
    elif u.field == "title":
        t = aut.check_doc(u.current_object.summary())
        db.update(title=t, new_title=call.text)
        u.field = "Book"
    elif u.field == "author":
        db.update(title=aut.check_doc(u.current_object.summary()), author=call.text)
        u.field = "Book"
    elif u.field == "owner":
        db.update(title=aut.check_doc(u.current_object.summary()), owner=call.text)
        u.field = "Book"
    elif u.field == "price":
        db.update(title=aut.check_doc(u.current_object.summary()), price=call.text)
        u.field = "Book"
    elif u.field == "url":
        db.update(title=aut.check_doc(u.current_object.summary()), url=call.text)
        u.field = "Book"
    elif u.field == "publication_date":
        db.update(title=aut.check_doc(u.current_object.summary()), publication_date=call.text)
        u.field = "Book"
    elif u.field == "publisher":
        db.update(title=aut.check_doc(u.current_object.summary()), publisher=call.text)
        u.field = "Book"
    elif u.field == "year":
        db.update(title=aut.check_doc(u.current_object.summary()), year=call.text)
        u.field = "Book"
    elif u.field == "journal":
        db.update(title=aut.check_doc(u.current_object.summary()), journal=call.text)
        u.field = "Book"
    elif u.field == "editor":
        db.update(title=aut.check_doc(u.current_object.summary()), editor=call.text)
        u.field = "Book"
    elif u.field == "edition":
        db.update(title=aut.check_doc(u.current_object.summary()), edition=call.text)
        u.field = "Book"
    elif u.field == "genre":
        db.update(title=aut.check_doc(u.current_object.summary()), genre=call.text)
        u.field = "Book"
    elif u.field == "bestseller":
        db.update(title=aut.check_doc(u.current_object.summary()), bestseller=call.text)
        u.field = "Book"
    elif u.field == "reference":
        db.update(title=aut.check_doc(u.current_object.summary()), reference=call.text)
        u.field = "Book"
    bot.send_message(call.chat.id, "Field {} of {} now equals to {}".format(u.field,
                                                                            u.current_object.get_title() if isinstance(
                                                                                u.current_object, Book) or isinstance(
                                                                                u.current_object,
                                                                                Article) or isinstance(u.current_object,
                                                                                                       AV_Materials) else u.current_object.get_id(),
                                                                            call.text),
                     reply_markup=bot_features.get_inline_markup([["ebanumba, zaebis", "Back"]]))


"KbIK db"


def get_type(obj):
    if obj == "Emails":
        return [["Id", "id"], ["Alias", "alias"], ["Name", "name"], ["Mail", "mail"], ["Number", "number"],
                ["Address", "address"], ["Back", "Back"]]
    if obj == "Book":
        return [["Title", "title"], ["Author", "author"], ["Owner", "owner"], ["Url", "url"],
                ["Year", "year"], ["Publisher", "publisher"], ["Edition", "edition"], ["Genre", "genre"],
                ["Bestseller", "bestseller"], ["Reference", "reference"], ["Back", "Back"]]
    elif obj == "Article":
        return [["Title", "title"], ["Author", "author"], ["Owner", "owner"], ["Url", "url"],
                ["Year", "year"], ["Journal", "journal"], ["Publication date", "publication_date"], ["Editor", "editor"], ["Back", "Back"]]
    elif obj == "AV":
        return [["Title", "title"], ["Author", "author"], ["Owner", "owner"], ["Url", "url"], ["Price", "price"], ["Back", "Back"]]


"DELETE, GETINFO AND ADD"


@bot.callback_query_handler(func=lambda call: call.data == "Delete")
def delete(call):
    db.delete(id=aut.check_user(u.current_object.summary()), title=aut.check_doc(u.current_object.summary()))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is deleted from {}".format(
                              u.current_object.get_title() if isinstance(u.current_object, Book) or isinstance(
                                  u.current_object, Article) or isinstance(u.current_object,
                                                                           AV_Materials) else u.current_object.get_id(),
                              u.field))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Add")
def add(call):
    # TODO: и change
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
                          text="{} is zaebis".format(u.current_object.summary()))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


"BACK"


@bot.callback_query_handler(func=lambda call: call.data == "Back")
def back(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do")
    if not aut.if_librarian(call.message.chat.id):
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))
    else:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))


if __name__ == '__main__':
    bot.polling(none_stop=True)
