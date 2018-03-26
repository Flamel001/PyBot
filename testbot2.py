import types
import config
from telebot import *
import telegraph
import datetime as date
import utilities as u
import verification as veri
import booking as b
import bot_features
from documents import *
from user import *

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
    if True:
        bot.send_message(message.chat.id, "Please choose your type",
                         reply_markup=bot_features.get_inline_markup(u.keyboard_buttons_choice))
    else:
        if u.is_librarian:
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))
        else:
            bot.send_message(message.chat.id, "Now choose what you want to do",
                             reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))

"PATRON"


@bot.callback_query_handler(func=lambda call: call.data == "Patron")
def initialize_patron(call):
    u.is_librarian = False#TODO: сделать через проверку типа в дб, думаю
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "My docs")
def my_docs(call):
    u.field = "Patron docs"#TODO: обратиться в дб по полю
    u.db_to_search = get_db(u.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter doc from list {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)



@bot.callback_query_handler(func=lambda call: call.data == "Reserve")
def renew(call):
    u.field = "Patron docs"#TODO: обратиться в дб по полю
    u.db_to_search = get_db(u.field)
    u.db_to_search.append(u.current_object.text)
    print(u.db_to_search)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} is added to {}".format(u.current_object.text, u.field))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "To waiting list")
def patron_waiting_list(call):
    #TODO:прикрутить сам вейтинг лист и какое то уведомление молодого о том, когда появится книга
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="You are added to the waiting list for {}".format(u.current_object.text))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))


@bot.callback_query_handler(func=lambda call: call.data == "Return")
def return_doc(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Please, go to the Library and return your book")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup([["OK!","Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Renew")
def renew(call):
    #TODO: update time
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Time for your doc updated")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup([["OK!", "Back"]]))


@bot.callback_query_handler(func=lambda call: call.data == "Tech support")
def tech_sup(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Here are aliases of tech support:\n @N_Flamel\n@jopa_enota",reply_markup=bot_features.get_inline_markup([["OK!","Back"]]))


"LIBRARIAN"


@bot.callback_query_handler(func=lambda call: call.data == "Librarian")
def initialize_librarian(call):
    u.is_librarian = True#TODO: проверка типов(мб нет)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))


@bot.callback_query_handler(func=lambda call: call.data == "Docs on hands")
def docs_on_hands(call):
    u.field = "Patron docs"#TODO: обратиться по типу
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
    #TODO: прикрутить сам лист
    list = ["patron1","faculty2","Ramil-pezduk999"]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="{} now in the waiting list".format(list))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup([["Spasibo-dosvidaniya","Back"]]))




"METHODS FOR SEARCH"
@bot.callback_query_handler(func=lambda call: call.data == "Actions with Patrons")
def search_patron(call):
    u.field = "Emails"#TODO: угадай что?
    u.db_to_search = get_db(u.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter e-mail from list {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


@bot.callback_query_handler(func=lambda call: call.data == "Books" or call.data == "Articles" or call.data == "Audio/Video")
def search_doc(call):
    u.field = call.data #TODO: и тут то же самое
    u.db_to_search = get_db(u.field)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter name of doc from list {}".format(u.db_to_search))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, search)


def search(call):
    u.db_to_search = get_db(u.field)
    u.current_object = call  # TODO: ага
    if call.text in u.db_to_search:
        if u.is_librarian:
            message = "Choose action to do with {}".format(call.text)
            markup = u.keyboard_librarian_buttons_manage
        else:
            if u.field == "Patron docs":
                message = "What do you want to do with {}?".format(call.text)
                markup = u.keyboard_patron_buttons_doc
            else:
                if False:#TODO: тут должно чекать, если количество книг>0
                    message = "Do you want to reserve {}?".format(call.text)
                    button = "Reserve"
                else:
                    message = "Do you want to be added to the waiting list to take {} when it will be availible?".format(call.text)
                    button = "To waiting list"
                markup = [[button,button]]
    else:
        if u.is_librarian:
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


def get_db(db):#дешево-сердито, расписал только для патрона и книги
    if db == "Emails":
        return ["patron1", "patron2"]
    if db == "Books":
        return ["Book1", "Book2"]
    if db == "Patron docs":
        return ["doc1","doc2"]
        # "Articles": ["Article1", "Article2"],
        # "Audio/Video": ["Audio/Video1", "Audio/Video2"]


"METHODS FOR EDIT"
@bot.callback_query_handler(func=lambda call: call.data == "Edit")
def edit(call):
    types = get_type(u.field)
    text_types = ""#TODO: тут к полям привязать, по которым искать я их хитромудро к инлайновым кнопкам привязал
    for i in types:
        text_types+= ("{}\n".format(i[0]))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Choose parameter to edit:".format(text_types))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(types))


@bot.callback_query_handler(func=lambda call: call.data == "Imya" or call.data == "Familiya" or call.data == "title" or call.data == "author")#TODO: следствие метода выше
def editing(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Enter new parameter for {} of {}".format(call.data, u.current_object.text))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_button_back))
    bot.register_next_step_handler(call.message, edited)


def edited(call):
    # TODO: Изменить поле u.field объекта u.current_object на call.text
    bot.send_message(call.chat.id, "Field {} of {} now equals to {}".format(u.field,u.current_object.text,call.text),
                     reply_markup=bot_features.get_inline_markup([["ebanumba, zaebis","Back"]]))

"KbIK db"
def get_type(obj):
    if obj == "Emails":
        return [["Imya","Imya"],[ "Familiya","Familiya"]]
    if obj == "Books":
        return [["title","title"],[ "author", "author"]]


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
    #TODO: наверно нужно перепривязать костыльную проверку к дб, но тут сам решай
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Now choose what you want to do")
    if not u.is_librarian:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=bot_features.get_inline_markup(u.keyboard_patron_buttons_home))
    else:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=bot_features.get_inline_markup(u.keyboard_librarian_buttons_home))


if __name__ == '__main__':
    bot.polling(none_stop=True)