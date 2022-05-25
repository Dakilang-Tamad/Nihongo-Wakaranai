import sqlite3
from pathlib import Path
from kivy.properties import StringProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup
from kivy.clock import Clock
import data_handling as dh
import os
import time


class GrammarPop(Popup):
    pass


class VocabPop(Popup):
    pass


class KanjiPop(Popup):
    pass


class LoadingScreen(Screen):
    text = "日本語 Wakaranai"
    def on_enter(self, *args):
        Clock.schedule_once(self.proceed, 3)

    def proceed(self, event):
        self.manager.current = "home"


class HomeScreen(Screen):
    pass


class DifficultySelection(Screen):
    def start5(self):
        dh.level = "N5"
        self.manager.current = "grammari"


class BookmarkCategories(Screen):
    pass


class BookmarkedItems(Screen):
    def Gpop(self):
        pop = GrammarPop()
        pop.open()

    def Vpop(self):
        pop = VocabPop()
        pop.open()

    def Kpop(self):
        pop = KanjiPop()
        pop.open()


class SettingsScreen(Screen):
    pass


class Courses(Screen):
    pass


class GrammarItem(Screen):

    question = StringProperty()
    A = StringProperty()
    B = StringProperty()
    C = StringProperty()
    D = StringProperty()
    ans = StringProperty()

    def on_pre_enter(self, *args):
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()
        retrieve_query = "select * from " + dh.level + "_GRAMMAR where ID = " + str(dh.contents[dh.current])
        cursor.execute(retrieve_query)
        contents = cursor.fetchall()
        for i in contents:
            self.question = i[1]
            self.A = i[2]
            self.B = i[3]
            self.C = i[4]
            self.D = i[5]
            self.ans = i[6]
        cursor.close()


    def ent_a(self):
        dh.current += 1
        if self.ans == 'a':
            dh.score += 1
        self.next_screen()

    def ent_b(self):
        dh.current += 1
        if self.ans == 'b':
            dh.score += 1
        self.next_screen()

    def ent_c(self):
        dh.current += 1
        if self.ans == 'c':
            dh.score += 1
        self.next_screen()

    def ent_d(self):
        dh.current += 1
        if self.ans == 'd':
            dh.score += 1
        self.next_screen()

    def next_screen(self):
        if dh.current == 10:
            self.manager.current = "end"
        else:
            self.manager.current = "vocabi"


class VocabItem(Screen):

    en = StringProperty()
    kanji = StringProperty()
    A = StringProperty()
    B = StringProperty()
    C = StringProperty()
    D = StringProperty()
    ans = StringProperty()

    def on_pre_enter(self, *args):
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()
        retrieve_query = "select * from " + dh.level + "_VOCAB where ID = " + str(dh.contents[dh.current])
        cursor.execute(retrieve_query)
        contents = cursor.fetchall()
        for i in contents:
            self.en = i[1]
            if i[2] != "":
                self.kanji = i[2]
            else:
                self.kanji = "<no kanji>"
            self.A = i[3]
            self.B = i[4]
            self.C = i[5]
            self.D = i[6]
            self.ans = i[7]
        cursor.close()

    def ent_a(self):
        dh.current += 1
        if self.ans == 'a':
            dh.score += 1
        self.manager.current = "kanjii"

    def ent_b(self):
        dh.current += 1
        if self.ans == 'b':
            dh.score += 1
        self.manager.current = "kanjii"

    def ent_c(self):
        dh.current += 1
        if self.ans == 'c':
            dh.score += 1
        self.manager.current = "kanjii"

    def ent_d(self):
        dh.current += 1
        if self.ans == 'd':
            dh.score += 1
        self.manager.current = "kanjii"


class KanjiItem(Screen):

    sentence = StringProperty()
    kanji = StringProperty()
    A = StringProperty()
    B = StringProperty()
    C = StringProperty()
    D = StringProperty()
    ans = StringProperty()

    def on_pre_enter(self, *args):
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()
        retrieve_query = "select * from " + dh.level + "_KANJI where ID = " + str(dh.contents[dh.current])
        cursor.execute(retrieve_query)
        contents = cursor.fetchall()
        for i in contents:
            self.sentence = i[1]
            self.kanji = i[2]
            self.A = i[3]
            self.B = i[4]
            self.C = i[5]
            self.D = i[6]
            self.ans = i[7]
        cursor.close()

    def ent_a(self):
        dh.current += 1
        if self.ans == 'a':
            dh.score += 1
        self.manager.current = "grammari"

    def ent_b(self):
        dh.current += 1
        if self.ans == 'b':
            dh.score += 1
        self.manager.current = "grammari"

    def ent_c(self):
        dh.current += 1
        if self.ans == 'c':
            dh.score += 1
        self.manager.current = "grammari"

    def ent_d(self):
        dh.current += 1
        if self.ans == 'd':
            dh.score += 1
        self.manager.current = "grammari"


class EndQuizz(Screen):
    def Gpop(self):
        pop = GrammarPop()
        pop.open()

    def Vpop(self):
        pop = VocabPop()
        pop.open()

    def Kpop(self):
        pop = KanjiPop()
        pop.open()


class WindowManager(ScreenManager):
    def launch(self, base):
        qc = QuizCont()
        if qc.current < 4:
            qc.current += 1
            self.current = "grammari"
        if (qc.current > 3) and (qc.current < 7):
            qc.current += 1
            self.current = "vocabi"
        if (qc.current > 6) and (qc.current < 10):
            qc.current += 1
            self.current = "kanjii"
        else:
            self.current = "end"


kv = Builder.load_file("my.kv")
tools_path = os.path.dirname("resources/")
icons_path = os.path.join(tools_path, 'komorebi-gothic-P.ttf')

LabelBase.register(name='komorebi',
                   fn_regular=icons_path)


class MainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MainApp().run()
