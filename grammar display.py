import sqlite3

conn = sqlite3.connect("Quizzes.db")

cursor = conn.execute("SELECT id, question, c_a, c_b, c_c, c_d, answer, word, jp, en from N5_GRAMMAR")
for row in cursor:
    print("ID = " + str(row[0]))
    print("QUESTION = " + row[1])
    print("A = " + row[2])
    print("B = " + row[3])
    print("C = " + row[4])
    print("D = " + row[5])
    print("ANSWER = " + row[6])
    print("WORD = " + row[7])
    print("JP = " + row[8])
    print("EN = " + row[9] + "\n")

conn.close()