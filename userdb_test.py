import psycopg2
import sqlite3
import hashlib

host = "nihongowakaranai.postgres.database.azure.com"
dbname = "Nihongo_Wakaranai"
user = "main_admin"
password = "Knxvn_0407"
sslmode = "require"

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn1 = psycopg2.connect(conn_string)
conn2 = sqlite3.connect("Quizzes.db")
print("Connection established")

cursor1 = conn1.cursor()

uname = "yes"
sample_pass = "yes"
obj = hashlib.sha256(sample_pass.encode())
hashed = obj.hexdigest()
tname = "u" + hashed[0:10] + "u"
print(hashed)
print(tname)

command = "INSERT INTO user_data(username, password, table_name) VALUES (%s, %s, %s);"
cursor1.execute(command, (uname, hashed, tname))
conn1.commit()


levels = ["N1", "N2", "N3", "N4", "N5"]
categories = ["GRAMMAR", "VOCAB", "KANJI"]


cursor1.execute("DROP TABLE IF EXISTS " + tname + ";")
print("Finished dropping table (if existed)")

cursor1.execute("CREATE TABLE " + tname + " (source_table TEXT, number INTEGER, proficiency INTEGER);")
print("Finished creating table")

#for i in levels:
#    for j in categories:
#        source = i + "_" + j
#        sqlite_command = "SELECT ID FROM " + source
#        cursor2 = conn2.execute(sqlite_command)
#        for k in cursor2:
#            insert_command = "INSERT INTO " + tname + " (source_table, number, proficiency) VALUES (%s, %s, %s);"
#            cursor1.execute(insert_command, (source, k[0], 0))
#            print(k[0])

cursor1.execute("SELECT * from " + tname + ";")
contents = cursor1.fetchall()

for x in contents:
    conn2.execute("UPDATE " + x[0] + " set PROF = " + str(x[2]) + " where ID = " + str(x[1]))
    print("UPDATE " + x[0] + " set PROF = " + str(x[2]) + " where ID = " + str(x[1]))

conn2.commit()

conn1.commit()
cursor1.close()
conn1.close()
