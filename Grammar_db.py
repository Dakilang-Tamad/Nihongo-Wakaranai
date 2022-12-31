import sqlite3
import openpyxl
from pathlib import Path

conn = sqlite3.connect("Quizzes.db")

table = "N1_GRAMMAR"
file = "n1_grammar.xlsx"

conn.execute("CREATE TABLE " + table + " (ID INT PRIMARY KEY, QUESTION TEXT, "
                                       "C_A TEXT, C_B TEXT, C_C TEXT, "
                                       "C_D TEXT, ANSWER TEXT, WORD TEXT, MEANING TEXT, "
                                       " JP TEXT, EN TEXT, BOOKMARK INT, PROF INT);")

xlsx_file = Path('resources', file)
wb_obj = openpyxl.load_workbook(xlsx_file)

sheet = wb_obj.active
for i in range(1, 51):
    print("\n" + str(i) + "\n")
    question = "A" + str(i)
    c_a = "B" + str(i)
    c_b = "C" + str(i)
    c_c = "D" + str(i)
    c_d = "E" + str(i)
    word = "F" + str(i)
    meaning = "G" + str(i)
    ans = "H" + str(i)
    jp = "I" + str(i)
    en = "J" + str(i)

    command = "INSERT INTO " + table + "(ID) VALUES (" + str(i) + ")"
    conn.execute(command)

    print(sheet[question].value)
    command = "UPDATE " + table + " set QUESTION = '" + sheet[question].value + "' where ID = " + str(i)
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
    print(sheet[word].value)
    command = "UPDATE " + table + " set WORD = '" + sheet[word].value + "' where ID = " + str(i)
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
    command = "UPDATE " + table + " set PROF = 0 where ID = " + str(i)
    conn.execute(command)
    conn.commit()
