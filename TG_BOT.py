import telebot
import datetime
import tools
from datetime import datetime
import Calendar
from telebot import types # для указание типов
import config
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

date = 0

bot = telebot.TeleBot(os.getenv('s'))

@bot.message_handler(commands=['date'])
def date(m, res = False):
    bot.send_message(m.chat.id, tools.generate_date_message())

@bot.message_handler(commands=['citate'])
def citate(m, res = False):
    bot.send_message(m.chat.id, tools.generate_citate())
    
@bot.message_handler(commands=['info'])
def info(m, res = False):
    bot.send_message(m.chat.id, tools.get_info_about_day())

@bot.message_handler(content_types=["text"])
def handle_text(message):
    editor = Calendar.TimetableEditor(bot)
    if message.text == '/open_day':
        bot.send_message(message.from_user.id,'⤵️Введите день, который хотите посмотреть: \n Формат: dd.mm.yyyy')
        bot.register_next_step_handler(message, editor.read_day)
    elif message.text == '/add_point':
        bot.send_message(message.from_user.id,'⤵️Введите день, который хотите редактировать: \n Формат: dd.mm.yyyy')
        bot.register_next_step_handler(message, editor.add_point)
    elif message.text == '/fact':
        bot.send_message(message.from_user.id,tools.get_info_about_day()) 
    elif message.text == '/remove_point': 
        bot.send_message(message.from_user.id,'⤵️Введите день, который хотите редактировать: \n Формат: dd.mm.yyyy')
        bot.register_next_step_handler(message, editor.remove_point)
    elif message.text == '/help' or message.text == '/start':
        s = '🤖Данный бот - ежедневник возволяет вам посмотреть, какой сегодня день, узнать интерсный факт про сегодняшний день, создать и удалять заметки на каждый день'
        s += '\n➡️Чтобы узнать какое сегодня число и прочитать мудрую цитату дня введите команду /date\n'
        s += '➡️Интересный факт про этот день можно узнать, нажав на /fact\n'
        s += '➡️Чтобы создать новую заметку или добавить что-то в существующую выберите /add_point, затем следуйте инструкциям\n'
        s += '➡️Для просмотра своих заметок выберите /open_day\n'
        s += '➡️Чтобы удалить какой то пункт из заметки нажмите на /remove_point'
        bot.send_message(message.from_user.id,s)
    else:
        bot.send_message(message.from_user.id, 'Извините, я не понимаю( \n Пожалуйста введите команду из меню' )

bot.polling(none_stop = True, interval = 0)
