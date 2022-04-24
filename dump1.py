from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import time


class LoadingScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class DifficultySelection(Screen):
    pass


class BookmarkCategories(Screen):
    pass


class BookmarkedItems(Screen):
    pass


class Settings(Screen):
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


UI = Builder.load_file("my.kv")


class MainApp(App):
    def build(self):
        return UI


if __name__ == "__main__":
    MainApp().run()
