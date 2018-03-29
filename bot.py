import telebot
import token
import utilities
import config

bot = telebot.TeleBot(config.token1)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, utilities.greeting)
