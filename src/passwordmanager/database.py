import sqlite3
from datetime import datetime
from .utils import path


class DataBase:

    def __init__(self):
        self.conn = sqlite3.connect(path+"\\DataBase.db")
        self.c = self.conn.cursor()

    def check_table(self):
        self.c.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
        try:
            table = self.c.fetchone()[0]
        except TypeError:
            table = None

        if table:
            return table
        else:
            return False

    def get_cred_password(self, username='', site=''):
        a = self.c.execute(
            f'''SELECT password FROM {self.check_table()} WHERE username = {username!r} AND website = {site!r}''')
        passwd = a.fetchone()[0]
        return passwd

    def create(self, tablename, **kwargs):
        itemString = ''
        for item in kwargs.items():
            string = f' {item[0]} {item[1]}'
            itemString += ',' + string

        itemString = itemString[1:]
        command = f'''CREATE TABLE {tablename} ({itemString}) '''
        self.c.execute(command)

    def insert(self, site, userame, password, desc):
        self.c.execute(
            f''' INSERT INTO {self.check_table()} VALUES ({site!r}, {userame!r}, {password!r}, {desc!r}, {str(datetime.now())!r}) ''')
        self.conn.commit()

    def remove(self, username='', password=''):
        self.c.execute(
            f'''DELETE FROM {self.check_table()} WHERE username = {username!r} AND password = {password!r}''')
        self.conn.commit()

    def update_username(self, currentusername='', newusername='', currentpassword=''):
        if currentusername != '' and newusername != '' and currentpassword != '':
            self.c.execute(
                f'''UPDATE {self.check_table()} SET username = {newusername!r}, LastModified = {str(datetime.now())!r} WHERE username = {currentusername!r} AND password = {currentpassword!r}''')
        else:
            print('Incomplete Input')
        self.conn.commit()

    def update_password(self, currentusername='', currentpassword='', newpassword=''):
        if currentpassword != '' and newpassword != '' and currentusername != '':
            self.c.execute(
                f'''UPDATE {self.check_table()} SET password = {newpassword!r}, LastModified = {str(datetime.now())!r} WHERE username = {currentusername!r} AND
                    password = {currentpassword!r}''')
        else:
            print("wrong credentials")
        self.conn.commit()

    def listAll(self):
        a = self.c.execute(f'select website, username, description, LastModified from {self.check_table()}').fetchall()
        return a

    def save(self):
        self.conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()
