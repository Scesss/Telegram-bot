import telebot
import os
from dotenv import load_dotenv
from telebot import types


bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
admin_chat_id = os.getenv('ADMIN_CHAT_ID')

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')

    # markup = types. ReplyKeyboardMarkup()
    # btn1 = types. KeyboardButton ('Лекейти на сайт', url= 'https://g00/glp.com')
    # markup. row(btn1)
    # btn2 = types. KeyboardButton ('Удалить фото', callback_data='delete')
    # btn3 = types. KeyboardButton ("Изменить лекст', callback_data='edit')


bot.infinity_polling()