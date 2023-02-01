import sqlite3
import random
import psycopg2
import sqlite3
import hashlib
import string
import re
from threading import Thread
from plyer import notification
from pathlib import Path

def new_table(tablename):
    tname = tablename
    host = "nihongowakaranai.postgres.database.azure.com"
    dbname = "Nihongo_Wakaranai"
    user = "main_admin"
    password = "Knxvn_0407"
    sslmode = "require"

    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn1 = psycopg2.connect(conn_string)
    conn2 = sqlite3.connect("Quizzes.db")

    cursor1 = conn1.cursor()

    levels = ["N1", "N2", "N3", "N4", "N5"]
    categories = ["GRAMMAR", "VOCAB", "KANJI"]


    cursor1.execute("DROP TABLE IF EXISTS " + tname + ";")

    cursor1.execute("CREATE TABLE " + tname + " (source_table TEXT, number INTEGER, proficiency INTEGER);")

    c_notif = notification.notify(
        title='My Title',
        message='My message',
        app_name='My App'
    )

    for i in levels:
        for j in categories:
            source = i + "_" + j
            sqlite_command = "SELECT ID FROM " + source
            cursor2 = conn2.execute(sqlite_command)
            for k in cursor2:
                insert_command = "INSERT INTO " + tname + " (source_table, number, proficiency) VALUES (%s, %s, %s);"
                cursor1.execute(insert_command, (source, k[0], 0))

                text = source + " " + str(k[0])

                notification.update(
                    notification_id = c_notif,
                    message = text
                )
    
    conn1.commit()
    conn1.close()

def signup(username, password):
    host = "nihongowakaranai.postgres.database.azure.com"
    dbname = "Nihongo_Wakaranai"
    user = "main_admin"
    password = "Knxvn_0407"
    sslmode = "require"

    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn1 = psycopg2.connect(conn_string)
    conn2 = sqlite3.connect("Quizzes.db")

    cursor1 = conn1.cursor()

    uname = username
    sample_pass = password
    obj = hashlib.sha256(sample_pass.encode())
    hashed = obj.hexdigest()
    tname = "t" + hashed[0:20] + "p"

    command = "INSERT INTO user_data(username, password, table_name) VALUES (%s, %s, %s);"
    cursor1.execute(command, (uname, hashed, tname))
    conn1.commit()

    print("account created, setting up account")
    
    conn1.commit()
    conn1.close()

    new_table(tname)

def validate(username, password):
    match=string.ascii_letters + string.digits + '_' + '.' + '@'
    if not all([x in match for x in username]):
        return False
    if not (len(username) >=4 and len(username) <=15):
        return False
    if not username[0].isalpha():
        return False
    if username[-1:] == '_':
        return False
    while True:
        if (len(password)<=8):
            return False
        elif not re.search("[a-z]", password):
            return False
        elif not re.search("[A-Z]", password):
            return False
        elif not re.search("[0-9]", password):
            return False
        elif not re.search("[_@$]" , password):
            return False
        elif re.search("\s" , password):
            return False
        else:
            return True


def new_quiz(diff):
    conn = sqlite3.connect("Quizzes.db")
    cursor1 = conn.execute("SELECT ID FROM " + diff + "_VOCAB WHERE PROF < 5;")
    cursor2 = conn.execute("SELECT ID FROM " + diff + "_KANJI WHERE PROF < 5;")
    cursor3 = conn.execute("SELECT ID FROM " + diff + "_GRAMMAR WHERE PROF < 5;")
    v = []
    k = []
    g = []
    for i in cursor1:
        v.append(i[0])
    for i in cursor2:
        k.append(i[0])
    for i in cursor3:
        g.append(i[0])

    quiz = []
    for i in range(10):
        if i in (0, 3, 6, 9):
            quiz.append(g.pop(random.randrange(len(g))))
        if i in (1, 4, 7):
            quiz.append(v.pop(random.randrange(len(v))))
        if i in (2, 5, 8):
            quiz.append(k.pop(random.randrange(len(k))))
    conn.close()
    return quiz

def add_bm(level, type, ID):
    conn = sqlite3.connect("Quizzes.db")
    table = level + "_BOOKMARKS"
    total = len(conn.execute("SELECT * FROM " + table + ";").fetchall())
    current_id = str(total + 1)
    command = "INSERT INTO " + table + "(ID) VALUES (" + current_id + ")"
    conn.execute(command)
    command = "UPDATE " + table + " set TYPE = '" + type + "' where ID = " + current_id
    conn.execute(command)
    command = "UPDATE " + table + " set POINTER = '" + str(ID) + "' where ID = " + current_id
    conn.execute(command)
    conn.commit()

def check_user():
    conn = sqlite3.connect("Quizzes.db")
    cursor = conn.cursor()
    t_list = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'
                            AND name='user'; """).fetchall()
    if t_list == []: return False
    else: return True


bg = '#fffbe6'
current = 0 #counter for the array
current_id = 0 #holder for the current ID value of a question/entry being processed
score = 0 #holder of the quiz score
tally = [] #a tally of which items were answered correctly
contents = [] #contains the contents (ID's) of the quiz
level = "" #current difficulty level selected
tts = "" #current text-to-speech container