from datetime import datetime
import requests
from bs4 import BeautifulSoup
import requests
import pandas as pd
import random
import wikipedia
import os
import sqlite3

class Date:
    def __init__(self):
        current_time = datetime.now()
        self.current_time = current_time
        self.day = current_time.day
        self.month  = current_time.month
        self.year = current_time.year
    def get_weekday(self):
        day = datetime.weekday(self.current_time)
        if (day == 6):
           return 'Воскресенье'
        if (day == 0):
           return 'Понедельник'
        if (day == 1):
           return 'Вторник'
        if (day == 2):
           return 'Среда'
        if (day == 3):
           return 'Четверг'
        if (day == 4):
           return 'Пятница'
        if (day == 5):
           return 'Суббота'
    def get_month(self):
        month = self.current_time.month
        if (month == 1):
            return 'январь'
        if (month == 2):
            return 'февраль'
        if (month == 3):
            return 'март'
        if (month == 4):
            return 'апрель'
        if (month == 5):
            return 'май'
        if (month == 6):
            return 'июнь'
        if (month == 7):
            return 'июль'
        if (month == 8):
            return 'август'
        if (month == 9):
            return 'сентябрь'
        if (month == 10):
            return 'октябрь'
        if (month == 11):
            return 'ноябрь'
        if (month == 12):
            return 'декабрь'
        
def get_info_about_day():
    date = Date()
    find = str(date.day) + ' ' + date.get_month()
    print(find)
    wikipedia.set_lang("ru")
    result = wikipedia.search(find)
    return wikipedia.summary(result[1])

def generate_date_message():
    date = Date()
    message = 'Сегодня: '
    message += str(date.day) + '.' + str(date.month) + '.' + str(date.year)
    message += ',' + date.get_weekday()
    message += '\n' + generate_citate()
    return message

def generate_citate():
    URL_TEMPLATE = "https://lafounder.com/article/motivaciya-citaty"
    response = requests.get(URL_TEMPLATE)
    bs = BeautifulSoup(response.text, "html.parser")
    bs = bs.find('div', {"class": 'field field--name-field-note-before field--type-text-long field--label-hidden field--item'})
    citates = bs.get_text().split('\n') 
    for i in range(len(citates)):
        citates[i] = citates[i].replace(u'\xa0', u' ')
    string = citates[0]
    while (string == ''):
        num = random.randint(10, 100)
        string = citates[num]
    return '🌐' + string


