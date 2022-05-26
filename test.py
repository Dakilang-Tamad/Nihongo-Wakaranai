import sqlite3
from pathlib import Path

conn = sqlite3.connect("Quizzes.db")

table = "N5_BOOKMARKS"

conn.execute("CREATE TABLE " + table + " (ID INT PRIMARY KEY, TYPE TEXT, "
                                       "POINTER INT); ")
