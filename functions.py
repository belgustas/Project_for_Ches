import sqlite3


def new_user(login, password):
    connection = sqlite3.connect("password_users.db")
    cursor = connection.cursor()
    all_users = cursor.execute("""SELECT * FROM Users""").fetchall()
    check_login = True
    for elem in all_users:
        if elem[1] == login:
            check_login = False
            break
    if check_login:
        cursor.execute("""INSERT INTO Users(login, password) VALUES(?, ?) """, (login, password)).fetchall()
        connection.commit()
        connection.close()
        return check_login
    else:
        connection.close()
        return check_login


def check_in_db(login, password):
    connection = sqlite3.connect("password_users.db")
    cursor = connection.cursor()
    user = cursor.execute("""SELECT login FROM Users WHERE login = ? AND password = ?""", (login, password)).fetchall()
    flag = False
    if len(user) == 1:
        flag = True
    return flag
