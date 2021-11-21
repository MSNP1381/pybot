# This bot is needed to connect two people and their subsequent anonymous communication
#
# Avaiable commands:
# `/start` - Just send you a messsage how to start
# `/find` - Find a person you can contact
# `/stop` - Stop active conversation

import telebot
from telebot import types
import csv
import time

  
API_TOKEN = '2140199987:AAHH3NvanKtAr6C2t4uUkpXp3fzWOia99b0'

bot = telebot.TeleBot(API_TOKEN)
user_dict = {}


# The `freeid` variable is needed to contain chat id, that want to start conversation
# Or, in other words: chat id of user in the search


class User:
    def __init__(self, clas):
        self.student_code = None
        self.state = None
        self.class1 = clas


# `/start` command handler
#
# That command only sends you 'Just use /find command!'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message,""" به ربات دفتر فرهنگی دانشکده کامپیوتر خوش آمدید.
                کار هاتون رو از منو پایین انتخاب کنید
""")

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('کلاس ریاضی')
    msg = bot.reply_to(message, 'کلاس خود را انتخاب کنید', reply_markup=markup)
    bot.register_next_step_handler(msg, option_level)


#  chat_id = message.chat.id
#         name = message.text
#         user = User(name)
#         user_dict[chat_id] = user


def option_level(message):
    
    try:
        chat_id = message.chat.id
        ClsName = message.text

        if (ClsName == u'کلاس ریاضی'):
            user_dict[chat_id] = User(ClsName)
            msg = bot.reply_to(message, 'کد دانشجویی خود را وارد کنید')
            bot.register_next_step_handler(msg, get_stdCode)
        else:
            raise Exception("انتخاب نا معتبر")
       
    except Exception as e:
        msg=bot.reply_to(message, 'oooops')
        bot.register_next_step_handler(msg, send_welcome)
        print(e)


def get_stdCode(message):
    with open('db.csv', mode='w') as employee_file: 
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        try:
            std_code = message.text
            chat_id = message.chat.id

            if (std_code.isdigit()):
                if (std_code.startswith('40052') and len(std_code) == 9):
                    u = user_dict[chat_id]
                    u.student_code = std_code
                    employee_writer.writerow([chat_id, std_code,time.time()])
    
                    bot.reply_to(message, "Tlink 400")
                elif (std_code[2:].startswith('52') and len(std_code) == 8):
                    u = user_dict[chat_id]
                    u.student_code = std_code
                    
                    employee_writer.writerow([chat_id, std_code,time.time()])
                    bot.reply_to(message, "link comp")
                elif (len(std_code) == 8):
                    u = user_dict[chat_id]
                    u.student_code = std_code
                    employee_writer.writerow([chat_id, std_code,time.time()])
                    
                    bot.reply_to(message, "link all")
                else:
                    bot.reply_to(message, "کد دانشجویی شما معتبر نیست")
                    msg = bot.send_message(message.chat.id, 'کد دانشجویی خود را دوباره وارد کنید')
                    bot.register_next_step_handler(msg, get_stdCode)
            else:
                bot.reply_to(message, "کد دانشجویی معتبر وارد کنید")
                msg = bot.send_message(message.chat.id, 'کد دانشجویی خود را دوباره وارد کنید')
                bot.register_next_step_handler(msg, get_stdCode)

            print(message.text)
        except Exception as e:
            bot.reply_to(message, 'oooops')
            print(e)


bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()
