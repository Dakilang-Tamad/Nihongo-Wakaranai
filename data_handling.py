import sqlite3
import random
from pathlib import Path


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
    if t_list == []: return True
    else: return True


bg = '#fffbe6'
current = 0 #counter for the array
current_id = 0 #holder for the current ID value of a question/entry being processed
score = 0 #holder of the quiz score
tally = [] #a tally of which items were answered correctly
contents = [] #contains the contents (ID's) of the quiz
level = "" #current difficulty level selected
tts = "" #current text-to-speech container