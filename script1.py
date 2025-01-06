import telebot
import os
from dotenv import load_dotenv, set_key
from telebot import types

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
admin_chat_id = os.getenv('ADMIN_CHAT_ID')
channel_id = '@nalogovayakniga'


@bot.message_handler(commands=['start'])


def first(message):

    user_id = message.from_user.id
    chat_member = bot.get_chat_member(channel_id, user_id)
    if chat_member.status in ['member', 'administrator', 'creator']:
        start(message, True)
    else:
        bot.reply_to(message, "Вы не подписаны на канал @nalogovayakniga. Пожалуйста, подпишитесь, чтобы продолжить. После подписки нажмите /start")

    # except Exception as e:
    #     bot.reply_to(message, "Произошла ошибка при проверке подписки на канал.")

def start(message, flag = True):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Социальные сети канала')
    btn2 = types.KeyboardButton('Создать заявку')
    btn3 = types.KeyboardButton('Обратная связь')
    markup.row(btn2)
    markup.row(btn1, btn3)
    if flag:
        bot.send_message(message.chat.id, 'Здравствуйте, выберите услугу:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Выберите услугу:', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Обратная связь':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Назад')
        markup.row(btn1)
        bot.send_message(message.chat.id, 'Здесь вы можете оставить ваши пожелания по развитию:', reply_markup=markup)
        bot.register_next_step_handler(message, feedback)
    elif message.text == 'Социальные сети канала':
        # bot.send_message(message.chat.id, f'')
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Назад')
        markup.row(btn1)
        mark = types.InlineKeyboardMarkup()

        bot.send_message(message.chat.id, 'Социальные сети:', reply_markup=markup)
        bot.register_next_step_handler(message, media)
    elif message.text == 'Создать заявку':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Договор')
        btn2 = types.KeyboardButton('Консультация')
        btn3 = types.KeyboardButton('Другое')
        btn4 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2, btn3)
        markup.row(btn4)
        bot.send_message(message.chat.id, 'Что вы хотите получить?', reply_markup=markup)
        bot.register_next_step_handler(message, service)
    else:
        start(message, False)

def media(message):
    if message.text == 'Назад':
        on_click(message)
    else:
        start(message, False)

def feedback(message):
    if message.text == 'Назад':
        on_click(message)
    else:
        bot.forward_message(admin_chat_id, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Мы рассмотрим ваше предложение, спасибо')
        start(message, False)

def service(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Назад')
    markup.row(btn1)
    if message.text == 'Договор':
        bot.send_message(message.chat.id, 'Кратко расскажите что вам требуется:', reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: bid(msg, 1))
    elif message.text == 'Консультация':
        bot.send_message(message.chat.id, 'Кратко расскажите что вам требуется:', reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: bid(msg, 2))
    elif message.text == 'Другое':
        bot.send_message(message.chat.id, 'Кратко расскажите что вам требуется:', reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: bid(msg, 3))
    else:
        on_click(message)

def bid(message, type):
    if message.text == 'Назад':
        on_click(message)
    else:
        load_dotenv()
        id = int(os.getenv('BID_ID'))
        if type == 1:
            id += 1
            bot.send_message(admin_chat_id, f'Тип заявки: Договор, id заявки {id}')
            set_key('.env', 'BID_ID', str(id))
            load_dotenv()
            bot.forward_message(admin_chat_id, message.chat.id, message.message_id)
            bot.send_message(message.chat.id, 'Ваша заявка создана, в течении одного рабочего дня вам напишут, '
                                              'чтобы обговорить условия выполнения')
        if type == 2:
            id += 1
            bot.send_message(admin_chat_id, f'Тип заявки: Консультация, id заявки {id}')
            set_key('.env', 'BID_ID', str(id))
            load_dotenv()
            bot.forward_message(admin_chat_id, message.chat.id, message.message_id)
            bot.send_message(message.chat.id, 'Ваша заявка создана, в течении одного рабочего дня вам напишут, '
                                              'чтобы обговорить условия выполнения')
        if type == 3:
            id += 1
            bot.send_message(admin_chat_id, f'Тип заявки: Другое, id заявки {id}')
            set_key('.env', 'BID_ID', str(id))
            load_dotenv()
            bot.forward_message(admin_chat_id, message.chat.id, message.message_id)
            bot.send_message(message.chat.id, 'Ваша заявка создана, в течении одного рабочего дня вам напишут, '
                                              'чтобы обговорить условия выполнения')
        bot.send_message(message.chat.id, 'Чтобы вернуться в начало введите /start')

bot.infinity_polling()