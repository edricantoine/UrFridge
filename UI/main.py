from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout


class myLayout(FloatLayout):
    pass


class Main(App):
    grb = None

    def build(self):
        return myLayout()


if __name__ == '__main__':
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')
    app = Main()
    app.run()
