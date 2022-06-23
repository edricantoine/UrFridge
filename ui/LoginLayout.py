from kivy.uix.gridlayout import GridLayout

from backend import Application as Apple


class LoginLayout(GridLayout):
    aap = None

    def __init__(self, apple: Apple.Application, app, **kwargs):
        super().__init__(**kwargs)
        self.aap = apple
        self.app = app

    def login(self, id_name: str):
        self.ids.idName.text = ""
        self.app.login(id_name)