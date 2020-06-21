from tabulate import tabulate
import pyperclip
from time import sleep
import os
import json
import getpass
import time

path = os.path.join(os.path.expanduser('~'),"AppData\\Local\\PManager")

def copy_clear_pass(password):
    pyperclip.copy(password)
    print('password is copied to clipboard')
    a = 15
    while a >= 0:
        print(f"password will clear in {a} seconds", end='\r')
        time.sleep(1)
        a -= 1
    pyperclip.copy('')


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_tabluarised(table):
    rowid=[]
    for i in range(1, len(table)+1):
        rowid.append(i)
    print(tabulate(table,
        headers=('Wesite/Account', 'Usename', 'Description', 'LastModified'),
        tablefmt="psql",
        showindex=rowid ))


def password_validate(password):
    SpecialSym = ['$', '@', '#', '%', '&']
    validation = True
    if len(password) < 6:
        print("Password must be atleast 6 Character long")
        validation = False
    elif len(password) > 15:
        print("Password is too long ")
        validation = False
    elif not any(char.isdigit() for char in password):
        print('Password should have at least one numeral')
        validation = False
    elif not any(char in SpecialSym for char in password):
        print('Password should have at least one of the symbols ($,@,#,&)')
        validation = False

    if validation:
        return validation


def setup(enc,db):
    with open(path + '\\setup.key', 'r') as js_file:
        js = json.load(js_file)
        if js['first_setup'] == 'True':
            print("This is your first Time Setup!!")
            password = getpass.getpass(prompt='Password: ')
            password_re = getpass.getpass(prompt="ReType Password: ")
            if password == password_re:
                if password_validate(password):
                    key = enc.get_key(password)
                    for x in range(0, 5):
                        b = f"your password is >> {password} << copy before {5 - x} seconds " + "." * x + "\r"
                        print(b, end='\r')
                        sleep(1)
                    os.system('cls')
                    js['key'] = key.decode()
                    js['first_setup'] = 'False'
                    with open(path + '\\setup.key', 'w') as js_file:
                        json.dump(js, js_file, indent=4)

    if not db.check_table():
        db.create('passwords', website="TEXT", username="TEXT", password="TEXT", description="TEXT",
                  LastModified='TEXT')

def authenticate(password,enc):
    validate = False
    with open(path + '\\setup.key', 'r') as js_file:
        js = json.load(js_file)
        if js['first_setup'] == 'False' and js['key']:
            key = js['key']
            if key == enc.get_key(password).decode():
                validate = True
    if validate:
        return validate


def MakeDirectorySetup():
    try:
        if os.path.isfile(path):
            pass
        else:
            os.mkdir(path)
            print('path created: ' + path)
    except FileExistsError:
        pass
    try:
        if os.path.isfile(path + '\\setup.key'):
            pass
        else:
            jsonfile = {"first_setup": "True", "key": ""}
            js = json.dumps(jsonfile, indent=4)
            with open(os.path.join(os.path.join(path, 'setup.key')), 'w') as file:
                file.write(js)
            print('setup.key file created')

    except Exception as e:
        print(e)
