import psycopg2

host = "nihongowakaranai.postgres.database.azure.com"
dbname = "Nihongo_Wakaranai"
user = "app_access"
password = "app_access"
sslmode = "require"

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS username;")
print("Finished dropping table (if existed)")

cursor.execute("CREATE TABLE username (level TEXT, category TEXT, number INTEGER, proficiency INTEGER);")
print("Finished creating table")

#cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
#cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
#cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
#print("Inserted 3 rows of data")

conn.commit()
cursor.close()
conn.close()
