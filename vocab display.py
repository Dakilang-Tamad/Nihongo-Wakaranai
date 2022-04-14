import sqlite3

conn = sqlite3.connect("Quizzes.db")

cursor = conn.execute("SELECT id, word, item, c_a, c_b, c_c, c_d, answer, kanji, jp, en from N5_VOCAB")
for row in cursor:
    print("ID = " + str(row[0]))
    print("WORD = " + row[1])
    print("ITEM = " + row[2])
    print("A = " + row[3])
    print("B = " + row[4])
    print("C = " + row[5])
    print("D = " + row[6])
    print("ANSWER = " + row[7])
    print("KANJI = " + row[8])
    print("JP = " + row[9])
    print("EN = " + row[10] + "\n")

conn.close()