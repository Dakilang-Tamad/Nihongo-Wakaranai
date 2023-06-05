import sqlite3
import random
import hashlib
import string
import re
import json
from threading import Thread
from pathlib import Path
import pg8000
import ssl


def get_user():
    conn = sqlite3.connect("Quizzes.db")
    data = []

    cursor = conn.execute("SELECT username FROM USER")

    for i in cursor:
        data.append(i[0])

    levels = ["N1", "N2", "N3", "N4", "N5"]
    categories = ["GRAMMAR", "VOCAB", "KANJI"]

    for i in levels:
        progress = 0
        for j in categories:
            source = i + "_" + j
            sqlite_command = "SELECT PROF FROM " + source
            cursor = conn.execute(sqlite_command)
            for k in cursor:
                progress = progress + k[0]
        data.append(str(progress))

    return data


def check_duplicate(username):
    with open('creds.json') as f:
        credentials = json.load(f)

    context = ssl.create_default_context(
        cafile='resources/cert/DigiCertGlobalRootCA.crt.pem')
    context.check_hostname = True

    pgconn = pg8000.connect(
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        port=5432,
        database=credentials['dbname'],
        ssl_context=context
    )
    pgcursor = pgconn.cursor()

    pgcursor.execute("SELECT username FROM user_data")
    results = pgcursor.fetchall()

    usernames = []

    for i in results:
        usernames.append(i[0])

    if username in usernames:
        return False
    else:
        return True


def update_progress():
    with open('creds.json') as f:
        credentials = json.load(f)

    context = ssl.create_default_context(
        cafile='resources/cert/DigiCertGlobalRootCA.crt.pem')
    context.check_hostname = True

    pgconn = pg8000.connect(
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        port=5432,
        database=credentials['dbname'],
        ssl_context=context
    )
    pgcursor = pgconn.cursor()

    conn = sqlite3.connect("Quizzes.db")
    cursor = conn.execute("SELECT table_name FROM USER")

    for i in cursor:
        tname = i[0]

    levels = ["N1", "N2", "N3", "N4", "N5"]
    categories = ["GRAMMAR", "VOCAB", "KANJI"]

    command = "UPDATE " + tname + \
        " SET proficiency = %s WHERE source_table = %s AND number = %s"

    for i in levels:
        for j in categories:
            source = i + "_" + j
            sqlite_command = "SELECT ID, PROF FROM " + source
            cursor = conn.execute(sqlite_command)
            for k in cursor:
                data = (k[1], source, k[0])
                pgcursor.execute(command, data)

    pgconn.commit()
    pgconn.close()
    
    global error
    error = 14


def new_table(tablename):
    tname = tablename
    with open('creds.json') as f:
        credentials = json.load(f)

    context = ssl.create_default_context(
        cafile='resources/cert/DigiCertGlobalRootCA.crt.pem')
    context.check_hostname = True

    pgconn = pg8000.connect(
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        port=5432,
        database=credentials['dbname'],
        ssl_context=context
    )
    pgcursor = pgconn.cursor()
    conn = sqlite3.connect("Quizzes.db")

    pgcursor.execute(" CREATE TABLE " + tname +
                     " ( id SERIAL PRIMARY KEY, source_table TEXT, number INTEGER, proficiency INTEGER );")
    
    pgconn.commit()

    command = "INSERT INTO " + tname + \
        " (source_table, number, proficiency) VALUES (%s, %s, %s)"

    levels = ["N1", "N2", "N3", "N4", "N5"]
    categories = ["GRAMMAR", "VOCAB", "KANJI"]

    for i in levels:
        for j in categories:
            source = i + "_" + j
            sqlite_command = "SELECT ID FROM " + source
            cursor = conn.execute(sqlite_command)
            for k in cursor:
                data = (source, k[0], 0)
                pgcursor.execute(command, data)

    pgconn.commit()
    pgconn.close()


def create_user(username, table_name):
    conn = sqlite3.connect("Quizzes.db")
    conn.execute(
        "create table USER (ID int primary key, username text, table_name text);")
    conn.execute("insert into USER(ID) values (0);")
    conn.execute("update USER set username = '" + username + "' where ID = 0")
    conn.execute("update USER set table_name = '" +
                 table_name + "' where ID = 0")
    conn.commit()
    conn.close()


def retrieve_progress(table_name):
    tname = table_name
    with open('creds.json') as f:
        credentials = json.load(f)

    context = ssl.create_default_context(
        cafile='resources/cert/DigiCertGlobalRootCA.crt.pem')
    context.check_hostname = True

    pgconn = pg8000.connect(
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        port=5432,
        database=credentials['dbname'],
        ssl_context=context
    )
    pgcursor = pgconn.cursor()
    conn = sqlite3.connect("Quizzes.db")
    pgcursor.execute("SELECT * FROM " + tname)
    results = pgcursor.fetchall()

    for row in results:
        conn.execute("UPDATE " + row[1] + " set PROF = '" +
                     str(row[3]) + "' where ID = " + str(row[2]))
    conn.commit()
    conn.close()
    pgconn.close()


def log_in(username, password):
    with open('creds.json') as f:
        credentials = json.load(f)

    context = ssl.create_default_context(
        cafile='resources/cert/DigiCertGlobalRootCA.crt.pem')
    context.check_hostname = True

    pgconn = pg8000.connect(
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        port=5432,
        database=credentials['dbname'],
        ssl_context=context
    )

    cursor = pgconn.cursor()

    sample_pass = password
    obj = hashlib.sha256(sample_pass.encode())
    hashed = obj.hexdigest()

    cursor.execute(
        "SELECT table_name FROM user_data WHERE username=%s AND password=%s", (username, hashed))
    result = cursor.fetchone()

    pgconn.close()

    return str(result[0]) if result else None


def signup(username, password):

    with open('creds.json') as f:
        credentials = json.load(f)

    context = ssl.create_default_context(
        cafile='resources/cert/DigiCertGlobalRootCA.crt.pem')
    context.check_hostname = True

    conn = pg8000.connect(
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        port=5432,
        database=credentials['dbname'],
        ssl_context=context
    )

    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS user_data (key SERIAL PRIMARY KEY, username TEXT, password TEXT, table_name TEXT)')

    uname = username
    sample_pass = password
    obj = hashlib.sha256(sample_pass.encode())
    hashed = obj.hexdigest()
    tname = "t" + hashed[0:20] + "p"

    cursor.execute(
        'INSERT INTO user_data (username, password, table_name) VALUES (%s, %s, %s)', (uname, hashed, tname))
    conn.commit()

    create_user(uname, tname)


def validate(username, password):
    match = string.ascii_letters + string.digits + '_' + '.' + '@'
    if not all([x in match for x in username]):
        return False
    if not (len(username) >= 4 and len(username) <= 15):
        return False
    if not username[0].isalpha():
        return False
    if username[-1:] == '_':
        return False
    while True:
        if (len(password) <= 8):
            return False
        elif not re.search("[a-z]", password):
            return False
        elif not re.search("[A-Z]", password):
            return False
        elif not re.search("[0-9]", password):
            return False
        elif not re.search("[_@$]", password):
            return False
        elif re.search("\s", password):
            return False
        else:
            return True


def new_quiz(diff):
    conn = sqlite3.connect("Quizzes.db")
    cursor1 = conn.execute("SELECT ID FROM " + diff + "_VOCAB WHERE PROF < 5;")
    cursor2 = conn.execute("SELECT ID FROM " + diff + "_KANJI WHERE PROF < 5;")
    cursor3 = conn.execute("SELECT ID FROM " + diff +
                           "_GRAMMAR WHERE PROF < 5;")
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
    command = "UPDATE " + table + " set TYPE = '" + \
        type + "' where ID = " + current_id
    conn.execute(command)
    command = "UPDATE " + table + " set POINTER = '" + \
        str(ID) + "' where ID = " + current_id
    conn.execute(command)
    conn.commit()


def check_user():
    conn = sqlite3.connect("Quizzes.db")
    cursor = conn.cursor()
    t_list = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'
                            AND name='USER'; """).fetchall()
    if t_list == []:
        return False
    else:
        return True


def add_open_level(level):
    conn = sqlite3.connect("Quizzes.db")
    table = "OPEN_LEVELS"
    command = "INSERT INTO " + table + "(level) VALUES ('" + level + "')"
    conn.execute(command)
    conn.commit()


def check_level_access(diff):
    conn = sqlite3.connect("Quizzes.db")

    cursor1 = conn.execute("SELECT PROF FROM " + diff + "_VOCAB;")
    cursor2 = conn.execute("SELECT PROF FROM " + diff + "_KANJI;")
    cursor3 = conn.execute("SELECT PROF FROM " + diff + "_GRAMMAR;")
    cursor4 = conn.execute("SELECT level FROM OPEN_LEVELS;")

    total = 0
    levels = []

    for i in cursor1:
        total += int(i[0])
    for i in cursor2:
        total += int(i[0])
    for i in cursor3:
        total += int(i[0])

    for i in cursor4:
        levels.append(i[0])

    if diff in levels or total >= 80:
        return True
    else:
        return False


bg = '#fffbe6'
current = 0  # counter for the array
current_id = 0  # holder for the current ID value of a question/entry being processed
score = 0  # holder of the quiz score
tally = []  # a tally of which items were answered correctly
contents = []  # contains the contents (ID's) of the quiz
level = ""  # current difficulty level selected
error = 0  # Error message control
tts = ""
tts_sentence = ""

# for the primary assessment
first_screen = ""
difficulties = ["N5", "N4", "N3", "N2", "N1"]
passing_scores = [5, 4, 5, 4, 3]
index = 0
