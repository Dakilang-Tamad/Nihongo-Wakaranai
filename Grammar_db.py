import sqlite3
import openpyxl
from pathlib import Path

conn = sqlite3.connect("Quizzes.db")

table = "N5_GRAMMAR"
file = "n5_grammar.xlsx"

conn.execute("CREATE TABLE " + table + " (ID INT PRIMARY KEY, QUESTION TEXT, "
                                       "C_A TEXT, C_B TEXT, C_C TEXT, "
                                       "C_D TEXT, ANSWER TEXT, WORD TEXT, "
                                       " JP TEXT, EN TEXT);")

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
    ans = "G" + str(i)
    jp = "H" + str(i)
    en = "I" + str(i)

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
    print(sheet[jp].value)
    command = "UPDATE " + table + " set JP = '" + sheet[jp].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
    print(sheet[en].value)
    command = "UPDATE " + table + " set EN = '" + sheet[en].value + "' where ID = " + str(i)
    conn.execute(command)
    conn.commit()
