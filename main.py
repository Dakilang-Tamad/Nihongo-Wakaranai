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
from kivy.core.window import Window
import data_handling as dh
from jnius import autoclass
import pygame
import os
import time

def to_audio():
    Locale = autoclass('java.util.Locale')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    tts = TextToSpeech(PythonActivity.mActivity, None)


    tts.setLanguage(Locale.JAPAN)
    tts.speak("日本語分からない",  TextToSpeech.QUEUE_FLUSH, None)


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
            return False
        else:
            return True
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


class ExitPop(Popup):
    def on_pre_open(self):
        w, h = Window.size
        self.width = (w/20)*19
        self.height = (h/10)*6

    def app_close(self):
        App.get_running_app().stop()


class GrammarPop(Popup):
    item = StringProperty()
    meaning = StringProperty()
    jp = StringProperty()
    en = StringProperty()
    status = StringProperty()
    bm_up = StringProperty()
    bm_down = StringProperty()

    def on_pre_open(self):
        w, h = Window.size
        self.width = (w/20)*19
        self.height = (h/10)*6
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_GRAMMAR"
        cursor = conn.execute("SELECT WORD, MEANING, JP, EN FROM " + level +" WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.item = i[0]
            self.meaning = i[1]
            self.jp = "Sample Japanese sentence:\n    " + i[2]
            self.en = "Sample English sentence:\n    " + i[3]
        conn.close()


    def update(self):
        level = dh.level + "_GRAMMAR"
        if update_status(level):
            self.bm_up = "./resources/Buttons/bookmarked_up.png"
            self.bm_down = "./resources/Buttons/bookmarked_down.png"
        else:
            self.bm_up = "./resources/Buttons/add_bookmark_up.png"
            self.bm_down = "./resources/Buttons/add_bookmark_down.png"

    def bookmark(self):
        level = dh.level + "_GRAMMAR"
        update_bookmark(level)
        self.update()

    def tts(self):
        dh.tts = self.item + ".." + self.jp
        to_audio()


class VocabPop1(Popup):
    jp_word = StringProperty()
    reading = StringProperty()
    en_word = StringProperty()
    jp_sent = StringProperty()
    en_sent = StringProperty()
    bm_up = StringProperty()
    bm_down = StringProperty()

    def on_pre_open(self):
        w, h = Window.size
        self.width = (w / 20) * 19
        self.height = (h / 10) * 6
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_VOCAB"
        cursor = conn.execute("SELECT WORD, KANJI, READING, JP, EN FROM " + level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.jp_word = i[1]
            self.en_word = i[0]
            self.reading = i[2]
            self.jp_sent = "Sample Japanese sentence:\n    " + i[3]
            self.en_sent = "Sample English sentence:\n    " + i[4]
        conn.close()

    def update(self):
        level = dh.level + "_VOCAB"
        if update_status(level):
            self.bm_up = "./resources/Buttons/bookmarked_up.png"
            self.bm_down = "./resources/Buttons/bookmarked_down.png"
        else:
            self.bm_up = "./resources/Buttons/add_bookmark_up.png"
            self.bm_down = "./resources/Buttons/add_bookmark_down.png"

    def bookmark(self):
        level = dh.level + "_VOCAB"
        update_bookmark(level)
        self.update()

    def tts(self):
        dh.tts = self.jp_word
        to_audio()


class VocabPop2(Popup):
    jp_word = StringProperty()
    kind = StringProperty()
    meaning = StringProperty()
    furigana = StringProperty()
    jp_sent = StringProperty()
    en_sent = StringProperty()
    bm_up = StringProperty()
    bm_down = StringProperty()

    def on_pre_open(self):
        w, h = Window.size
        self.width = (w / 20) * 19
        self.height = (h / 10) * 6
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_VOCAB"
        cursor = conn.execute("SELECT KANJI, FURIGANA, KIND, MEANING, JP, EN FROM " + level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.jp_word = i[0]
            self.furigana = i[1]
            self.kind = i[2]
            self.meaning = i[3]
            self.jp_sent = "Sample Japanese sentence:\n    " + i[4]
            self.en_sent = "Sample English sentence:\n    " + i[5]
        conn.close()

    def update(self):
        level = dh.level + "_VOCAB"
        if update_status(level):
            self.bm_up = "./resources/Buttons/bookmarked_up.png"
            self.bm_down = "./resources/Buttons/bookmarked_down.png"
        else:
            self.bm_up = "./resources/Buttons/add_bookmark_up.png"
            self.bm_down = "./resources/Buttons/add_bookmark_down.png"

    def bookmark(self):
        level = dh.level + "_VOCAB"
        update_bookmark(level)
        self.update()

    def tts(self):
        dh.tts = self.jp_word
        to_audio()


class KanjiPop(Popup):
    jp_word = StringProperty()
    translation = StringProperty()
    jp_sent = StringProperty()
    en_sent = StringProperty()
    reading = StringProperty()
    bm_up = StringProperty()
    bm_down = StringProperty()

    def on_pre_open(self):
        w, h = Window.size
        self.width = (w / 20) * 19
        self.height = (h / 10) * 6
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_KANJI"
        cursor = conn.execute("SELECT KANJI, KIND, MEANING, JP, EN, READING FROM "
                              + level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.jp_word = i[0]
            self.translation = i[1] + ": " + i[2]
            self.jp_sent = "Sample Japanese sentence:\n    " + i[3]
            self.en_sent = "Sample English Sentence:\n    "+i[4]
            self.reading = i[5]
        conn.close()

    def update(self):
        level = dh.level + "_KANJI"
        if update_status(level):
            self.bm_up = "./resources/Buttons/bookmarked_up.png"
            self.bm_down = "./resources/Buttons/bookmarked_down.png"
        else:
            self.bm_up = "./resources/Buttons/add_bookmark_up.png"
            self.bm_down = "./resources/Buttons/add_bookmark_down.png"

    def bookmark(self):
        level = dh.level + "_KANJI"
        update_bookmark(level)
        self.update()

    def tts(self):
        dh.tts = self.jp_word
        to_audio()


class HomeScreen(Screen):
    pass


class DifficultySelection(Screen):
    level = dh.level

    def start5(self):
        dh.level = "N5"
        new_contents()
        self.manager.current = "grammari"

    def start4(self):
        dh.level = "N4"
        new_contents()
        self.manager.current = "grammari"

    def start3(self):
        dh.level = "N3"
        new_contents()
        self.manager.current = "grammari"

    def start2(self):
        dh.level = "N2"
        new_contents()
        self.manager.current = "grammari"

    def start1(self):
        dh.level = "N1"
        new_contents()
        self.manager.current = "grammari"


class BookmarkDifficulty(Screen):
    def notice(self):
        pop = NoticePop()
        pop.open()

    def book5(self):
        dh.level = "N5"
        self.manager.current = "booki"

    def book4(self):
        dh.level = "N4"
        self.manager.current = "booki"

    def book3(self):
        dh.level = "N3"
        self.manager.current = "booki"

    def book2(self):
        dh.level = "N2"
        self.manager.current = "booki"

    def book1(self):
        dh.level = "N1"
        self.manager.current = "booki"


class BookmarkedItems(Screen):
    level = dh.level + " BOOKMARKS"
    button_up = './resources/Buttons/rec_1_up.png'
    button_down = './resources/Buttons/rec_1_down.png'
    back_up = './resources/Buttons/back_button_up.png'
    back_down = './resources/Buttons/back_button_down.png'

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
                button = Button(text=button_text, font_name="komorebi", color=(0, 0, 0, 1),
                                background_normal=self.button_up, background_down=self.button_down,
                                border=(0, 0, 0, 0))
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
            if dh.level == "N5":
                pop = VocabPop1()
                pop.open()
            else:
                pop = VocabPop2()
                pop.open()
        if type == "KANJI":
            pop = KanjiPop()
            pop.open()


class SettingsScreen(Screen):
    pass


class ContentsDiff(Screen):

    def cont5(self):
        dh.level = "N5"
        self.manager.current = "contents"

    def cont4(self):
        dh.level = "N4"
        self.manager.current = "contents"

    def cont3(self):
        dh.level = "N3"
        self.manager.current = "contents"

    def cont2(self):
        dh.level = "N2"
        self.manager.current = "contents"

    def cont1(self):
        dh.level = "N1"
        self.manager.current = "contents"


class Contents(Screen):
    level = StringProperty()
    button_up = './resources/Buttons/rec_1_up.png'
    button_down = './resources/Buttons/rec_1_down.png'
    back_up = './resources/Buttons/back_button_up.png'
    back_down = './resources/Buttons/back_button_down.png'

    def on_pre_enter(self, *args):
        self.level = dh.level + " CONTENTS"
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
                button = Button(text=button_text, font_name="komorebi", color=(0, 0, 0, 1),
                                background_normal=self.button_up, background_down=self.button_down,
                                border=(0, 0, 0, 0))
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
            if dh.level == "N5":
                pop = VocabPop1()
                pop.open()
            else:
                pop = VocabPop2()
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
    label = StringProperty()
    button_up = "resources/Buttons/rec_2_up.png"
    button_down = 'resources/Buttons/rec_2_down.png'
    border = 'resources/Buttons/empty_box.png'

    def on_pre_enter(self, *args):
        self.label = "Item #" + str(dh.current+1)
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

    item = StringProperty()
    kanji = StringProperty()
    A = StringProperty()
    B = StringProperty()
    C = StringProperty()
    D = StringProperty()
    ans = StringProperty()
    label = StringProperty()
    button_up = "resources/Buttons/rec_2_up.png"
    button_down = 'resources/Buttons/rec_2_down.png'
    border = 'resources/Buttons/empty_box.png'

    def on_pre_enter(self, *args):
        self.label = "Item #" + str(dh.current + 1)
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()
        if dh.level == "N5":
            retrieve_query =("select WORD, KANJI, C_A, C_B, C_C, C_D, ANSWER from " + dh.level +
                            "_VOCAB where ID = " +
                            str(dh.contents[dh.current]))
            cursor.execute(retrieve_query)
        else:
            retrieve_query =("select SENTENCE, KANJI, C_A, C_B, C_C, C_D, ANSWER from " + dh.level +
                            "_VOCAB where ID = " +
                            str(dh.contents[dh.current]))
            cursor.execute(retrieve_query)
        contents = cursor.fetchall()
        for i in contents:
            self.item = i[0]
            if i[1] != "":
                self.kanji = i[1]
            else:
                self.kanji = "<no kanji>"
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
    label = StringProperty()
    button_up = "resources/Buttons/rec_2_up.png"
    button_down = 'resources/Buttons/rec_2_down.png'
    border = 'resources/Buttons/empty_box.png'

    def on_pre_enter(self, *args):
        self.label = "Item #" + str(dh.current + 1)
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
    button_up = './resources/Buttons/rec_2_up.png'
    button_down = './resources/Buttons/rec_2_down.png'
    border = './resources/Buttons/rec_4_up.png'
    back_up = './resources/Buttons/back_button_up.png'
    back_down = './resources/Buttons/back_button_down.png'

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
                    button = Button(text=button_text, font_name="komorebi", color=(0,0,0,1),
                                    background_normal=self.button_up, background_down=self.button_down,
                                    border=(0,0,0,0))
                    button.bind(on_release=lambda x, id=dh.contents[i], type="grammar": self.popup(type, id))
                    self.ids.review_buttons.add_widget(button)
            if i in (1, 4, 7):
                retrieve_query = "select KANJI from " + dh.level + "_VOCAB where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[0] + " - " + dh.tally[i]
                    button = Button(text=button_text, font_name="komorebi", color=(0,0,0,1),
                                    background_normal=self.button_up, background_down=self.button_down,
                                    border=(0,0,0,0))
                    button.bind(on_release=lambda x, id=dh.contents[i], type="vocab": self.popup(type, id))
                    self.ids.review_buttons.add_widget(button)
            if i in (2, 5, 8):
                retrieve_query = "select KANJI from " + dh.level + "_KANJI where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[0] + " - " + dh.tally[i]
                    button = Button(text=button_text, font_name="komorebi", color=(0,0,0,1),
                                    background_normal=self.button_up, background_down=self.button_down,
                                    border=(0,0,0,0))
                    button.bind(on_release=lambda x, id=dh.contents[i], type="kanji": self.popup(type, id))
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
            if dh.level == "N5":
                pop = VocabPop1()
                pop.open()
            else:
                pop = VocabPop2()
                pop.open()
        if type == "kanji":
            pop = KanjiPop()
            pop.open()



class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")
tools_path = os.path.dirname("resources/")
icons_path1 = os.path.join(tools_path, 'komorebi-gothic-P.ttf')
icons_path2 = os.path.join(tools_path, 'ComicSansMSBold.ttf')

LabelBase.register(name='komorebi',
                   fn_regular=icons_path1)
LabelBase.register(name='ComicSans',
                   fn_regular=icons_path2)


class MainApp(App):
    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            pop = ExitPop()
            pop.open()
            return True

    def build(self):
        return kv


if __name__ == "__main__":
    MainApp().run()
