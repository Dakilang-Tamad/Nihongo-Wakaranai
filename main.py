import sqlite3
from pathlib import Path
from kivy.properties import StringProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.label import Label
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


def update_status(level):
    conn = sqlite3.connect("Quizzes.db")
    level = level
    cursor = conn.execute("SELECT BOOKMARK FROM " + level + " WHERE ID=" + str(dh.current_id) + ";")
    for i in cursor:
        if i[0] == 1:
            return "Add Bookmark"
        else:
            return "Bookmarked"
    conn.close()


def update_bookmark(level):
    conn = sqlite3.connect("Quizzes.db")
    level = level
    cursor = conn.execute("SELECT BOOKMARK FROM " + level + " WHERE ID=" + str(dh.current_id) + ";")
    for i in cursor:
        if i[0] == 1:
            command = "UPDATE " + level + " set BOOKMARK = 0 where ID = " + str(dh.current_id)
            conn.execute(command)
            conn.commit()
        else:
            command = "UPDATE " + level + " set BOOKMARK = 1 where ID = " + str(dh.current_id)
            conn.execute(command)
            conn.commit()
    conn.close()


class NoticePop(Popup):
    pass


class GrammarPop(Popup):
    item = StringProperty()
    meaning = StringProperty()
    jp = StringProperty()
    en = StringProperty()
    status = StringProperty()

    def on_pre_open(self):
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_GRAMMAR"
        cursor = conn.execute("SELECT WORD, MEANING, JP, EN FROM " + level +" WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.item = i[0]
            self.meaning = i[1]
            self.jp = i[2]
            self.en = i[3]
        conn.close()

    def update(self):
        level = dh.level + "_GRAMMAR"
        self.status = update_status(level)

    def bookmark(self):
        level = dh.level + "_GRAMMAR"
        update_bookmark(level)
        self.update()


class VocabPop(Popup):
    jp_word = StringProperty()
    reading = StringProperty()
    en_word = StringProperty()
    jp_sent = StringProperty()
    en_sent = StringProperty()
    status = StringProperty()

    def on_pre_open(self):
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_VOCAB"
        cursor = conn.execute("SELECT WORD, KANJI, READING, JP, EN FROM " + level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.jp_word = i[1]
            self.en_word = i[0]
            self.reading = i[2]
            self.jp_sent = i[3]
            self.en_sent = i[4]
        conn.close()

    def update(self):
        level = dh.level + "_VOCAB"
        self.status = update_status(level)

    def bookmark(self):
        level = dh.level + "_VOCAB"
        update_bookmark(level)
        self.update()


class KanjiPop(Popup):
    jp_word = StringProperty()
    translation = StringProperty()
    jp_sent = StringProperty()
    en_sent = StringProperty()
    status = StringProperty()

    def on_pre_open(self):
        self.update()
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

    def update(self):
        level = dh.level + "_KANJI"
        self.status = update_status(level)

    def bookmark(self):
        level = dh.level + "_KANJI"
        update_bookmark(level)
        self.update()


class HomeScreen(Screen):
    pass


class DifficultySelection(Screen):
    def start5(self):
        dh.level = "N5"
        new_contents()
        self.manager.current = "grammari"

    def start1(self):
        pop = NoticePop()
        pop.open()


class BookmarkDifficulty(Screen):
    def notice(self):
        pop = NoticePop()
        pop.open()


class BookmarkedItems(Screen):
    level = dh.level + " BOOKMARKS"

    def on_pre_enter(self, *args):
        diffs = ["GRAMMAR", "VOCAB", "KANJI"]
        for i in diffs:
            self.display(i)

    def display(self, categ):
        table = ""
        query = ""
        if categ in "GRAMMAR":
            table = dh.level + "_" + categ
            query = "WORD"
        if categ in "VOCAB":
            table = dh.level + "_" + categ
            query = "KANJI"
        if categ in "KANJI":
            table = dh.level + "_" + categ
            query = "KANJI"

        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()
        retrieve_query = "select ID, " + query +" from " + table + " where BOOKMARK = 0;"
        cursor.execute(retrieve_query)
        contents = cursor.fetchall()
        if not contents:
            print("empty")
            lbl = Label(text="No bookmarks added yet.", font_name="komorebi")
            if categ == "GRAMMAR":
                self.ids.grammar_tab.add_widget(lbl)
            if categ == "VOCAB":
                self.ids.vocab_tab.add_widget(lbl)
            if categ == "KANJI":
                self.ids.kanji_tab.add_widget(lbl)
        else:
            for i in contents:
                button_text = i[1]
                button = Button(text=button_text, font_name="komorebi")
                button.bind(on_press=lambda x, id=i[0], type=categ: self.popup(type, id))
                if categ == "GRAMMAR":
                    self.ids.grammar_tab.add_widget(button)
                if categ == "VOCAB":
                    self.ids.vocab_tab.add_widget(button)
                if categ == "KANJI":
                    self.ids.kanji_tab.add_widget(button)

    def on_leave(self, *args):
        self.ids.grammar_tab.clear_widgets()
        self.ids.vocab_tab.clear_widgets()
        self.ids.kanji_tab.clear_widgets()

    def popup(self, type, ID):
        dh.current_id = ID
        if type == "GRAMMAR":
            pop = GrammarPop()
            pop.open()
        if type == "VOCAB":
            pop = VocabPop()
            pop.open()
        if type == "KANJI":
            pop = KanjiPop()
            pop.open()


class SettingsScreen(Screen):
    pass


class ContentsDiff(Screen):
    def next_screen(self):
        self.manager.current = "contents"

class Contents(Screen):
    level = dh.level + " CONTENTS"

    def on_pre_enter(self, *args):
        diffs = ["GRAMMAR", "VOCAB", "KANJI"]
        for i in diffs:
            self.display(i)

    def display(self, categ):
        table = ""
        query = ""
        if categ in "GRAMMAR":
            table = dh.level + "_" + categ
            query = "WORD"
        if categ in "VOCAB":
            table = dh.level + "_" + categ
            query = "KANJI"
        if categ in "KANJI":
            table = dh.level + "_" + categ
            query = "KANJI"
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()
        retrieve_query = "select ID, " + query +" from " + table
        cursor.execute(retrieve_query)
        contents = cursor.fetchall()
        if not contents:
            lbl = Label(text="No bookmarks added yet.", font_name="komorebi")
            if categ == "GRAMMAR":
                self.ids.grammar_tab.add_widget(lbl)
            if categ == "VOCAB":
                self.ids.vocab_tab.add_widget(lbl)
            if categ == "KANJI":
                self.ids.kanji_tab.add_widget(lbl)
        else:
            for i in contents:
                button_text = i[1]
                button = Button(text=button_text, font_name="komorebi")
                button.bind(on_press=lambda x, id=i[0], type=categ: self.popup(type, id))
                if categ == "GRAMMAR":
                    self.ids.grammar_tab.add_widget(button)
                if categ == "VOCAB":
                    self.ids.vocab_tab.add_widget(button)
                if categ == "KANJI":
                    self.ids.kanji_tab.add_widget(button)

    def on_leave(self, *args):
        self.ids.grammar_tab.clear_widgets()
        self.ids.vocab_tab.clear_widgets()
        self.ids.kanji_tab.clear_widgets()

    def popup(self, type, ID):
        dh.current_id = ID
        if type == "GRAMMAR":
            pop = GrammarPop()
            pop.open()
        if type == "VOCAB":
            pop = VocabPop()
            pop.open()
        if type == "KANJI":
            pop = KanjiPop()
            pop.open()


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
                retrieve_query = "select WORD from " + dh.level + "_GRAMMAR where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[0] + " - " + dh.tally[i]
                    button = Button(text=button_text, font_name="komorebi")
                    button.bind(on_press=lambda x, id=dh.contents[i], type="grammar": self.popup(type, id))
                    self.ids.review_buttons.add_widget(button)
            if i in (1, 4, 7):
                retrieve_query = "select KANJI from " + dh.level + "_VOCAB where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[0] + " - " + dh.tally[i]
                    button = Button(text=button_text, font_name="komorebi")
                    button.bind(on_press=lambda x, id=dh.contents[i], type="vocab": self.popup(type, id))
                    self.ids.review_buttons.add_widget(button)
            if i in (2, 5, 8):
                retrieve_query = "select KANJI from " + dh.level + "_KANJI where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[0] + " - " + dh.tally[i]
                    button = Button(text=button_text, font_name="komorebi")
                    button.bind(on_press=lambda x, id=dh.contents[i], type="kanji": self.popup(type, id))
                    self.ids.review_buttons.add_widget(button)
        conn.close()

    def on_leave(self, *args):
        self.ids.review_buttons.clear_widgets()

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
