import pg8000
import sqlite3
import json

tname = "t14412888b7ddc5f7ab07p"
with open('creds.json') as f:
    credentials = json.load(f)

pgconn = pg8000.connect(
user=credentials['user'], 
password=credentials['password'], 
host=credentials['host'], 
port=5432, 
database=credentials['dbname'], 
ssl_context=True
)
pgcursor = pgconn.cursor()
conn = sqlite3.connect("Quizzes.db")

pgcursor.execute(" CREATE TABLE " + tname + " ( id SERIAL PRIMARY KEY, source_table TEXT, number INTEGER, proficiency INTEGER );")

command = "INSERT INTO " + tname + " (source_table, number, proficiency) VALUES (%s, %s, %s)"

levels = ["N1", "N2", "N3", "N4", "N5"]
categories = ["GRAMMAR", "VOCAB", "KANJI"]

for i in levels:
    for j in categories:
        source = i + "_" + j
        sqlite_command = "SELECT ID FROM " + source
        cursor = conn.execute(sqlite_command)
        for k in cursor:
            data = (source, k[0], 0)
            pgcursor.execute(command, data)
            print(data)
    
pgconn.commit()
pgconn.close()
