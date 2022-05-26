import sqlite3
from pathlib import Path
from kivy.properties import StringProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
import data_handling as dh
import os
import time

def new_contents():
    dh.contents = dh.new_quiz()
    dh.current = 0
    dh.tally = []
    dh.score = 0


class GrammarPop(Popup):
    item = StringProperty()
    jp = StringProperty()
    en = StringProperty()
    def on_pre_open(self):
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_GRAMMAR"
        cursor = conn.execute("SELECT WORD, JP, EN FROM " + level +" WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.item = i[0]
            self.jp = i[1]
            self.en = i[2]
        conn.close()


class VocabPop(Popup):
    jp_word = StringProperty()
    en_word = StringProperty()
    jp_sent = StringProperty()
    en_sent = StringProperty()

    def on_pre_open(self):
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_VOCAB"
        cursor = conn.execute("SELECT WORD, kanji, JP, EN FROM " + level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.jp_word = i[1]
            self.en_word = i[0]
            self.jp_sent = i[2]
            self.en_sent = i[3]
        conn.close()


class KanjiPop(Popup):
    jp_word = StringProperty()
    translation = StringProperty()
    jp_sent = StringProperty()
    en_sent = StringProperty()

    def on_pre_open(self):
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_KANJI"
        cursor = conn.execute("SELECT KANJI, KIND, MEANING, JP, EN FROM "
                              + level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.jp_word = i[0]
            self.translation = i[1] + "\n" + i[2]
            self.jp_sent = i[3]
            self.en_sent = i[4]
        conn.close()


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
        new_contents()
        self.manager.current = "grammari"

    def start1(self):
        self.manager.current = "end"


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
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.next_screen()

    def ent_b(self):
        dh.current += 1
        if self.ans == 'b':
            dh.score += 1
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.next_screen()

    def ent_c(self):
        dh.current += 1
        if self.ans == 'c':
            dh.score += 1
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.next_screen()

    def ent_d(self):
        dh.current += 1
        if self.ans == 'd':
            dh.score += 1
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
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
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.manager.current = "kanjii"

    def ent_b(self):
        dh.current += 1
        if self.ans == 'b':
            dh.score += 1
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.manager.current = "kanjii"

    def ent_c(self):
        dh.current += 1
        if self.ans == 'c':
            dh.score += 1
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.manager.current = "kanjii"

    def ent_d(self):
        dh.current += 1
        if self.ans == 'd':
            dh.score += 1
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
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
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.manager.current = "grammari"

    def ent_b(self):
        dh.current += 1
        if self.ans == 'b':
            dh.score += 1
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.manager.current = "grammari"

    def ent_c(self):
        dh.current += 1
        if self.ans == 'c':
            dh.score += 1
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.manager.current = "grammari"

    def ent_d(self):
        dh.current += 1
        if self.ans == 'd':
            dh.score += 1
            dh.tally.append("Correct")
        else:
            dh.tally.append("Incorrect")
        self.manager.current = "grammari"


class EndQuizz(Screen):
    score = StringProperty()

    def on_pre_enter(self, **kwargs):
        self.score = "Your score is " + str(dh.score) + "/10"
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()

        for i in range(10):
            if i in (0, 3, 6, 9):
                retrieve_query = "select * from " + dh.level + "_GRAMMAR where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[7] + " - " + dh.tally[i]
                    button = Button(text=button_text, font_name="komorebi")
                    button.bind(on_press=lambda x, id=j[0], type="grammar": self.popup(type, id))
                    self.ids.review_buttons.add_widget(button)
            if i in (1, 4, 7):
                retrieve_query = "select * from " + dh.level + "_VOCAB where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[8] + " - " + dh.tally[i]
                    button = Button(text=button_text, font_name="komorebi")
                    button.bind(on_press=lambda x, id=j[0], type="vocab": self.popup(type, id))
                    self.ids.review_buttons.add_widget(button)
            if i in (2, 5, 8):
                retrieve_query = "select * from " + dh.level + "_KANJI where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[8] + " - " + dh.tally[i]
                    button = Button(text=button_text, font_name="komorebi")
                    button.bind(on_press=lambda x, id=j[0], type="kanji": self.popup(type, id))
                    self.ids.review_buttons.add_widget(button)
        conn.close()

    def popup(self, type, ID):
        dh.current_id = ID
        if type == "grammar":
            pop = GrammarPop()
            pop.open()
        if type == "vocab":
            pop = VocabPop()
            pop.open()
        if type == "kanji":
            pop = KanjiPop()
            pop.open()



class WindowManager(ScreenManager):
    pass


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
