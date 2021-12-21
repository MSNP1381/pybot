# This bot is needed to connect two people and their subsequent anonymous communication
#
# Avaiable commands:
# `/start` - Just send you a messsage how to start
# `/find` - Find a person you can contact
# `/stop` - Stop active conversation

import telebot
from telebot import types
import os.path
import time
link_400='https://ppng.ir/d/CnxH'
link_comp='https://ppng.ir/d/phyf'
link_all='https://ppng.ir/d/Gl78'

API_TOKEN = ''

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
@bot.message_handler(commands=['stop'])
def removeusr(message):
    if(message.chat.id in user_dict.keys()):
        del(user_dict[message.chat.id])
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if(message.chat.id in user_dict.keys()):
        return
    msg = bot.reply_to(message,""" به ربات دفتر فرهنگی دانشکده کامپیوتر خوش آمدید.
                کار هاتون رو از منو پایین انتخاب کنید
""")

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('کلاس C#')
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

        if (ClsName == u'کلاس C#'):
            user_dict[chat_id] = User(ClsName)
            msg = bot.reply_to(message, 'کد دانشجویی خود را وارد کنید')
            bot.register_next_step_handler(msg, get_stdCode)
        else:
            msg = bot.send_message(message.chat.id, "انتخاب نامعتبر")
            bot.register_next_step_handler(msg, option_level)

    except Exception as e:
        msg=bot.reply_to(message, 'oooops')
        bot.register_next_step_handler(msg, send_welcome)
        print(e)


def get_stdCode(message):
    with open('db.csv', mode='a') as employee_file:
        try:
            std_code = message.text
            chat_id = message.chat.id                
            if (std_code.isdigit()):
                if (std_code.startswith('40052') and len(std_code) == 9):
                    u = user_dict[chat_id]
                    u.student_code = std_code
                    employee_file.write([chat_id, std_code,time.time()])
                    bot.reply_to(message, link_400)
                elif (std_code[2:].startswith('52') and len(std_code) == 8):
                    u = user_dict[chat_id]
                    u.student_code = std_code

                    employee_file.writerow([chat_id, std_code,time.time()])
                    bot.reply_to(message,link_comp)
                elif (len(std_code) == 8):
                    u = user_dict[chat_id]
                    u.student_code = std_code
                    employee_file.writerow([chat_id, std_code,time.time()])

                    bot.reply_to(message, link_all)
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
