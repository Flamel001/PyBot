import config
import telebot
import telegraph

bot = telebot.TeleBot(config.token2)
ph = telegraph.Telegraph()


"""
    Usage of Telegraph api. Integration of telegraph api for "about" features.
    
"""
ph.create_account(short_name='InnoLib')
response = ph.create_page('Bruce Eckels Thinking in Java',
                          html_content="<p> Thinking in Java should be read cover to cover by every Java programmer, "
                                       "then kept close at hand for frequent reference. The exercises are challenging,"
                                       " and the chapter on Collections is superb!"
                                       " Not only did this book help me to pass the Sun Certified Java Programmer exam;"
                                       " it’s also the first book I turn to whenever I have a Java question. </p>")


@bot.message_handler(commands=['Books'])
def telegraph_func(message):
    bot.reply_to(message, 'http://telegra.ph/{}'.format(response['path']))
    bot.reply_to(message, 'http://telegra.ph/Bruce-Eckels-Thinking-in-Java-4th-editon-01-29')


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy,how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


@bot.message_handler(regexp="hui")
def keyboard(message):
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row('Books')
    markup.row('My orders')
    markup.row('Help')
    bot.send_message(message.chat.id, "Please,choose the option.", reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
