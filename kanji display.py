import sqlite3

conn = sqlite3.connect("Quizzes.db")

cursor = conn.execute("SELECT id, question, item, c_a, c_b, c_c, c_d, answer, kanji, kind, meaning, jp, en from N3_KANJI")
for row in cursor:
    print("ID = " + str(row[0]))
    print("QUESTION = " + row[1])
    print("ITEM = " + row[2])
    print("A = " + row[3])
    print("B = " + row[4])
    print("C = " + row[5])
    print("D = " + row[6])
    print("ANSWER = " + row[7])
    print("KANJI = " + row[8])
    print("KIND = " + row[9])
    print("MEANING = " + row[10])
    print("JP = " + row[11])
    print("EN = " + row[12] + "\n")

conn.close()