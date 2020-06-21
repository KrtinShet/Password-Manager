import passwordmanager.database
import passwordmanager.encryption
from passwordmanager.utils import *
# from passwordmanager.utils import copy_clear_pass, clear, print_tabluarised, password_validate, setup, authenticate, MakeDirectorySetup, path, json
import getpass
#====================================================

#===================================================

def ascii():
    print("                                                                              ___      ")
    print(" ____                                     _  __     __          _ _         //  \\\    ")
    print("|  _ \ __ _ ___ _____      _____  _ __ __| | \ \   / /_ _ _   _| | |_      _||__||__   ")
    print("| |_) / _` / __/ __\ \ /\ / / _ \| '__/ _` |  \ \ / / _` | | | | | __|    (_________)  ")
    print("|  __/ (_| \__ \__ \\\ V  V / (_) | | | (_| |   \\ V / (_| | |_| | | |_     |         | ")
    print("|_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|    \_/ \__,_|\__,_|_|\__|    '._______.' ")
    print("                                                                                             ")
    print("                                                                - The Password Manager \n")

def add(key,db,enc):
    key=key
    try:
        in_site = input("Site: ")
        if len(in_site) != 0:
            username = input("Username: ")
            if len(username) != 0:
                password = getpass.getpass(prompt="Site Password: ")
                if len(password) != 0:
                    desc = input("Desc: ")
                    db.insert(site=in_site,
                              userame=username,
                              password=enc.encrypt(password, key=key),
                              desc=desc)
                else:
                    print("Password Cannot be empty, Try the process again !")
                    time.sleep(1)
                    clear()
                    pass
            else:
                print("Username Cannot be empty, Try the process again  !")
                time.sleep(1)
                clear()
                pass
        else:
            print('Provide a valid Website!')
            time.sleep(1)
            clear()
            pass
    except KeyboardInterrupt:
        pass

    clear()

def remove(enc,db):
    try:
        mst_passwd = getpass.getpass(prompt="Master Password: ")
        re_mst_passwd = getpass.getpass(prompt="Confirm Master Password: ")
        if mst_passwd == re_mst_passwd:
            if authenticate(mst_passwd,enc=enc):
                table = db.listAll()
                print_tabluarised(table)
                index = int(input('id(?): ')) - 1
                try:
                    username=table[index][1]
                except IndexError:
                    print('Wrong Input! Select a Proper ID')
                    time.sleep(1)
                try:
                    db.remove(username=username,
                              password=db.get_cred_password(username=username, site=table[index][0]))
                except:
                    print("Try Again!")
                    time.sleep(1)
                    pass
        else:
            print('Password Mismatch !! \n Try Again')
            remove()
    except KeyboardInterrupt:
        pass
    clear()

def UpdateUsername(enc,db):
    try:
        mst_passwd = getpass.getpass(prompt="Master Password: ")
        re_mst_passwd = getpass.getpass(prompt="Confirm Master Password: ")
        if mst_passwd == re_mst_passwd:
            if authenticate(mst_passwd,enc=enc):
                table = db.listAll()
                print_tabluarised(table)
                try:
                    index = int(input('id(?): ')) -1
                    currentusername = table[index][1]
                    try:
                        newusername = input('New Username: ')
                        if len(newusername) != 0:
                            db.update_username(currentusername=currentusername,
                                            newusername=newusername,
                                            currentpassword=db.get_cred_password(username=currentusername, site=table[index][0]))
                            print("Updated Username Sucessfully!!")
                            time.sleep(1)
                        else:
                            print("New Username Cannot be empty!! \nTry Again!")
                            time.sleep(1)
                    except Exception :
                        pass
                except IndexError:
                    print("Try again and Select a valid ID!")
                    time.sleep(1)
                    UpdateUsername()
    except KeyboardInterrupt:
        pass
    clear()

def UpdatePassword(key,enc,db):
    try:
        mst_passwd = getpass.getpass(prompt="Master Password: ")
        re_mst_passwd = getpass.getpass(prompt="Confirm Master Password: ")
        if mst_passwd == re_mst_passwd:
            if authenticate(mst_passwd,enc):
                table = db.listAll()
                print_tabluarised(table)
                try:
                    index = int(input('id(?): ')) -1
                    username = table[index][1]
                    try:
                        newpassword = getpass.getpass('New Password: ')
                        if len(newpassword) !=0 :
                            db.update_password(currentusername=username,
                                               currentpassword=db.get_cred_password(username=username, site=table[index][0]),
                                               newpassword=enc.encrypt(data=newpassword, key=key))
                            print("Updated Password Sucessfully!")
                            time.sleep(1)
                    except Exception:
                        pass
                except IndexError:
                    print("TryAgain and select a valid ID")
                    time.sleep(1)
                    UpdatePassword()

    except KeyboardInterrupt:
        pass
    clear()

def getPasswordFromSelected(key,enc,db):
    try:
        table = db.listAll()
        print_tabluarised(table)
        index = int(input('id(?): ')) -1
        try:
            cypher_password = db.get_cred_password(username=table[index][1], site=table[index][0])
            password = enc.decrypt(cypher_password.encode(), key=key)
            copy_clear_pass(password)
        except IndexError:
            print("select a Proper ID")
            time.sleep(1)
            getPasswordFromSelected(key)
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
    clear()

def run(enc,db):
    try:
        password = getpass.getpass(prompt='Master Password: ')
        if not authenticate(password,enc):
            print("Wrong Password ..! Try again")
            time.sleep(0.5)
            clear()
            exit()

        js_file = open(path + '\\setup.key', 'r')
        js = json.load(js_file)
        key = js['key']
        key = key.encode()
        control = True
        while control:

            cmd = input('(a)dd\\ (r)emove\\ update: username(uu)| password(up)\\ ListAll(l)\\ (g)et credential\\ (e)xit : ')

            if cmd == 'a':
                add(key=key,db=db,enc=enc)

            if cmd == 'r':
                remove(enc=enc,db=db)

            if cmd == 'uu':
                UpdateUsername(enc=enc,db=db)

            if cmd == 'up':
                UpdatePassword(key=key,enc=enc,db=db)

            if cmd == 'l':
                print_tabluarised(table= db.listAll())

            if cmd == 'g':
                getPasswordFromSelected(key=key,enc=enc,db=db)

            if cmd == 'e':
                print('\n\nExiting...!')
                time.sleep(1)
                clear()
                db.save()
                control = False

    except KeyboardInterrupt:
        print('\n\nExiting...!')
        time.sleep(1)
        clear()

def main():
    ascii()
    MakeDirectorySetup()
    db = passwordmanager.database.DataBase()
    enc = passwordmanager.encryption.Encryption()
    setup(enc=enc,db=db)
    run(enc=enc,db=db)

if __name__ == '__main__':
    main()
