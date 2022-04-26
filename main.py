from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.clock import Clock
import time

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
    pass


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
    pass


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
