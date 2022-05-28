import sqlite3
import random
from pathlib import Path


def new_quiz():
    v = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    k = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    g = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,
         26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
    quiz = []
    for i in range(10):
        if i in (0, 3, 6, 9):
            quiz.append(g.pop(random.randrange(len(g))))
        if i in (1, 4, 7):
            quiz.append(v.pop(random.randrange(len(v))))
        if i in (2, 5, 8):
            quiz.append(k.pop(random.randrange(len(k))))

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


bg = '#fffbe6'
current = 0 #counter for the array
current_id = 0 #holder for the current ID value of a question/entry being processed
score = 0 #holder of the quiz score
tally = [] #a tally of which items were answered correctly
contents = [] #contains the contents (ID's) of the quiz
level = "N5" #current difficulty level selected