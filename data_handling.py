import sqlite3
from pathlib import Path

def new_quiz(base):
    conn = sqlite3.connect("Quizzes.db")
    conn.execute("CREATE TABLE CURRENT QUIZ (ID INT PRIMARY KEY, CATEGORY TEXT, ITEM INT);")
    for i in range(3):
        red = int
