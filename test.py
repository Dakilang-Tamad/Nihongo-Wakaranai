import string
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


word = "user,name"
list = [*word]
check = string.ascii_letters + string.digits + "_" + "@" + "."
whitelist = [*check]


for i in list:
    if i in whitelist:
        pass
    else:
        print("error")


def new_table(tablename):
    tname = tablename
    host = "nihongowakaranai.postgres.database.azure.com"
    dbname = "Nihongo_Wakaranai"
    user = "main_admin"
    port = "5432"
    password = "Knxvn_0407"
    sslmode = "require"

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode={sslmode}')
    Base = declarative_base()
    metadata = MetaData()

    levels = ["N1", "N2", "N3", "N4", "N5"]
    categories = ["GRAMMAR", "VOCAB", "KANJI"]


    cursor1.execute("DROP TABLE IF EXISTS " + tname + ";")

    cursor1.execute("CREATE TABLE " + tname + " (source_table TEXT, number INTEGER, proficiency INTEGER);")

    c_notif = notification.notify(
        title='My Title',
        message='My message',
        app_name='My App'
    )

    for i in levels:
        for j in categories:
            source = i + "_" + j
            sqlite_command = "SELECT ID FROM " + source
            cursor2 = conn2.execute(sqlite_command)
            for k in cursor2:
                insert_command = "INSERT INTO " + tname + " (source_table, number, proficiency) VALUES (%s, %s, %s);"
                cursor1.execute(insert_command, (source, k[0], 0))

                text = source + " " + str(k[0])

                notification.update(
                    notification_id = c_notif,
                    message = text
                )
    
    conn1.commit()
    conn1.close()