from abc import ABC
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import Backend.Application as Apple


class MainScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class Main(MDApp):
    app = None

    def build(self):
        self.app = Apple.Application()
        self.theme_cls.primary_palette = "Green"
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="Main Screen"))

        return sm


if __name__ == '__main__':
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')
    Window.size = (350, 740)
    app = Main()
    app.run()
