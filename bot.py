import config
import telebot
import telegraph
import DataBase as db

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
    # bot.reply_to(message, 'http://telegra.ph/{}'.format(response['path']))
    # bot.reply_to(message, 'http://telegra.ph/Bruce-Eckels-Thinking-in-Java-4th-editon-01-29')
    # bot.reply_to(message, 'http://telegra.ph/Youve-been-visited-by-mrKeglya-02-02')
    db.insertBook("Thinking in Java",db.dictForBook("Hooj","http://telegra.ph/Bruce-Eckels-Thinking-in-Java-4th"
                                                           "-editon-01-29"))
    print(db.getBook("Thinking in Java"))
    d = db.getBook("Thinking in Java")
    string = "" + d["description"] + "\n" + d["reference"]
    bot.send_message(message.chat.id, string)



@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy,how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)

