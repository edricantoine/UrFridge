from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from jnius import autoclass
import Backend.Ingredient as Ing
import Backend.Application as Apple
import Backend.Fridge as Frg
import http.client as httplib


def check_connectivity():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()


class MainScreen(Screen):
    app = None

    def __init__(self, aap: Apple.Application, **kw):
        super().__init__(**kw)
        self.app = aap
        self.clearify()
        self.ids.botNav.switch_tab("home")

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
            self.ids.frScroll.add_widget(FridgeDisplay(i, self.app.getFridge(), self))
        self.ids.frScroll.add_widget(AddIngredientButtonFr(self.app.fridge, self, "fridge"))
        self.ids.frScroll.add_widget(NothingThereLabel())

    def refreshFreezer(self):
        self.ids.fzScroll.clear_widgets()
        for i in self.app.freezer.getIngredient():
            self.ids.fzScroll.add_widget(FridgeDisplay(i, self.app.getFreezer(), self))
        self.ids.fzScroll.add_widget(AddIngredientButtonFz(self.app.freezer, self, "freezer"))
        self.ids.fzScroll.add_widget(NothingThereLabel())

    def refreshPantry(self):
        self.ids.pnScroll.clear_widgets()
        for i in self.app.pantry.getIngredient():
            self.ids.pnScroll.add_widget(FridgeDisplay(i, self.app.getPantry(), self))
        self.ids.pnScroll.add_widget(AddIngredientButtonPn(self.app.pantry, self, "pantry"))
        self.ids.pnScroll.add_widget(NothingThereLabel())

    def refreshMisc(self):
        self.ids.msScroll.clear_widgets()
        for i in self.app.misc.getIngredient():
            self.ids.msScroll.add_widget(FridgeDisplay(i, self.app.getMisc(), self))
        self.ids.msScroll.add_widget(AddIngredientButtonMs(self.app.misc, self, "misc"))
        self.ids.msScroll.add_widget(NothingThereLabel())


class WindowManager(ScreenManager):
    pass


class FridgeDisplay(MDCard):
    ing: Ing.Ingredient
    frg = Frg.Fridge
    ms = MainScreen

    def __init__(self, ingredient: Ing.Ingredient, fridge: Frg.Fridge, ms: MainScreen, **kwargs):
        super().__init__(**kwargs)
        self.ing = ingredient
        self.frg = fridge
        self.ms = ms
        self.ids.fDisplayLabel.text = ingredient.getName()
        self.ids.fAmtLabel.text = str(ingredient.getQuant()) + " " + ingredient.getUnit()

    def deletus_ingredient(self):
        self.frg.removeIngredients(self.ing.getName(), self.ing.getQuant())


class AddIngredientButtonFr(MDFloatingActionButton):
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


class AddIngredientButtonFz(MDFloatingActionButton):
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


class AddIngredientButtonPn(MDFloatingActionButton):
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


class AddIngredientButtonMs(MDFloatingActionButton):
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
    ferg = None

    def __init__(self, schlapp: Frg.Fridge, **kwargs):
        super().__init__(**kwargs)
        self.ferg = schlapp


class EditIngredientDialog(MDDialog):
    pass


class EditIngredientContent(BoxLayout):
    ferg: Frg.Fridge
    ms: MainScreen

    def __init__(self, ferg: Frg.Fridge, mss: MainScreen, **kwargs):
        super().__init__(**kwargs)
        self.ferg = ferg
        self.ms = mss


class AddIngredientContent(BoxLayout):
    aap = Frg.Fridge
    ms: MainScreen

    def __init__(self, ferg: Frg.Fridge, mss: MainScreen, **kwargs):
        super().__init__(**kwargs)
        self.aap = ferg
        self.ms = mss

    def readInput(self):
        name = self.ids.ingName.text
        amount = self.ids.ingAmt.text
        unit = self.ids.ingUnit.text
        if name != "" and amount != "" and unit != "" and len(name) <= 10 and len(amount) <= 10 and len(unit) <= 10:
            self.aap.addIngredient(name, float(amount), unit)
            self.ms.clearify()
            self.ids.ingName.text = ""
            self.ids.ingAmt.text = ""
            self.ids.ingUnit.text = ""
        else:
            toast('One or more fields are invalid.')


class NothingThereLabel(MDLabel):
    def __draw_shadow__(self, origin, end, context=None):
        pass


class InfoLabel(MDLabel):
    def __draw_shadow__(self, origin, end, context=None):
        pass


class Main(MDApp):
    app = None
    dialog = None
    sm = None

    def dialog_close(self):
        self.dialog.dismiss(force=True)

    def showEditDialogFr(self):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="New Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen")))
        self.dialog.open()

    def showEditDialogFz(self):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="New Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen")))
        self.dialog.open()

    def showEditDialogPn(self):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="New Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen")))
        self.dialog.open()

    def showEditDialogMs(self):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="New Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen")))
        self.dialog.open()

    def showAddDialogFrg(self):
        self.dialog = AddIngredientDialog(self.app.getFridge(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app.getFridge(),
                                                                           self.sm.get_screen("Main Screen")))
        self.dialog.open()

    def showAddDialogFrz(self):
        self.dialog = AddIngredientDialog(self.app.getFreezer(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app.getFreezer(),
                                                                           self.sm.get_screen("Main Screen")))
        self.dialog.open()

    def showAddDialogPn(self):
        self.dialog = AddIngredientDialog(self.app.getPantry(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app.getPantry(),
                                                                           self.sm.get_screen("Main Screen")))
        self.dialog.open()

    def showAddDialogMs(self):
        self.dialog = AddIngredientDialog(self.app.getMisc(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app.getMisc(),
                                                                           self.sm.get_screen("Main Screen")))
        self.dialog.open()

    def build(self):
        self.app = Apple.Application()
        self.theme_cls.primary_palette = "Green"
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(self.app, name="Main Screen"))
        if check_connectivity():
            print("Connected!")
        else:
            print("Not connected.")
        return self.sm


if __name__ == '__main__':
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')
    Window.size = (350, 740)
    app = Main()
    app.run()
