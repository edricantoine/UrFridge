from kivy.uix.screenmanager import Screen

from backend import Application as Apple
from ui.LoginLayout import LoginLayout


class LoginScreen(Screen):
    aap = None

    def __init__(self, apple: Apple.Application, app, **kw):
        super().__init__(**kw)
        self.aap = apple
        self.app = app
        self.ids.loginGrid.add_widget(LoginLayout(self.aap, self.app))
