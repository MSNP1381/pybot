# This bot is needed to connect two people and their subsequent anonymous communication
#
# Avaiable commands:
# `/start` - Just send you a messsage how to start
# `/find` - Find a person you can contact
# `/stop` - Stop active conversation

import telebot
from telebot import types

# Initialize bot with your token
bot = telebot.TeleBot('2140199987:AAHH3NvanKtAr6C2t4uUkpXp3fzWOia99b0')

# The `users` variable is needed to contain chat ids that are either in the search or in the active dialog, like {chat_id, chat_id}
users = {}
# The `freeid` variable is needed to contain chat id, that want to start conversation
# Or, in other words: chat id of user in the search
freeid = None

# `/start` command handler
#
# That command only sends you 'Just use /find command!'


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, 'Just use /find command!')


@bot.message_handler()
def function_name(message):
    #bot.reply_to(message, "This is a message handler")
    std_code = message.text
    if(std_code.isdigit()):
        if(std_code.startswith('40052') and len(std_code) == 9):
            bot.reply_to(message, "Tlink 400")
        elif(std_code[2:].startswith('52') and len(std_code) == 8):
            bot.reply_to(message, "link comp")
        elif(len(std_code) == 8):
            bot.reply_to(message, "link all")
        else:
            bot.reply_to(message, "std code not valid")
    else:
            bot.reply_to(message, "print valid code")
        
    print(message.text)


# `/find` command handler
#
# That command finds opponent for you
#
# That command according to the following principle:
# 1. You have written `/find` command
# 2. If you are already in the search or have an active dialog, bot sends you 'Shut up!'
# 3. If not:
#   3.1. Bot sends you 'Finding...'
#   3.2. If there is no user in the search:
#       3.2.2. `freeid` updated with `your_chat_id`
#   3.3. If there is user in the search:
#       3.3.1. Both you and the user in the search recieve the message 'Founded!'
#       3.3.2. `users` updated with a {user_in_the_search_chat_id, your_chat_id}
#       3.3.3. `users` updated with a {your_chat_id, user_in_the_search_id}
#       3.3.4. `freeid` updated with `None`
@bot.message_handler(commands=['find'])
def find(message: types.Message):
    global freeid

    if message.chat.id not in users:
        bot.send_message(message.chat.id, 'Finding...')

        if freeid == None:
            freeid = message.chat.id
        else:
            # Question:
            # Is there any way to simplify this like `bot.send_message([message.chat.id, freeid], 'Founded!')`?
            bot.send_message(message.chat.id, 'Founded!')
            bot.send_message(freeid, 'Founded!')

            users[freeid] = message.chat.id
            users[message.chat.id] = freeid
            freeid = None

        print(users, freeid)  # Debug purpose, you can remove that line
    else:
        bot.send_message(message.chat.id, 'Shut up!')

# `/stop` command handler
#
# That command stops your current conversation (if it exist)
#
# That command according to the following principle:
# 1. You have written `/stop` command
# 2. If you are not have active dialog or you are not in search, bot sends you 'You are not in search!'
# 3. If you are in active dialog:
#   3.1. Bot sends you 'Stopping...'
#   3.2. Bot sends 'Your opponent is leavin`...' to your opponent
#   3.3. {your_opponent_chat_id, your_chat_id} removes from `users`
#   3.4. {your_chat_id, your_opponent_chat_id} removes from `users`
# 4. If you are only in search:
#   4.1. Bot sends you 'Stopping...'
#   4.2. `freeid` updated with `None`


@bot.message_handler(commands=['stop'])
def stop(message: types.Message):
    global freeid

    if message.chat.id in users:
        bot.send_message(message.chat.id, 'Stopping...')
        bot.send_message(users[message.chat.id], 'Your opponent is leavin`...')

        del users[users[message.chat.id]]
        del users[message.chat.id]

        print(users, freeid)  # Debug purpose, you can remove that line
    elif message.chat.id == freeid:
        bot.send_message(message.chat.id, 'Stopping...')
        freeid = None

        print(users, freeid)  # Debug purpose, you can remove that line
    else:
        bot.send_message(message.chat.id, 'You are not in search!')

# message handler for conversation
#
# That handler needed to send message from one opponent to another
# If you are not in `users`, you will recieve a message 'No one can hear you...'
# Otherwise all your messages are sent to your opponent
#
# Questions:
# 1. Is there any way to improve readability like `content_types=['all']`?
# 2. Is there any way to register this message handler only when i found the opponent?


@bot.message_handler(content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'])
def chatting(message: types.Message):
    if message.chat.id in users:
        bot.copy_message(users[message.chat.id],
                         users[users[message.chat.id]], message.id)
    else:
        bot.send_message(message.chat.id, 'No one can hear you...')


bot.infinity_polling(skip_pending=True)
# {'content_type': 'text', 'id': 15, 'message_id': 15, 'from_user': {'id': 1973842531, 'is_bot': False, 'first_name': 'SA', 'username': 'Iust_math', 'last_name': None, 'language_code': 'en', 'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None},
#  'date': 1637407487, 'chat':
#      {'id': 1973842531, 'type': 'private', 'title': None, 'username': 'Iust_math', 'first_name': 'SA', 'last_name': None, 'photo': None, 'bio': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 'message_auto_delete_time': None, 'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None}, 'sender_chat': None, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_sender_name': None, 'forward_date': None, 'reply_to_message': None, 'via_bot': None, 'edit_date': None, 'media_group_id': None,
#     'author_signature': None, 'text': 'Chvgcg', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'reply_markup': None, 'json': {'message_id': 15, 'from': {'id': 1973842531, 'is_bot': False, 'first_name': 'SA', 'username': 'Iust_math', 'language_code': 'en'}, 'chat': {'id': 1973842531, 'first_name': 'SA', 'username': 'Iust_math', 'type': 'private'}, 'date': 1637407487, 'text': 'Chvgcg'}}
