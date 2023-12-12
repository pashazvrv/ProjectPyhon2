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
        d = {}
        d[6] = 'Воскресенье'
        d[0] = 'Понедельник'
        d[1] = 'Вторник'
        d[2] = 'Среда'
        d[3] = 'Четверг'
        d[4] = 'Пятница'
        d[5] = 'Суббота'
        return d[day]
    def get_month(self):
        d = {}
        month = self.current_time.month
        d[1] = 'январь'
        d[2] = 'февраль'
        d[3] = 'март'
        d[4] = 'апрель'
        d[5] = 'май'
        d[6] = 'июнь'
        d[7] = 'июль'
        d[8] = 'август'
        d[9] = 'сентябрь'
        d[10] = 'октябрь'
        d[11] = 'ноябрь'
        d[12] = 'декабрь'
        return d[month]
        
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


