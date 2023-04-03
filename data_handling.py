import sqlite3
import random
import hashlib
import string
import re
import json
from threading import Thread
from plyer import notification
from pathlib import Path
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def new_table(tablename):
    tname = tablename
    with open('creds.json') as f:
        credentials = json.load(f)

    conn_string = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}/{credentials['dbname']}?sslmode={credentials['sslmode']}"
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    conn = sqlite3.connect("Quizzes.db")

    Base = declarative_base()

    class Quiz(Base):
        __tablename__ = tname
        
        id = Column(Integer, primary_key=True)
        source_table = Column(String)
        number = Column(Integer)
        proficiency = Column(Integer)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    levels = ["N1", "N2", "N3", "N4", "N5"]
    categories = ["GRAMMAR", "VOCAB", "KANJI"]

    for i in levels:
        for j in categories:
            source = i + "_" + j
            sqlite_command = "SELECT ID FROM " + source
            cursor = conn.execute(sqlite_command)
            for k in cursor:
                quiz = Quiz(source_table=source, number=k[0], proficiency=0)
                session.add(quiz)
    

    session.commit()
    session.close()

def create_user(username, table_name):
    conn = sqlite3.connect("Quizzes.db")
    conn.execute("create table USER (ID int primary key, username text, table_name text);")
    conn.execute("insert into USER(ID) values (0);")
    conn.execute("update USER set username = '" + username + "' where ID = 0")
    conn.execute("update USER set table_name = '" + table_name + "' where ID = 0")
    conn.commit()
    conn.close()

def retrieve_progress(table_name):
    tname = table_name
    with open('creds.json') as f:
        credentials = json.load(f)

    conn_string = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}/{credentials['dbname']}?sslmode={credentials['sslmode']}"
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    conn = sqlite3.connect("Quizzes.db")
    metadata = MetaData()
    metadata.reflect(bind=engine)

    table = Table(tname, metadata, autoload=True, autoload_with=engine)

    results = session.query(table).all()

    for row in results:
        conn.execute("UPDATE " + row[1] + " set PROF = '" + str(row[3]) + "' where ID = " + str(row[2]))
    conn.commit()
    conn.close()

def log_in(username, password):
    with open('creds.json') as f:
        credentials = json.load(f)

    conn_string = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}/{credentials['dbname']}?sslmode={credentials['sslmode']}"
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    Base = declarative_base()

    sample_pass = password
    obj = hashlib.sha256(sample_pass.encode())
    hashed = obj.hexdigest()

    class User(Base):
        __tablename__ = 'user_data'
        key = Column(Integer, primary_key=True)
        username = Column(String)
        password = Column(String)
        table_name = Column(String)

    result = session.query(User.table_name)\
        .filter_by(username=username, password=hashed).scalar()
    
    return (str(result))

def signup(username, password):

    with open('creds.json') as f:
        credentials = json.load(f)

    conn_string = f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}/{credentials['dbname']}?sslmode={credentials['sslmode']}"
    engine = create_engine(conn_string)

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user_data'
        key = Column(Integer, primary_key=True)
        username = Column(String)
        password = Column(String)
        table_name = Column(String)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    uname = username
    sample_pass = password
    obj = hashlib.sha256(sample_pass.encode())
    hashed = obj.hexdigest()
    tname = "t" + hashed[0:20] + "p"

    user = User(username=uname, password=hashed, table_name=tname)
    session.add(user)
    session.commit()

    create_user(uname, tname)

    new_table(tname)

def validate(username, password):
    match=string.ascii_letters + string.digits + '_' + '.' + '@'
    if not all([x in match for x in username]):
        return False
    if not (len(username) >=4 and len(username) <=15):
        return False
    if not username[0].isalpha():
        return False
    if username[-1:] == '_':
        return False
    while True:
        if (len(password)<=8):
            return False
        elif not re.search("[a-z]", password):
            return False
        elif not re.search("[A-Z]", password):
            return False
        elif not re.search("[0-9]", password):
            return False
        elif not re.search("[_@$]" , password):
            return False
        elif re.search("\s" , password):
            return False
        else:
            return True

def new_quiz(diff):
    conn = sqlite3.connect("Quizzes.db")
    cursor1 = conn.execute("SELECT ID FROM " + diff + "_VOCAB WHERE PROF < 5;")
    cursor2 = conn.execute("SELECT ID FROM " + diff + "_KANJI WHERE PROF < 5;")
    cursor3 = conn.execute("SELECT ID FROM " + diff + "_GRAMMAR WHERE PROF < 5;")
    v = []
    k = []
    g = []
    for i in cursor1:
        v.append(i[0])
    for i in cursor2:
        k.append(i[0])
    for i in cursor3:
        g.append(i[0])

    quiz = []
    for i in range(10):
        if i in (0, 3, 6, 9):
            quiz.append(g.pop(random.randrange(len(g))))
        if i in (1, 4, 7):
            quiz.append(v.pop(random.randrange(len(v))))
        if i in (2, 5, 8):
            quiz.append(k.pop(random.randrange(len(k))))
    conn.close()
    return quiz

def add_bm(level, type, ID):
    conn = sqlite3.connect("Quizzes.db")
    table = level + "_BOOKMARKS"
    total = len(conn.execute("SELECT * FROM " + table + ";").fetchall())
    current_id = str(total + 1)
    command = "INSERT INTO " + table + "(ID) VALUES (" + current_id + ")"
    conn.execute(command)
    command = "UPDATE " + table + " set TYPE = '" + type + "' where ID = " + current_id
    conn.execute(command)
    command = "UPDATE " + table + " set POINTER = '" + str(ID) + "' where ID = " + current_id
    conn.execute(command)
    conn.commit()

def check_user():
    conn = sqlite3.connect("Quizzes.db")
    cursor = conn.cursor()
    t_list = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'
                            AND name='USER'; """).fetchall()
    if t_list == []: return False
    else: return True

def add_open_level(level):
    conn = sqlite3.connect("Quizzes.db")
    table = "OPEN_LEVELS"
    command = "INSERT INTO " + table + "(level) VALUES (" + level + ")"
    conn.execute(command)
    conn.commit()

def check_level_access(diff):
    conn = sqlite3.connect("Quizzes.db")

    cursor1 = conn.execute("SELECT PROF FROM " + diff + "_VOCAB;")
    cursor2 = conn.execute("SELECT PROF FROM " + diff + "_KANJI;")
    cursor3 = conn.execute("SELECT PROF FROM " + diff + "_GRAMMAR;")
    cursor4 = conn.execute("SELECT level FROM OPEN_LEVELS;")

    total = 0
    levels = []

    for i in cursor1:
        total += int(i[0])
    for i in cursor2:
        total += int(i[0])
    for i in cursor3:
        total += int(i[0])

    for i in cursor4:
        levels.append(i[0])
    
    if diff in levels or total >= 80:
        return True
    else:
        return False


bg = '#fffbe6'
current = 0 #counter for the array
current_id = 0 #holder for the current ID value of a question/entry being processed
score = 0 #holder of the quiz score
tally = [] #a tally of which items were answered correctly
contents = [] #contains the contents (ID's) of the quiz
level = "" #current difficulty level selected

#for the primary assessment
first_screen = ""
difficulties = ["N5", "N4", "N3", "N2", "N1"]
passing_scores = [8, 8, 6, 5, 5]
index = 0