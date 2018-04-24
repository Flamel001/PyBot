from telebot import types
import utilities

__number = 0


def get_reply_markup(button_titles_array):
    reply = types.ReplyKeyboardMarkup(True, False, True, 1)
    for button_title in button_titles_array:
        reply.add(types.KeyboardButton(text=button_title))
    return reply


def get_inline_markup(button_array):
    inline = types.InlineKeyboardMarkup()
    for button in button_array:
        inline.add(types.InlineKeyboardButton(text=button[0],callback_data=button[1]))
    return inline



