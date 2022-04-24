from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import time

class LoadingScreen(Screen):
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


kv = Builder.load_file("my.kv", encoding='utf8')


class MainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MainApp().run()