from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup
from kivy.clock import Clock
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
    pass


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
    pass


class VocabItem(Screen):
    pass


class KanjiItem(Screen):
    pass


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
    pass


kv = Builder.load_file("my.kv")

LabelBase.register(name='komorebi',
                   fn_regular='resources/komorebi-gothic-P.ttf')


class MainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MainApp().run()
