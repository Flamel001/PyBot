from telebot import types
import utilities

__number = 0


def get_reply_markup(button_titles_array):
    reply = types.ReplyKeyboardMarkup(True, False, True, 1)
    for button_title in button_titles_array:
        reply.add(types.KeyboardButton(text=button_title))
    return reply


def get_inline_markup(button_array):#left_amount
    # if len(button_array)==3:
    #     inline = types.InlineKeyboardMarkup(3)
    # else:
    #     inline = types.InlineKeyboardMarkup()
    inline = types.InlineKeyboardMarkup()
    for button in button_array:
        inline.add(types.InlineKeyboardButton(text=button[0],callback_data=button[1]))
    return inline
    global __number
    exp = '{}/{}'.format(__number + 1, db.get_count_of_different_books())
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Reserve", callback_data="Book"))
    markup.add(types.InlineKeyboardButton(text=(str(left_amount) + " left"), callback_data="Left"))
    markup.add(types.InlineKeyboardButton(text='⬅', callback_data='prev'),
               types.InlineKeyboardButton(text=exp, callback_data='counter'),
               types.InlineKeyboardButton(text="➡", callback_data='next'))
    return markup


def get_current_book_number():
    return __number


def increment_book_number():
    global __number
    if __number == db.get_count_of_different_books() - 1:
        __number = 0
    else:
        __number+=1


def decrement_book_number():
    global __number
    if __number == 0:
        __number = db.get_count_of_different_books() - 1
    else:
        __number -= 1
