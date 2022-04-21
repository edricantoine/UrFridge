from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import Backend.Application as Apple


class MainScreen(Screen):
    app = None

    def __init__(self, aap: Apple.Application, **kw):
        super().__init__(**kw)
        self.app = aap

    def printFridges(self):
        for f in self.app.getFridges():
            print(f.getName())


class createFridgeScreen(Screen):
    app = None

    def attemptAddFridge(self, name):
        if self.app.addFridge(name):
            return "Fridge successfully added!"
        else:
            return "Invalid fridge name."

    def __init__(self, aap: Apple.Application, **kw):
        super().__init__(**kw)
        self.app = aap

    pass


class WindowManager(ScreenManager):
    pass


class selectFridgeScreen(Screen):
    pass


class Main(App):
    app = None

    def build(self):
        self.app = Apple.Application()
        sm = ScreenManager()
        sm.add_widget(MainScreen(self.app, name="Main Screen"))
        sm.add_widget(createFridgeScreen(self.app, name="Create Fridge"))
        return sm


if __name__ == '__main__':
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')
    app = Main()
    app.run()
