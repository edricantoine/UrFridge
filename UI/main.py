from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
import Backend.Application as Apple
import Backend.Fridge as Frg


class MainScreen(Screen):
    pass



class WindowManager(ScreenManager):
    pass


class RoundedButton(Button):
    pass


class SelectButton(Button):
    pass


class Main(App):
    app = None

    def build(self):
        self.app = Apple.Application()
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="Main Screen"))

        return sm


if __name__ == '__main__':
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')
    app = Main()
    app.run()
