import sqlite3

conn = sqlite3.connect("Quizzes.db")

cursor = conn.execute("SELECT username FROM USER")

for i in cursor:
    print(i[0])