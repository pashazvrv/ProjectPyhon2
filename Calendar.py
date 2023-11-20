import tools
import sqlite3
from fnmatch import fnmatch
bot = 0
class TimetableEditor:
    def __init__(self, bot1):
        global bot
        bot = bot1
        
    def read_day(self, message):
        timetable = Database(message.from_user.id)
        global date
        date = message.text
        bot.send_message(message.from_user.id,'▶️Планы на данный день:\n' + timetable.get_timetable(date))
        
    def add_point(self, message):
        timetable = Database(message.from_user.id)
        global date
        date = message.text
        bot.send_message(message.from_user.id,'▶️Текущие планы на эту дату:\n' + timetable.get_timetable(date))
        bot.send_message(message.from_user.id,'Напишите что нужно добавить: (для выхода напишите -)')
        bot.register_next_step_handler(message, add_point_helper)
        
    def remove_point(self, message):
        global date
        date = message.text
        timetable = Database(message.from_user.id)
        bot.send_message(message.from_user.id,'▶️Текущие планы на эту дату:\n' + timetable.get_timetable(date))
        bot.send_message(message.from_user.id,'Что хотите удалить? (введите номер, для выхода напишите -)')
        bot.register_next_step_handler(message, remove_point_helper)
        
def remove_point_helper(message):
    timetable = Database(message.from_user.id)
    point = message.text
    if (point == '/help' or point == '/date' or point == '/fact' or point == '/add_point' or point == '/open_day' or point == '/remove_point' or point == '/start'):
        bot.send_message(message.from_user.id,'⛔️Ошибка, введите команду еще раз:')
    elif (point != '-'):
        last_point = timetable.get_point(date, point)
        timetable.remove_from_timetable(date, int(point))
        bot.send_message(message.from_user.id,last_point + ' - Удалено☑️')
        bot.register_next_step_handler(message, remove_point_helper)
    else:
        bot.send_message(message.from_user.id,'Все изменения сохранены☑️')

def add_point_helper(message):
    timetable = Database(message.from_user.id)
    point = message.text
    if (point == '/help' or point == '/date' or point == '/fact' or point == '/add_point' or point == '/open_day' or point == '/remove_point' or point == '/start'):
        bot.send_message(message.from_user.id,'⛔️Ошибка, введите команду еще раз:')    
    elif (point != '-'):
        timetable.add_in_timetable(date, point)
        bot.send_message(message.from_user.id,point + ' - Добавлено☑️')
        bot.register_next_step_handler(message, add_point_helper)
    elif (point == '-'):
        bot.send_message(message.from_user.id,'Все изменения сохранены☑️')

class Database:
    def __init__(self, name):
        self.conn = sqlite3.connect(str(name) + ".db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            points TEXT NOT NULL
        )
        """)
        
    def get_timetable(self, date):
        self.cursor.execute("SELECT * FROM timetable WHERE date = ?", (date,))
        rows = self.cursor.fetchall()
        s = ''
        count = 1
        if len(rows) > 0 and rows[0][2].replace('||', '') != '':
            for i in rows[0][2].split('||'):
                s+='\n' + str(count) + '. ' + i + ' '
                count += 1
            return s
        else:
            return 'планов на день нет'
        
    def get_point(self, date, point):
        self.cursor.execute("SELECT * FROM timetable WHERE date = ?", (date,))
        rows = self.cursor.fetchall()
        s = ''
        count = 1
        for i in rows[0][2].split('||')[1:]:
            if (count == point):
                s = i
                break
            count += 1
        return s
        
    def add_in_timetable(self, date, new_point):
        self.cursor.execute("SELECT * FROM timetable WHERE date = ?", (date,))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            self.cursor.execute("INSERT INTO timetable (date, points) VALUES (?, ?)", (date, new_point))
            self.conn.commit()
            return
        else:
            self.cursor.execute("UPDATE timetable SET points = ? WHERE date = ?", (rows[0][2] + new_point + '||', date))
            self.conn.commit()
    def remove_from_timetable(self, date, point):
        self.cursor.execute("SELECT * FROM timetable WHERE date = ?", (date,))
        rows = self.cursor.fetchall()
        if len(rows) == 0:
            return 'на этот день у вас нет никаких планов'
        else:
            s = ''
            count = 1
            for i in rows[0][2].split():
                if (count != point):
                    s += i + '||'
                count+=1
            self.cursor.execute("UPDATE timetable SET points = ? WHERE date = ?", (s, date))
            self.conn.commit()
