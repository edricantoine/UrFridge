from abc import ABC
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.button import MDFlatButton
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
import Backend.Ingredient as Ing
import Backend.Application as Apple
import Backend.Fridge as Frg


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
        self.clearify()

    def clearify(self):
        self.ids.frScroll.clear_widgets()
        self.ids.fzScroll.clear_widgets()
        self.ids.pnScroll.clear_widgets()
        self.ids.msScroll.clear_widgets()
        self.refreshFridge()
        self.refreshFreezer()
        self.refreshPantry()
        self.refreshMisc()

    def refreshFridge(self):
        self.ids.frScroll.clear_widgets()
        for i in self.app.fridge.getIngredient():
            self.ids.frScroll.add_widget(FridgeDisplay(i))
        self.ids.frScroll.add_widget(AddIngredientButton(self.app.fridge, self, "fridge"))

    def refreshFreezer(self):
        self.ids.fzScroll.clear_widgets()
        for i in self.app.freezer.getIngredient():
            self.ids.fzScroll.add_widget(FridgeDisplay(i))
        self.ids.fzScroll.add_widget(AddIngredientButton(self.app.freezer, self, "freezer"))

    def refreshPantry(self):
        self.ids.pnScroll.clear_widgets()
        for i in self.app.pantry.getIngredient():
            self.ids.pnScroll.add_widget(FridgeDisplay(i))
        self.ids.pnScroll.add_widget(AddIngredientButton(self.app.pantry, self, "pantry"))

    def refreshMisc(self):
        self.ids.msScroll.clear_widgets()
        for i in self.app.misc.getIngredient():
            self.ids.msScroll.add_widget(FridgeDisplay(i))
        self.ids.msScroll.add_widget(AddIngredientButton(self.app.misc, self, "misc"))


class WindowManager(ScreenManager):
    pass


class FridgeDisplay(MDCard):
    def __init__(self, ingredient: Ing.Ingredient, **kwargs):
        super().__init__(**kwargs)
        self.ids.fDisplayLabel.text = ingredient.getName()
        self.ids.fAmtLabel.text = str(ingredient.getQuant()) + " " + ingredient.getUnit()


class AddIngredientButton(MDFloatingActionButton):
    fridge: Frg.Fridge
    ms: MainScreen
    type: str

    def refresh(self):
        if self.type == "fridge":
            self.ms.refreshFridge()
        elif self.type == 'freezer':
            self.ms.refreshFreezer()
        elif self.type == 'pantry':
            self.ms.refreshPantry()
        elif self.type == 'misc':
            self.ms.refreshMisc()

    def __init__(self, f: Frg.Fridge, ms: MainScreen, type: str, **kwargs):
        super().__init__(**kwargs)
        self.fridge = f
        self.ms = ms
        self.type = type


class AddIngredientDialog(MDDialog):
    aap = None

    def __init__(self, schlapp: Apple.Application, **kwargs):
        super().__init__(**kwargs)
        self.aap = schlapp


class AddIngredientContent(BoxLayout):
    aap = None

    def __init__(self, schlapp: Apple.Application, **kwargs):
        super().__init__(**kwargs)
        self.aap = schlapp


class Main(MDApp):
    app = None
    dialog = None

    def showAddDialog(self):
        if not self.dialog:
            self.dialog = AddIngredientDialog(self.app, type="custom",
                                              title="New Ingredient", content_cls=AddIngredientContent(self.app))
        self.dialog.open()

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
