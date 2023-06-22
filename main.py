import sqlite3
from pathlib import Path
from kivy.properties import StringProperty
from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.core.image import Image as CoreImage
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import sp
from threading import Thread
import data_handling as dh
import json
import urllib.request
# from jnius import autoclass
import os
import ssl

# This part was commented for development; only works on android build
# Locale = autoclass('java.util.Locale')
# PythonActivity = autoclass('org.kivy.android.PythonActivity')
# TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
# tts = TextToSpeech(PythonActivity.mActivity, None)

class CustomButton(Button):
    bookmarked = BooleanProperty(False)


def connected():
    try:
        context = ssl._create_unverified_context()
        urllib.request.urlopen('https://www.google.com/', cotext=context)
        return True
    except:
        return False


def to_audio():
    # tts.setLanguage(Locale.JAPAN)
    # tts.speak(dh.tts + " Example, " + dh.tts_sentence, TextToSpeech.QUEUE_FLUSH, None)
    pass


def new_contents():
    dh.answers = ["e","e","e","e","e","e","e","e","e","e"]
    dh.keys = ["e","e","e","e","e","e","e","e","e","e"]
    dh.contents = dh.new_quiz(dh.level)
    dh.current = 0
    dh.score = 0


def update_status(level):
    conn = sqlite3.connect("Quizzes.db")
    level = level
    cursor = conn.execute("SELECT BOOKMARK FROM " +
                          level + " WHERE ID=" + str(dh.current_id) + ";")
    for i in cursor:
        if i[0] == 1:
            return False
        else:
            return True
    conn.close()


def add_prof(level):
    conn = sqlite3.connect("Quizzes.db")
    level = level
    cursor = conn.execute("SELECT PROF FROM " + level +
                          " WHERE ID = " + str(dh.contents[dh.current - 1]) + ";")
    prof = 0
    for i in cursor:
        prof = i[0] + 1
    command = "UPDATE " + level + " set PROF = " + \
        str(prof) + " where ID = " + str(dh.contents[dh.current - 1])
    conn.execute(command)
    conn.commit()
    conn.close()


def update_bookmark(level):
    conn = sqlite3.connect("Quizzes.db")
    level = level
    cursor = conn.execute("SELECT BOOKMARK FROM " +
                          level + " WHERE ID=" + str(dh.current_id) + ";")
    for i in cursor:
        if i[0] == 1:
            command = "UPDATE " + level + \
                " set BOOKMARK = 0 where ID = " + str(dh.current_id)
            conn.execute(command)
            conn.commit()
        else:
            command = "UPDATE " + level + \
                " set BOOKMARK = 1 where ID = " + str(dh.current_id)
            conn.execute(command)
            conn.commit()
    conn.close()


def new_user_table():
    conn = sqlite3.connect("Quizzes.db")
    cursor = conn.cursor()
    t_list = cursor.execute("""SELECT table_name FROM USER;""").fetchall()
    new_table = Thread(target = dh.new_table, args = t_list[0])
    new_table.start()
    new_table.join()
    dh.error = 14
    Clock.schedule_once(lambda dt: NoticePop().open())


def retrieve_user_progress():
    conn = sqlite3.connect("Quizzes.db")
    cursor = conn.cursor()
    t_list = cursor.execute("""SELECT table_name FROM USER;""").fetchall()
    retrieve_progress = Thread(target = dh.retrieve_progress, args = t_list[0])
    retrieve_progress.start()


class LogoutPop(Popup):
    def on_pre_open(self):
        w, h = Window.size
        self.width = w*0.8
        self.height = h/3

    def logout(self):
        Thread(target=dh.log_out).start()
        dh.first_screen = "signup"
        MDApp.get_running_app().root.current = "signup"
        self.dismiss()


class GrammarQ(Popup):
    question = StringProperty()
    choice = StringProperty()
    key = StringProperty()

    def on_pre_open(self):
        w, h = Window.size
        self.width = (w/20)*19
        self.height = (h/10)*6
        conn = sqlite3.connect("Quizzes.db")
        choice = "C_" + (dh.answers[dh.pop_index]).upper()
        key = "C_" + (dh.keys[dh.pop_index]).upper()

        cursor = conn.execute("SELECT QUESTION, " + choice + ", " + key + " FROM " + dh.level + "_GRAMMAR WHERE ID = " + str(dh.current_id))

        for i in cursor:
            self.question = i[0]
            self.choice = i[1]
            self.key = i[2]


class VocabQ(Popup):
    question = StringProperty()
    item = StringProperty()
    choice = StringProperty()
    key = StringProperty()

    def on_pre_open(self):
        w, h = Window.size
        self.width = (w/20)*19
        self.height = (h/10)*6
        conn = sqlite3.connect("Quizzes.db")
        choice = "C_" + (dh.answers[dh.pop_index]).upper()
        key = "C_" + (dh.keys[dh.pop_index]).upper()

        if dh.level == "N5":
            cursor = conn.execute("SELECT WORD, " + choice + ", " + key + ", ITEM FROM " + dh.level + "_VOCAB WHERE ID = " + str(dh.current_id))
        else:
            cursor = conn.execute("SELECT SENTENCE, " + choice + ", " + key + ", KANJI FROM " + dh.level + "_VOCAB WHERE ID = " + str(dh.current_id))

        for i in cursor:
            self.question = i[0]
            self.choice = i[1]
            self.key = i[2]
            self.item = i[3]


class KanjiQ(Popup):
    question = StringProperty()
    item = StringProperty()
    choice = StringProperty()
    key = StringProperty()

    def on_pre_open(self):
        w, h = Window.size
        self.width = (w/20)*19
        self.height = (h/10)*6
        conn = sqlite3.connect("Quizzes.db")
        choice = "C_" + (dh.answers[dh.pop_index]).upper()
        key = "C_" + (dh.keys[dh.pop_index]).upper()

        cursor = conn.execute("SELECT QUESTION, " + choice + ", " + key + ", ITEM FROM " + dh.level + "_KANJI WHERE ID = " + str(dh.current_id))

        for i in cursor:
            self.question = i[0]
            self.choice = i[1]
            self.key = i[2]
            self.item = i[3]


class ValidationPop(Popup):
    pass


class ProfilePop(Popup):
    username = StringProperty()
    n5_prog = StringProperty()
    n4_prog = StringProperty()
    n3_prog = StringProperty()
    n2_prog = StringProperty()
    n1_prog = StringProperty()
    level = StringProperty()

    def on_pre_open(self):
        data = dh.get_user()
        self.username = "Username: " + data[0]
        self.n1_prog = data[1]
        self.n2_prog = data[2]
        self.n3_prog = data[3]
        self.n4_prog = data[4]
        self.n5_prog = data[5]
        self.level = "Current Level: " + data[6]
    
    def logout(self):
        Thread(target=dh.log_out).start()
        dh.first_screen = "signup"
        MDApp.get_running_app().root.current = "signup"
        self.dismiss()


class NoticePop(Popup):
    error_text = StringProperty()

    def on_pre_open(self):
        with open('errors.json') as x:
            error = json.load(x)

        if dh.error == 1:
            self.error_text = error['empty_settings']
        elif dh.error == 2:
            self.error_text = error['level_locked']
        elif dh.error == 3:
            self.error_text = error['invalid_password_1']
        elif dh.error == 4:
            self.error_text = error['invalid_password_2']
        elif dh.error == 5:
            self.error_text = error['invalid_creds']
        elif dh.error == 6:
            self.error_text = error['primary_upload']
        elif dh.error == 7:
            self.error_text = error['retrieve_progress']
        elif dh.error == 8:
            self.error_text = error['to_n4']
        elif dh.error == 9:
            self.error_text = error['to_n3']
        elif dh.error == 10:
            self.error_text = error['to_n2']
        elif dh.error == 11:
            self.error_text = error['to_n1']
        elif dh.error == 12:
            self.error_text = error['n5_start']
        elif dh.error == 13:
            self.error_text = error['db_error']
        elif dh.error == 14:
            self.error_text = error['safe_dc']
        elif dh.error == 15:
            self.error_text = error['username_error']
        else:
            self.error_text = "Unknown Error"


class ExitPop(Popup):
    def on_pre_open(self):
        w, h = Window.size
        self.width = (w/20)*19
        self.height = (h/10)*6

    def app_close(self):
        App.get_running_app().stop()


class UpdatePop(Popup):

    def on_pre_open(self):
        self.p1 = True
        self.p2 = False
        w, h = Window.size
        self.width = (w/20)*19
        self.height = (h/10)*6

    def condition(self, param):
        if param:
            return True
        else:
            return False


class GrammarPop(Popup):
    item = StringProperty()
    meaning = StringProperty()
    jp = StringProperty()
    en = StringProperty()
    status = StringProperty()
    bm_up = StringProperty()
    bm_down = StringProperty()
    prog = StringProperty()

    def initialize(self):
        w, h = Window.size
        self.width = (w/20)*19
        self.height = (h/10)*6
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_GRAMMAR"
        cursor = conn.execute("SELECT WORD, MEANING, JP, EN, PROF FROM " +
                              level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.item = i[0]
            self.meaning = i[1]
            self.jp = "Sample Japanese sentence:\n    " + i[2]
            self.sentence = i[2]
            self.en = "English Translation:\n    " + i[3]
            self.prog = "Progress: " + str(i[4]) + "/5"
        conn.close()

        back_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        next_anchor = AnchorLayout(anchor_x='center', anchor_y='center')

        self.ids.nav.add_widget(back_anchor)
        self.ids.nav.add_widget(next_anchor)

        if dh.pop_source != "review":
            if dh.current_id != 1:
                back = Button(background_normal='./resources/Buttons_2/BackButtonNew.png',
                                        border=(0, 0, 0, 0),
                                        size_hint=(None, None), width=self.width/7, height=self.width/7)
                back.bind(on_release=self.prev)
                back_anchor.add_widget(back)
            if dh.current_id != 50:
                next = Button(background_normal='./resources/Buttons_2/NextButtonNew.png',
                                        border=(0, 0, 0, 0),
                                        size_hint=(None, None), width=self.width/7, height=self.width/7)
                next.bind(on_release=self.next)
                next_anchor.add_widget(next)
        else: pass

    def on_pre_open(self):
        self.initialize()
    
    def prev(self, *args):
        dh.current_id -= 1
        self.ids.nav.clear_widgets()
        self.initialize()

    def next(self, *args):
        dh.current_id += 1
        self.ids.nav.clear_widgets()
        self.initialize()

    def update(self):
        level = dh.level + "_GRAMMAR"
        if update_status(level):
            self.bm_up = "./resources/Buttons_2/Bookmark_Clicked.png"
        else:
            self.bm_up = "./resources/Buttons_2/Bookmark_Def.png"

    def bookmark(self):
        level = dh.level + "_GRAMMAR"
        update_bookmark(level)
        self.update()

    def tts(self):
        dh.tts = self.item
        dh.tts_sentence = self.sentence
        to_audio()


class VocabPop1(Popup):
    jp_word = StringProperty()
    reading = StringProperty()
    en_word = StringProperty()
    jp_sent = StringProperty()
    en_sent = StringProperty()
    bm_up = StringProperty()
    bm_down = StringProperty()
    prog = StringProperty()

    def initialize(self):
        w, h = Window.size
        self.width = (w / 20) * 19
        self.height = (h / 10) * 6
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_VOCAB"
        cursor = conn.execute("SELECT WORD, KANJI, READING, JP, EN, PROF FROM " +
                              level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.jp_word = i[1]
            self.en_word = i[0]
            self.reading = i[2]
            self.jp_sent = "Sample Japanese sentence:\n    " + i[3]
            self.sentence = i[3]
            self.en_sent = "English Translation:\n    " + i[4]
            self.prog = "Progress: " + str(i[5]) + "/5"
        conn.close()

        back_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        next_anchor = AnchorLayout(anchor_x='center', anchor_y='center')

        self.ids.nav.add_widget(back_anchor)
        self.ids.nav.add_widget(next_anchor)


        if dh.pop_source != "review":
            if dh.current_id != 1:
                back = Button(background_normal='./resources/Buttons_2/BackButtonNew.png',
                                        border=(0, 0, 0, 0),
                                        size_hint=(None, None), width=self.width/7, height=self.width/7)
                back.bind(on_release=self.prev)
                back_anchor.add_widget(back)
            if dh.current_id != 25:
                next = Button(background_normal='./resources/Buttons_2/NextButtonNew.png',
                                        border=(0, 0, 0, 0),
                                        size_hint=(None, None), width=self.width/7, height=self.width/7)
                next.bind(on_release=self.next)
                next_anchor.add_widget(next)
        else: pass
    
    def prev(self, *args):
        dh.current_id -= 1
        self.ids.nav.clear_widgets()
        self.initialize()

    def next(self, *args):
        dh.current_id += 1
        self.ids.nav.clear_widgets()
        self.initialize()

    def on_pre_open(self):
        self.initialize()

    def update(self):
        level = dh.level + "_VOCAB"
        if update_status(level):
            self.bm_up = "./resources/Buttons_2/Bookmark_Clicked.png"
        else:
            self.bm_up = "./resources/Buttons_2/Bookmark_Def.png"

    def bookmark(self):
        level = dh.level + "_VOCAB"
        update_bookmark(level)
        self.update()

    def tts(self):
        dh.tts = self.jp_word
        dh.tts_sentence = self.sentence
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
    prog = StringProperty()

    def initialize(self):
        w, h = Window.size
        self.width = (w / 20) * 19
        self.height = (h / 10) * 6
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_VOCAB"
        cursor = conn.execute("SELECT KANJI, FURIGANA, KIND, MEANING, JP, EN, PROF FROM " +
                              level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.jp_word = i[0]
            self.furigana = i[1]
            self.kind = i[2]
            self.meaning = i[3]
            self.jp_sent = "Sample Japanese sentence:\n    " + i[4]
            self.sentence = i[4]
            self.en_sent = "English Translation:\n    " + i[5]
            self.prog = "Progress: " + str(i[6]) + "/5"
        conn.close()

        back_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        next_anchor = AnchorLayout(anchor_x='center', anchor_y='center')

        self.ids.nav.add_widget(back_anchor)
        self.ids.nav.add_widget(next_anchor)

        if dh.pop_source != "review":
            if dh.current_id != 1:
                back = Button(background_normal='./resources/Buttons_2/BackButtonNew.png',
                                        border=(0, 0, 0, 0),
                                        size_hint=(None, None), width=self.width/7, height=self.width/7)
                back.bind(on_release=self.prev)
                back_anchor.add_widget(back)
            if dh.current_id != 25:
                next = Button(background_normal='./resources/Buttons_2/NextButtonNew.png',
                                        border=(0, 0, 0, 0),
                                        size_hint=(None, None), width=self.width/7, height=self.width/7)
                next.bind(on_release=self.next)
                next_anchor.add_widget(next)
        else: pass

    def on_pre_open(self):
        self.initialize()
    
    def prev(self, *args):
        dh.current_id -= 1
        self.ids.nav.clear_widgets()
        self.initialize()

    def next(self, *args):
        dh.current_id += 1
        self.ids.nav.clear_widgets()
        self.initialize()
        

    def update(self):
        level = dh.level + "_VOCAB"
        if update_status(level):
            self.bm_up = "./resources/Buttons_2/Bookmark_Clicked.png"
        else:
            self.bm_up = "./resources/Buttons_2/Bookmark_Def.png"

    def bookmark(self):
        level = dh.level + "_VOCAB"
        update_bookmark(level)
        self.update()

    def tts(self):
        dh.tts = self.jp_word
        dh.tts_sentence = self.sentence
        to_audio()


class KanjiPop(Popup):
    jp_word = StringProperty()
    translation = StringProperty()
    jp_sent = StringProperty()
    en_sent = StringProperty()
    reading = StringProperty()
    bm_up = StringProperty()
    bm_down = StringProperty()
    prog = StringProperty()

    def initialize(self):
        w, h = Window.size
        self.width = (w / 20) * 19
        self.height = (h / 10) * 6
        self.update()
        conn = sqlite3.connect("Quizzes.db")
        level = dh.level + "_KANJI"
        cursor = conn.execute("SELECT KANJI, KIND, MEANING, JP, EN, READING, PROF FROM "
                              + level + " WHERE ID=" + str(dh.current_id) + ";")
        for i in cursor:
            self.jp_word = i[0]
            self.translation = i[1] + ": " + i[2]
            self.jp_sent = "Sample Japanese sentence:\n    " + i[3]
            self.sentence = i[3]
            self.en_sent = "English Translation:\n    "+i[4]
            self.reading = i[5]
            self.prog = "Progress: " + str(i[6]) + "/5"
        conn.close()

        back_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        next_anchor = AnchorLayout(anchor_x='center', anchor_y='center')

        self.ids.nav.add_widget(back_anchor)
        self.ids.nav.add_widget(next_anchor)

        if dh.pop_source != "review":
            if dh.current_id != 1:
                back = Button(background_normal='./resources/Buttons_2/BackButtonNew.png',
                                        border=(0, 0, 0, 0),
                                        size_hint=(None, None), width=self.width/7, height=self.width/7)
                back.bind(on_release=self.prev)
                back_anchor.add_widget(back)
            if dh.current_id != 25:
                next = Button(background_normal='./resources/Buttons_2/NextButtonNew.png',
                                        border=(0, 0, 0, 0),
                                        size_hint=(None, None), width=self.width/7, height=self.width/7)
                next.bind(on_release=self.next)
                next_anchor.add_widget(next)
        else: pass

    def on_pre_open(self):
        self.initialize()
    
    def prev(self, *args):
        dh.current_id -= 1
        self.ids.nav.clear_widgets()
        self.initialize()

    def next(self, *args):
        dh.current_id += 1
        self.ids.nav.clear_widgets()
        self.initialize()
        

    def update(self):
        level = dh.level + "_KANJI"
        if update_status(level):
            self.bm_up = "./resources/Buttons_2/Bookmark_Clicked.png"
        else:
            self.bm_up = "./resources/Buttons_2/Bookmark_Def.png"

    def bookmark(self):
        level = dh.level + "_KANJI"
        update_bookmark(level)
        self.update()

    def tts(self):
        dh.tts = self.jp_word
        dh.tts_sentence = self.sentence
        to_audio()


class Dummy(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch_screen)

    def switch_screen(self, dt):
        if dh.check_user():
            dh.first_screen = "home"
            self.manager.current = "home"
        else:
            dh.first_screen = "signup"
            self.manager.current = "signup"


class Signup(Screen):
    def signup(self):
        try:
            usrname = self.ids.s_name.text
            pass1 = self.ids.s_pass.text
            pass2 = self.ids.s_pass_2.text

            if (pass1 == pass2):
                if (dh.validate(usrname, pass1)):
                    if (dh.check_duplicate(usrname)):
                        self.new_acc = Thread(target=dh.signup, args=(usrname, pass1,))
                        self.new_acc.start()
                        dh.level = dh.difficulties[dh.index]
                        new_contents()
                        self.manager.current = "entry"
                    else:
                        dh.error = 15
                        NoticePop().open()
                else:
                    ValidationPop().open()
            else:
                dh.error = 4
                NoticePop().open()
        except:
            dh.error = 13
            NoticePop().open()

    def login(self):
        self.manager.current = "login"


class Login(Screen):
    def login(self):
        try:
            dh.first_screen = "login"
            username = self.ids.s_name.text
            password = self.ids.s_pass.text

            table = dh.log_in(username, password)

            if table == None:
                dh.error = 5
                NoticePop().open()
            else:
                dh.create_user(username, table)
                self.retrieve = Thread(target=dh.retrieve_progress, args=(table,))
                self.retrieve.start()
                self.manager.current = "home"
        except:
            dh.error = 13
            NoticePop().open()

    def signup(self):
        self.manager.current = "signup"


class HomeScreen(Screen):
    def on_enter(self, *args):
        try:
            if dh.first_screen == "signup":
                new_table = Thread(target = new_user_table)
                new_table.start()
                dh.first_screen = ""
                dh.error = 6
                NoticePop().open()
            if dh.first_screen == "home":
                update = Thread(target = dh.update_progress)
                update.start()
                dh.first_screen = ""
        except:
            dh.error = 13
            NoticePop().open()

    def raise_notice(self):
        dh.error = 1
        NoticePop().open()

    def open_profile(self):
        ProfilePop().open()
    
    def raise_logout(self):
        LogoutPop().open()


class DifficultySelection(Screen):
    level = dh.level

    def initialize(self):
        conn = sqlite3.connect("Quizzes.db")
        levels = conn.execute("select level from OPEN_LEVELS").fetchall()
        unlocked = []

        for i in levels:
            unlocked.append(i[0])
        
        if "N5" not in unlocked:
            self.ids.n5.background_normal= 'resources/Buttons_2/N5_Locked.png'
        if "N4" not in unlocked:
            self.ids.n4.background_normal= 'resources/Buttons_2/N4_Locked.png'
        if "N3" not in unlocked:
            self.ids.n3.background_normal= 'resources/Buttons_2/N3_Locked.png'
        if "N2" not in unlocked:
            self.ids.n2.background_normal= 'resources/Buttons_2/N2_Locked.png'
        if "N1" not in unlocked:
            self.ids.n1.background_normal= 'resources/Buttons_2/N1_Locked.png'

    def on_pre_enter(self, *args):
        self.initialize()

    def start5(self):
        dh.level = "N5"
        if dh.check_level_access(dh.level):
            new_contents()
            self.manager.current = "grammari"
        else:
            dh.error = 2
            NoticePop().open()

    def start4(self):
        dh.level = "N4"
        if dh.check_level_access(dh.level):
            new_contents()
            self.manager.current = "grammari"
        else:
            dh.error = 2
            NoticePop().open()

    def start3(self):
        dh.level = "N3"
        if dh.check_level_access(dh.level):
            new_contents()
            self.manager.current = "grammari"
        else:
            dh.error = 2
            NoticePop().open()

    def start2(self):
        dh.level = "N2"
        if dh.check_level_access(dh.level):
            new_contents()
            self.manager.current = "grammari"
        else:
            dh.error = 2
            NoticePop().open()

    def start1(self):
        dh.level = "N1"
        if dh.check_level_access(dh.level):
            new_contents()
            self.manager.current = "grammari"
        else:
            dh.error = 2
            NoticePop().open()


class BookmarkDifficulty(Screen):

    def initialize(self):
        conn = sqlite3.connect("Quizzes.db")
        levels = conn.execute("select level from OPEN_LEVELS").fetchall()
        unlocked = []

        for i in levels:
            unlocked.append(i[0])
        
        if "N5" not in unlocked:
            self.ids.n5.background_normal= 'resources/Buttons_2/N5_Locked.png'
        if "N4" not in unlocked:
            self.ids.n4.background_normal= 'resources/Buttons_2/N4_Locked.png'
        if "N3" not in unlocked:
            self.ids.n3.background_normal= 'resources/Buttons_2/N3_Locked.png'
        if "N2" not in unlocked:
            self.ids.n2.background_normal= 'resources/Buttons_2/N2_Locked.png'
        if "N1" not in unlocked:
            self.ids.n1.background_normal= 'resources/Buttons_2/N1_Locked.png'


    def on_pre_enter(self, *args):
        self.initialize()

    def book5(self):
        dh.level = "N5"
        if dh.check_level_access(dh.level):
            self.manager.current = "booki"
        else:
            dh.error = 2
            NoticePop().open()

    def book4(self):
        dh.level = "N4"
        if dh.check_level_access(dh.level):
            self.manager.current = "booki"
        else:
            dh.error = 2
            NoticePop().open()

    def book3(self):
        dh.level = "N3"
        if dh.check_level_access(dh.level):
            self.manager.current = "booki"
        else:
            dh.error = 2
            NoticePop().open()

    def book2(self):
        dh.level = "N2"
        if dh.check_level_access(dh.level):
            self.manager.current = "booki"
        else:
            dh.error = 2
            NoticePop().open()

    def book1(self):
        dh.level = "N1"
        if dh.check_level_access(dh.level):
            self.manager.current = "booki"
        else:
            dh.error = 2
            NoticePop().open()


class BookmarkedItems(Screen):
    level = StringProperty()
    button_up = './resources/Buttons/rec_1_up.png'
    button_down = './resources/Buttons/rec_1_down.png'
    bm_up = './resources/Buttons/bm_1_up.png'
    bm_down = './resources/Buttons/bm_1_down.png'
    back_up = './resources/Buttons/back_button_up.png'
    back_down = './resources/Buttons/back_button_down.png'
    buttons = []

    def on_pre_enter(self, *args):
        self.level = dh.level + " BOOKMARKS"
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
        retrieve_query = "select ID, " + query + \
            " from " + table + " where BOOKMARK = 0;"
        cursor.execute(retrieve_query)
        contents = cursor.fetchall()
        if not contents:
            lbl = Label(text="No bookmarks added yet.",
                        font_name="jp_font", color="black")
            if categ == "GRAMMAR":
                self.ids.grammar_tab.add_widget(lbl)
            if categ == "VOCAB":
                self.ids.vocab_tab.add_widget(lbl)
            if categ == "KANJI":
                self.ids.kanji_tab.add_widget(lbl)
        else:
            for i in contents:
                button_text = i[1]
                button = Button(text=button_text, font_name="jp_font", color=(0, 0, 0, 1), font_size= sp(20),
                                background_normal=self.bm_up, background_down=self.bm_down,
                                border=(0, 0, 0, 0))
                button.bind(on_press=lambda x,
                            id=i[0], type=categ: self.popup(type, id))
                button.bind(on_release=lambda x, button=button: self.change_color(button))
                if categ == "GRAMMAR":
                    self.ids.grammar_tab.add_widget(button)
                if categ == "VOCAB":
                    self.ids.vocab_tab.add_widget(button)
                if categ == "KANJI":
                    self.ids.kanji_tab.add_widget(button)
    
    def change_color(self, current_button):
        current_button.background_normal = 'resources/Buttons/bm_picked.png'
        for button in self.buttons:
            if button.text != current_button.text:
                button.background_normal = 'resources/Buttons/bm_1_up.png'


    def on_leave(self, *args):
        self.ids.grammar_tab.clear_widgets()
        self.ids.vocab_tab.clear_widgets()
        self.ids.kanji_tab.clear_widgets()

    def popup(self, type, ID):
        dh.pop_source = "bookmarks"
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


class ContentsDiff(Screen):

    def initialize(self):
        conn = sqlite3.connect("Quizzes.db")
        levels = conn.execute("select level from OPEN_LEVELS").fetchall()
        unlocked = []

        for i in levels:
            unlocked.append(i[0])
        
        if "N5" not in unlocked:
            self.ids.n5.background_normal= 'resources/Buttons_2/N5_Locked.png'
        if "N4" not in unlocked:
            self.ids.n4.background_normal= 'resources/Buttons_2/N4_Locked.png'
        if "N3" not in unlocked:
            self.ids.n3.background_normal= 'resources/Buttons_2/N3_Locked.png'
        if "N2" not in unlocked:
            self.ids.n2.background_normal= 'resources/Buttons_2/N2_Locked.png'
        if "N1" not in unlocked:
            self.ids.n1.background_normal= 'resources/Buttons_2/N1_Locked.png'


    def on_pre_enter(self, *args):
        self.initialize()
        
    def cont5(self):
        dh.level = "N5"
        if dh.check_level_access(dh.level):
            self.manager.current = "contents"
        else:
            dh.error = 2
            NoticePop().open()

    def cont4(self):
        dh.level = "N4"
        if dh.check_level_access(dh.level):
            self.manager.current = "contents"
        else:
            dh.error = 2
            NoticePop().open()

    def cont3(self):
        dh.level = "N3"
        if dh.check_level_access(dh.level):
            self.manager.current = "contents"
        else:
            dh.error = 2
            NoticePop().open()

    def cont2(self):
        dh.level = "N2"
        if dh.check_level_access(dh.level):
            self.manager.current = "contents"
        else:
            dh.error = 2
            NoticePop().open()

    def cont1(self):
        dh.level = "N1"
        if dh.check_level_access(dh.level):
            self.manager.current = "contents"
        else:
            dh.error = 2
            NoticePop().open()


class Contents(Screen):
    level = StringProperty()
    button_up = './resources/Buttons/rec_1_up.png'
    button_down = './resources/Buttons/rec_1_down.png'
    bm_up = './resources/Buttons/bm_1_up.png'
    bm_down = './resources/Buttons/bm_1_down.png'
    back_up = './resources/Buttons/back_button_up.png'
    back_down = './resources/Buttons/back_button_down.png'
    buttons = []

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
        retrieve_query = "select ID,  " + query + ", BOOKMARK from " + table
        cursor.execute(retrieve_query)
        contents = cursor.fetchall()
        if not contents:
            lbl = Label(text="No bookmarks added yet.", font_name="jp_font")
            if categ == "GRAMMAR":
                self.ids.grammar_tab.add_widget(lbl)
            if categ == "VOCAB":
                self.ids.vocab_tab.add_widget(lbl)
            if categ == "KANJI":
                self.ids.kanji_tab.add_widget(lbl)
        else:
            for i in contents:
                button_text = i[1]
                if i[2] == 1:
                    button = CustomButton(text=button_text, font_name="jp_font", color=(0, 0, 0, 1), font_size= sp(20),
                                background_normal=self.button_up, background_down=self.button_down, bookmarked = False,
                                border=(0, 0, 0, 0))
                else:
                    button = CustomButton(text=button_text, font_name="jp_font", color=(0, 0, 0, 1), font_size= sp(20),
                                background_normal=self.bm_up, background_down=self.bm_down, bookmarked = True,
                                border=(0, 0, 0, 0))
                button.bind(on_press=lambda x,
                            id=i[0], type=categ: self.popup(type, id))
                button.bind(on_release=lambda x, button=button: self.change_color(button))
                self.buttons.append(button)
                if categ == "GRAMMAR":
                    self.ids.grammar_tab.add_widget(button)
                if categ == "VOCAB":
                    self.ids.vocab_tab.add_widget(button)
                if categ == "KANJI":
                    self.ids.kanji_tab.add_widget(button)
    
    def change_color(self, current_button):
        if current_button.bookmarked:
            current_button.background_normal = 'resources/Buttons/bm_picked.png'
        else:
            current_button.background_normal = 'resources/Buttons/rec_3_up.png'
        for button in self.buttons:
            if button.text != current_button.text:
                if button.bookmarked:
                    button.background_normal = 'resources/Buttons/bm_1_up.png'
                else:
                    button.background_normal = 'resources/Buttons/rec_1_up.png'

    def on_leave(self, *args):
        self.ids.grammar_tab.clear_widgets()
        self.ids.vocab_tab.clear_widgets()
        self.ids.kanji_tab.clear_widgets()

    def popup(self, type, ID):
        dh.pop_source = "contents"
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
    
    def to_bookmarks(self):
        self.manager.current = "booki"


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

    def initialize(self):
        self.label = "Item #" + str(dh.current+1) + "/10"
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()
        retrieve_query = "select * from " + dh.level + \
            "_GRAMMAR where ID = " + str(dh.contents[dh.current])
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

        dh.keys[dh.current] = self.ans

        if dh.answers[dh.current] == "a":
            self.ids.ga.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.gb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gc.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gd.background_normal = 'resources/Buttons/rec_1_up.png'
        elif dh.answers[dh.current] == "b":
            self.ids.gb.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.ga.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gc.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gd.background_normal = 'resources/Buttons/rec_1_up.png'
        elif dh.answers[dh.current] == "c":
            self.ids.gc.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.ga.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gd.background_normal = 'resources/Buttons/rec_1_up.png'
        elif dh.answers[dh.current] == "d":
            self.ids.gd.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.ga.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gc.background_normal = 'resources/Buttons/rec_1_up.png'
        else:
            self.ids.ga.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gc.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.gd.background_normal = 'resources/Buttons/rec_1_up.png'
        
        if dh.current == 0:
            self.ids.prev.disabled = True
        else:
            self.ids.prev.disabled = False
        if dh.first_screen == "signup" and dh.current == 0:
            if dh.level == "N5":
                dh.error = 12
            NoticePop().open()

    def on_pre_enter(self, *args):
        self.initialize()

    def ent_a(self):
        dh.answers[dh.current] = "a"
        self.ids.ga.background_normal = 'resources/Buttons/rec_3_up.png'
        self.ids.gb.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.gc.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.gd.background_normal = 'resources/Buttons/rec_1_up.png'

    def ent_b(self):
        dh.answers[dh.current] = "b"
        self.ids.ga.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.gb.background_normal = 'resources/Buttons/rec_3_up.png'
        self.ids.gc.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.gd.background_normal = 'resources/Buttons/rec_1_up.png'

    def ent_c(self):
        dh.answers[dh.current] = "c"
        self.ids.ga.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.gb.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.gc.background_normal = 'resources/Buttons/rec_3_up.png'
        self.ids.gd.background_normal = 'resources/Buttons/rec_1_up.png'

    def ent_d(self):
        dh.answers[dh.current] = "d"
        self.ids.ga.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.gb.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.gc.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.gd.background_normal = 'resources/Buttons/rec_3_up.png'

    def next_screen(self):
        dh.current += 1

        if dh.current == 10:
            if dh.first_screen == "signup":
                if dh.score < dh.passing_scores[dh.index]:
                    if dh.level == "N5":
                        dh.add_open_level("N5")
                    dh.current = 0
                    dh.level = ""
                    self.manager.current = "home"
                else:
                    if dh.level == "N5":
                        dh.add_open_level("N5")
                    if dh.level != "N1":
                        dh.index = dh.index + 1
                        dh.level = dh.difficulties[dh.index]
                        dh.add_open_level(dh.level)
                        dh.current = 0
                        new_contents()
                        if dh.level == "N4":
                            dh.error = 8
                        if dh.level == "N3":
                            dh.error = 9
                        if dh.level == "N2":
                            dh.error = 10
                        if dh.level == "N1":
                            dh.error = 11
                        self.initialize()
                    else:
                        self.manager.current = "home"
            else:
                self.manager.current = "end"
        else:
            self.manager.current = "vocabi"
    
    def prev_screen(self):
        dh.current -= 1

        self.manager.current = "kanjii"


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

    def initialize(self):
        self.label = "Item #" + str(dh.current + 1) +"/10"
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()
        if dh.level == "N5":
            retrieve_query = ("select WORD, KANJI, C_A, C_B, C_C, C_D, ANSWER from " + dh.level +
                              "_VOCAB where ID = " +
                              str(dh.contents[dh.current]))
            cursor.execute(retrieve_query)
        else:
            retrieve_query = ("select SENTENCE, KANJI, C_A, C_B, C_C, C_D, ANSWER from " + dh.level +
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

        dh.keys[dh.current] = self.ans

        if dh.answers[dh.current] == "a":
            self.ids.va.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.vb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vc.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vd.background_normal = 'resources/Buttons/rec_1_up.png'
        elif dh.answers[dh.current] == "b":
            self.ids.vb.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.va.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vc.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vd.background_normal = 'resources/Buttons/rec_1_up.png'
        elif dh.answers[dh.current] == "c":
            self.ids.vc.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.va.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vd.background_normal = 'resources/Buttons/rec_1_up.png'
        elif dh.answers[dh.current] == "d":
            self.ids.vd.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.va.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vc.background_normal = 'resources/Buttons/rec_1_up.png'
        else:
            self.ids.va.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vc.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.vd.background_normal = 'resources/Buttons/rec_1_up.png'

    def on_pre_enter(self, *args):
        self. initialize()
    
    def ent_a(self):
        dh.answers[dh.current] = "a"
        self.ids.va.background_normal = 'resources/Buttons/rec_3_up.png'
        self.ids.vb.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.vc.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.vd.background_normal = 'resources/Buttons/rec_1_up.png'

    def ent_b(self):
        dh.answers[dh.current] = "b"
        self.ids.va.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.vb.background_normal = 'resources/Buttons/rec_3_up.png'
        self.ids.vc.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.vd.background_normal = 'resources/Buttons/rec_1_up.png'

    def ent_c(self):
        dh.answers[dh.current] = "c"
        self.ids.va.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.vb.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.vc.background_normal = 'resources/Buttons/rec_3_up.png'
        self.ids.vd.background_normal = 'resources/Buttons/rec_1_up.png'

    def ent_d(self):
        dh.answers[dh.current] = "d"
        self.ids.va.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.vb.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.vc.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.vd.background_normal = 'resources/Buttons/rec_3_up.png'

    def next_screen(self):
        dh.current += 1
        self.manager.current = "kanjii"
    
    def prev_screen(self):
        dh.current -= 1
        self.manager.current = "grammari"


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

    def initialize(self):
        self.label = "Item #" + str(dh.current + 1) + "/10"
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()
        retrieve_query = "select * from " + dh.level + \
            "_KANJI where ID = " + str(dh.contents[dh.current])
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

        dh.keys[dh.current] = self.ans

        if dh.answers[dh.current] == "a":
            self.ids.ka.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.kb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kc.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kd.background_normal = 'resources/Buttons/rec_1_up.png'
        elif dh.answers[dh.current] == "b":
            self.ids.kb.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.ka.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kc.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kd.background_normal = 'resources/Buttons/rec_1_up.png'
        elif dh.answers[dh.current] == "c":
            self.ids.kc.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.ka.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kd.background_normal = 'resources/Buttons/rec_1_up.png'
        elif dh.answers[dh.current] == "d":
            self.ids.kd.background_normal = 'resources/Buttons/rec_3_up.png'
            self.ids.ka.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kc.background_normal = 'resources/Buttons/rec_1_up.png'
        else:
            self.ids.ka.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kb.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kc.background_normal = 'resources/Buttons/rec_1_up.png'
            self.ids.kd.background_normal = 'resources/Buttons/rec_1_up.png'

    def on_pre_enter(self, *args):
        self.initialize()


    def ent_a(self):
        dh.answers[dh.current] = "a"
        self.ids.ka.background_normal = 'resources/Buttons/rec_3_up.png'
        self.ids.kb.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.kc.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.kd.background_normal = 'resources/Buttons/rec_1_up.png'

    def ent_b(self):
        dh.answers[dh.current] = "b"
        self.ids.ka.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.kb.background_normal = 'resources/Buttons/rec_3_up.png'
        self.ids.kc.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.kd.background_normal = 'resources/Buttons/rec_1_up.png'

    def ent_c(self):
        dh.answers[dh.current] = "c"
        self.ids.ka.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.kb.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.kc.background_normal = 'resources/Buttons/rec_3_up.png'
        self.ids.kd.background_normal = 'resources/Buttons/rec_1_up.png'

    def ent_d(self):
        dh.answers[dh.current] = "d"
        self.ids.ka.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.kb.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.kc.background_normal = 'resources/Buttons/rec_1_up.png'
        self.ids.kd.background_normal = 'resources/Buttons/rec_3_up.png'

    def next_screen(self):
        dh.current += 1
        self.manager.current = "grammari"
    
    def prev_screen(self):
        dh.current -= 1
        self.manager.current = "vocabi"


class EndQuizz(Screen):
    score = StringProperty()
    button_up = './resources/Buttons/rec_2_up.png'
    button_down = './resources/Buttons/rec_2_down.png'
    border = './resources/Buttons/rec_4_up.png'
    back_up = './resources/Buttons/back_button_up.png'
    back_down = './resources/Buttons/back_button_down.png'

    def __init__(self, **kwargs):
        super(EndQuizz, self).__init__(**kwargs)
        self.rect = Rectangle()

    def on_pre_enter(self, **kwargs):
        conn = sqlite3.connect("Quizzes.db")
        cursor = conn.cursor()

        for i in range(10):
            grid_width = Window.width*0.9
            grid_layout = GridLayout(cols=6, size_hint=(None, None), width=grid_width)
            setattr(grid_layout, 'id', 'grid_layout_{}'.format(i))
            grid_layout.cols_minimum = {0: grid_width * 0.05, 
                                        1: grid_width * 0.2,
                                        2: grid_width * 0.3,
                                        3: grid_width * 0.2,
                                        4: grid_width * 0.2,
                                        5: grid_width * 0.05,}
            self.ids.review_buttons.add_widget(grid_layout)

            with grid_layout.canvas.before:
                Rectangle(source=self.button_up, pos=grid_layout.pos, size=grid_layout.size)

            grid_layout.bind(pos=self.update_background, size=self.update_background)

            anchor0 = AnchorLayout(anchor_x='center', anchor_y='center')
            grid_layout.add_widget(anchor0)

            image_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
            grid_layout.add_widget(image_anchor)

            if dh.keys[i] == dh.answers[i]:
                dh.score += 1
                image = Image(source='./resources/Buttons_2/CorrectButton.png', size_hint=(None, None),
                              width=grid_layout.height * 0.7, height=grid_layout.height * 0.7)
            else:
                image = Image(source='./resources/Buttons_2/WrongButton.png', size_hint=(None, None),
                              width=grid_layout.height * 0.7, height=grid_layout.height * 0.7)
            
            image_anchor.add_widget(image)

            anchor1 = AnchorLayout(anchor_x='center', anchor_y='center')
            item_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
            question_anchor = AnchorLayout(anchor_x='center', anchor_y='center')

            grid_layout.add_widget(anchor1)
            grid_layout.add_widget(item_anchor)
            grid_layout.add_widget(question_anchor)

            if i in (0, 3, 6, 9):
                retrieve_query = "select WORD from " + dh.level + \
                    "_GRAMMAR where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[0]
                    label = Label(text=button_text, font_name="jp_font", color=(0, 0, 0, 1), font_size=sp(20))
                    anchor1.add_widget(label)
                    item = Button(background_normal='./resources/Buttons_2/New_ViewItem.png',
                                    border=(0, 0, 0, 0),
                                    size_hint=(None, None), width=grid_width * 0.12, height=grid_layout.height * 0.8)
                    item.bind(
                        on_release=lambda x, id=dh.contents[i], type="grammar": self.popup(type, id))
                    question = Button(background_normal='./resources/Buttons_2/New_ViewQuestion.png',
                                    border=(0, 0, 0, 0),
                                    size_hint=(None, None), width=grid_width * 0.12, height=grid_layout.height * 0.8)
                    question.bind(
                        on_release=lambda x, id=dh.contents[i], index = i, type="grammar": self.question_pop(type, id, index))
                    item_anchor.add_widget(item)
                    question_anchor.add_widget(question)
            if i in (1, 4, 7):
                retrieve_query = "select KANJI from " + dh.level + \
                    "_VOCAB where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[0]
                    label = Label(text=button_text, font_name="jp_font", color=(0, 0, 0, 1), font_size=sp(20))
                    anchor1.add_widget(label)
                    item = Button(background_normal='./resources/Buttons_2/New_ViewItem.png',
                                    border=(0, 0, 0, 0),
                                    size_hint=(None, None), width=grid_width * 0.12, height=grid_layout.height * 0.8)
                    item.bind(
                        on_release=lambda x, id=dh.contents[i], type="vocab": self.popup(type, id))
                    question = Button(background_normal='./resources/Buttons_2/New_ViewQuestion.png',
                                    border=(0, 0, 0, 0),
                                    size_hint=(None, None), width=grid_width * 0.12, height=grid_layout.height * 0.8)
                    question.bind(
                        on_release=lambda x, id=dh.contents[i], index = i,type="vocab": self.question_pop(type, id, index))
                    item_anchor.add_widget(item)
                    question_anchor.add_widget(question)
            if i in (2, 5, 8):
                retrieve_query = "select KANJI from " + dh.level + \
                    "_KANJI where ID = " + str(dh.contents[i])
                cursor.execute(retrieve_query)
                contents = cursor.fetchall()
                for j in contents:
                    button_text = j[0]
                    label = Label(text=button_text, font_name="jp_font", color=(0, 0, 0, 1), font_size=sp(20))
                    anchor1.add_widget(label)
                    item = Button(background_normal='./resources/Buttons_2/New_ViewItem.png',
                                    border=(0, 0, 0, 0),
                                    size_hint=(None, None), width=grid_width * 0.12, height=grid_layout.height * 0.8)
                    item.bind(
                        on_release=lambda x, id=dh.contents[i], type="kanji": self.popup(type, id))
                    question = Button(background_normal='./resources/Buttons_2/New_ViewQuestion.png',
                                    border=(0, 0, 0, 0),
                                    size_hint=(None, None), width=grid_width * 0.12, height=grid_layout.height * 0.8)
                    question.bind(
                        on_release=lambda x, id=dh.contents[i], index = i, type="kanji": self.question_pop(type, id, index))
                    item_anchor.add_widget(item)
                    question_anchor.add_widget(question)
        conn.close()
        anchor2 = AnchorLayout(anchor_x='center', anchor_y='center')
        grid_layout.add_widget(anchor2)
        self.score = "Your score is " + str(dh.score) + "/10"

    def on_leave(self, *args):
        self.ids.review_buttons.clear_widgets()

    def popup(self, type, ID):
        dh.pop_source = "review"
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
    
    def question_pop(self, type, id, index):
        dh.current_id = id
        dh.pop_index = index
        print(dh.pop_index)
        if type == "grammar":
            pop = GrammarQ()
            pop.open()
        if type == "vocab":
                pop = VocabQ()
                pop.open()
        if type == "kanji":
            pop = KanjiQ()
            pop.open()
    
    def update_background(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Rectangle(source=self.button_up, pos=instance.pos, size=instance.size)


class Entry(Screen):
    message = "Thank you for signing up for Nihongo Wakaranai! To ensure a personalized learning experience, we kindly request you to complete an entry assessment. This assessment will determine your current proficiency level in Japanese and help us tailor the content to your needs. Rest assured that your assessment results will remain confidential. Begin your learning journey by tapping the start button below."


class WindowManager(ScreenManager):
    pass


tools_path = os.path.dirname("resources/")
icons_path1 = os.path.join(tools_path, 'komorebi-gothic-P.ttf')
icons_path2 = os.path.join(tools_path, 'VisbyRoundCF-DemiBold.otf')

LabelBase.register(name='jp_font',
                   fn_regular=icons_path1)
LabelBase.register(name='en_font',
                   fn_regular=icons_path2)


class MainApp(MDApp):
    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            pop = ExitPop()
            pop.open()
            return True

    def build(self):
        kv = Builder.load_file("my.kv")
        return kv


if __name__ == "__main__":
    MainApp().run()
