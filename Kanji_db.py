import sqlite3
import openpyxl
from pathlib import Path

conn = sqlite3.connect("Quizzes.db")

table = "N5_KANJI"
file = "n5_kanji.xlsx"

conn.execute("CREATE TABLE " + table + " (ID INT PRIMARY KEY, QUESTION TEXT, "
                                       "ITEM TEXT, C_A TEXT, C_B TEXT, C_C TEXT, "
                                       "C_D TEXT, ANSWER TEXT, KANJI TEXT, READING TEXT, "
                                       "KIND TEXT, MEANING TEXT, JP TEXT, EN TEXT, BOOKMARK INT);")

xlsx_file = Path('resources', file)
wb_obj = openpyxl.load_workbook(xlsx_file)

sheet = wb_obj.active

for i in range(1, 26):
    print("\n" + str(i) + "\n")
    question = "A" + str(i)
    item = "B" + str(i)
    c_a = "C" + str(i)
    c_b = "D" + str(i)
    c_c = "E" + str(i)
    c_d = "F" + str(i)
    ans = "G" + str(i)
    kanji = "H" + str(i)
    reading = "I" + str(i)
    kind = "J" + str(i)
    meaning = "K" + str(i)
    jp = "L" + str(i)
    en = "M" + str(i)

    command = "INSERT INTO " + table + "(ID) VALUES (" + str(i) + ")"
    conn.execute(command)

    print(sheet[question].value)
    command = "UPDATE " + table + " set QUESTION = '" + sheet[question].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[item].value)
    command = "UPDATE " + table + " set ITEM = '" + sheet[item].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[c_a].value)
    command = "UPDATE " + table + " set C_A = '" + sheet[c_a].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[c_b].value)
    command = "UPDATE " + table + " set C_B = '" + sheet[c_b].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[c_c].value)
    command = "UPDATE " + table + " set C_C = '" + sheet[c_c].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[c_d].value)
    command = "UPDATE " + table + " set C_D = '" + sheet[c_d].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[ans].value)
    command = "UPDATE " + table + " set ANSWER = '" + sheet[ans].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[kanji].value)
    command = "UPDATE " + table + " set KANJI = '" + sheet[kanji].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[reading].value)
    command = "UPDATE " + table + " set READING = '" + sheet[reading].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[kind].value)
    command = "UPDATE " + table + " set KIND = '" + sheet[kind].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[meaning].value)
    command = "UPDATE " + table + " set MEANING = '" + sheet[meaning].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[jp].value)
    command = "UPDATE " + table + " set JP = '" + sheet[jp].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[en].value)
    command = "UPDATE " + table + " set EN = '" + sheet[en].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(1)
    command = "UPDATE " + table + " set BOOKMARK = 1 where ID = " + str(i)
    conn.execute(command)
    conn.commit()

conn.close()






