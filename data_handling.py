import sqlite3
import random
from pathlib import Path


def new_quiz():
    v = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    k = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    g = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,
         26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
    quiz = []
    for i in range(10):
        if i in (0, 3, 6, 9):
            quiz.append(g.pop(random.randrange(len(g))))
        if i in (1, 4, 7):
            quiz.append(v.pop(random.randrange(len(v))))
        if i in (2, 5, 8):
            quiz.append(k.pop(random.randrange(len(k))))

    return quiz

current = 0
score = 0
contents = new_quiz()
level = "N5"