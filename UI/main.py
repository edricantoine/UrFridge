import codecs
import Backend.recipeGrabber as Grab
from kivy.app import App
from kivy.uix.label import Label


class Main(App):
    def build(self):
        label = Label(text="Testing",
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        grb = Grab.RecipeGrabber(["cheese", "bacon"], 1000)

        return label


if __name__ == '__main__':
    app = Main()
    app.run()
