from abc import ABC
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.uix.card import MDCard
import Backend.Ingredient as Ing
import Backend.Application as Apple


class MainScreen(Screen):
    app = None

    def __init__(self, aap: Apple.Application, **kw):
        super().__init__(**kw)
        self.app = aap
        self.app.fridge.addIngredient("Paprika", 1.0, "tsp")
        self.app.fridge.addIngredient("Watermelon", 1.0, "melon(s)")
        self.app.freezer.addIngredient("Blueberry", 10.0, "berry(s)")
        self.app.freezer.addIngredient("Cookie", 10.0, "package(s)")
        self.app.pantry.addIngredient("Beef", 1.0, "steak(s)")
        self.app.pantry.addIngredient("Pork", 1.0, "chop(s)")
        self.app.misc.addIngredient("Ciabatta", 1.0, "loaf")
        self.app.misc.addIngredient("B R E A D", 1.0, "loaf")
        self.addFridgeDisplays()

    def addFridgeDisplays(self):
        for i in self.app.fridge.getIngredient():
            self.ids.frScroll.add_widget(FridgeDisplay(i))

        for i in self.app.freezer.getIngredient():
            self.ids.fzScroll.add_widget(FridgeDisplay(i))

        for i in self.app.pantry.getIngredient():
            self.ids.pnScroll.add_widget(FridgeDisplay(i))

        for i in self.app.misc.getIngredient():
            self.ids.msScroll.add_widget(FridgeDisplay(i))

    pass


class WindowManager(ScreenManager):
    pass


class FridgeDisplay(MDCard):
    def __init__(self, ingredient: Ing.Ingredient, **kwargs):
        super().__init__(**kwargs)
        self.ids.fDisplayLabel.text = ingredient.getName()
        self.ids.fAmtLabel.text = str(ingredient.getQuant()) + " " + ingredient.getUnit()


class Main(MDApp):
    app = None

    def build(self):
        self.app = Apple.Application()
        self.theme_cls.primary_palette = "Green"
        sm = ScreenManager()
        sm.add_widget(MainScreen(self.app, name="Main Screen"))

        return sm


if __name__ == '__main__':
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')
    Window.size = (350, 740)
    app = Main()
    app.run()
