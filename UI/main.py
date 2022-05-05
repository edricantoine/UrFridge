from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from decimal import *
from kivy.storage.jsonstore import JsonStore

import Backend.Ingredient as Ing
import Backend.Application as Apple
import Backend.Fridge as Frg
import http.client as httplib


# Main class for screens + custom widgets

def check_connectivity():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()


# The main screen, with the bottom navigation panels + their contents

class MainScreen(Screen):
    app = None

    def __init__(self, aap: Apple.Application, **kw):
        super().__init__(**kw)
        self.app = aap
        self.clearify()
        self.ids.botNav.switch_tab("home")

    # clears scrollpanes and refreshes ingredient UI for all four fridges

    def clearify(self):
        self.ids.frScroll.clear_widgets()
        self.ids.fzScroll.clear_widgets()
        self.ids.pnScroll.clear_widgets()
        self.ids.msScroll.clear_widgets()
        self.refreshFridge()
        self.refreshFreezer()
        self.refreshPantry()
        self.refreshMisc()

    # clears scrollpanes and refreshes ingredient UI for fridge

    def refreshFridge(self):
        self.ids.frScroll.clear_widgets()
        for i in self.app.fridge.getIngredient():
            self.ids.frScroll.add_widget(FridgeDisplay(i, self.app.getFridge(), self))
        self.ids.frScroll.add_widget(AddIngredientButtonFr(self.app.fridge, self, "fridge"))
        self.ids.frScroll.add_widget(NothingThereLabel())

    # clears scrollpanes and refreshes ingredient UI for freezer
    def refreshFreezer(self):
        self.ids.fzScroll.clear_widgets()
        for i in self.app.freezer.getIngredient():
            self.ids.fzScroll.add_widget(FridgeDisplay(i, self.app.getFreezer(), self))
        self.ids.fzScroll.add_widget(AddIngredientButtonFz(self.app.freezer, self, "freezer"))
        self.ids.fzScroll.add_widget(NothingThereLabel())

    # clears scrollpanes and refreshes ingredient UI for pantry
    def refreshPantry(self):
        self.ids.pnScroll.clear_widgets()
        for i in self.app.pantry.getIngredient():
            self.ids.pnScroll.add_widget(FridgeDisplay(i, self.app.getPantry(), self))
        self.ids.pnScroll.add_widget(AddIngredientButtonPn(self.app.pantry, self, "pantry"))
        self.ids.pnScroll.add_widget(NothingThereLabel())

    # clears scrollpanes and refreshes ingredient UI for misc. section
    def refreshMisc(self):
        self.ids.msScroll.clear_widgets()
        for i in self.app.misc.getIngredient():
            self.ids.msScroll.add_widget(FridgeDisplay(i, self.app.getMisc(), self))
        self.ids.msScroll.add_widget(AddIngredientButtonMs(self.app.misc, self, "misc"))
        self.ids.msScroll.add_widget(NothingThereLabel())


# holds all screens in app
class WindowManager(ScreenManager):
    pass


# the MDCard that holds ingredient name + buttons for editing ingredient
class FridgeDisplay(MDCard):
    ing: Ing.Ingredient
    frg = Frg.Fridge
    ms = MainScreen

    # handles checkbox changing state
    def on_checkbox(self, checkbox, value):
        if value:
            self.ing.setSelected(True)
            print("Ingredient " + self.ing.getName() + " is now selected")
        else:
            self.ing.setSelected(False)
            print("Ingredient " + self.ing.getName() + " is now deselected")

    # calls the appropriate editing dialog
    def callEdit(self):
        if self.frg.getName() == "Fridge":
            app.showEditDialogFr(self.ing)
        elif self.frg.getName() == "Freezer":
            app.showEditDialogFz(self.ing)
        elif self.frg.getName() == "Pantry":
            app.showEditDialogPn(self.ing)
        else:
            app.showEditDialogMs(self.ing)

    def __init__(self, ingredient: Ing.Ingredient, fridge: Frg.Fridge, ms: MainScreen, **kwargs):
        super().__init__(**kwargs)
        self.ing = ingredient
        self.frg = fridge
        self.ms = ms
        self.ids.fDisplayLabel.text = ingredient.getName()
        self.ids.fAmtLabel.text = str(ingredient.getQuant()) + " " + ingredient.getUnit()

    # deletes an ingredient
    def deletus_ingredient(self):
        self.frg.removeIngredients(self.ing.getName(), self.ing.getQuant())


# Button that adds an ingredient (fridge)

class AddIngredientButtonFr(MDFloatingActionButton):
    fridge: Frg.Fridge
    ms: MainScreen
    type: str

    # calls appropriate refresh method of main screen
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


# Same as above, but for freezer
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


# Same as above, but for pantry
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


# Same as above, but for misc.
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


# The dialog that helps to add an ingredient
class AddIngredientDialog(MDDialog):
    ferg = None

    def __init__(self, schlapp: Frg.Fridge, **kwargs):
        super().__init__(**kwargs)
        self.ferg = schlapp


# The dialog that helps to edit an ingredient amount
class EditIngredientDialog(MDDialog):
    pass


# The content of the EditIngredientDialog
class EditIngredientContent(BoxLayout):
    ferg: Frg.Fridge
    ms: MainScreen
    ing: Ing.Ingredient

    # Reads the input of the content's textbox, and edits an ingredient amount appropriately
    def readInput(self):
        op = self.ids.ddItem.current_item
        amount = self.ids.newAmount.text
        if amount == "":
            toast("Amount field was invalid.")

        if op == "Add":
            self.ferg.increaseIngredient(self.ing.getName(), Decimal(amount))
        elif op == "Remove":
            self.ferg.removeIngredients(self.ing.getName(), Decimal(amount))
        else:
            toast("Invalid command issued.")

        self.ms.clearify()
        self.ids.newAmount.text = ""

    def __init__(self, ferg: Frg.Fridge, mss: MainScreen, ing: Ing.Ingredient, **kwargs):
        super().__init__(**kwargs)
        self.ferg = ferg
        self.ms = mss
        self.ing = ing


# The content of the AddIngredientDialog
class AddIngredientContent(BoxLayout):
    aap = Frg.Fridge
    ms: MainScreen

    def __init__(self, ferg: Frg.Fridge, mss: MainScreen, **kwargs):
        super().__init__(**kwargs)
        self.aap = ferg
        self.ms = mss

    # Reads the input of the content's textboxes, adds an ingredient or shows an error appropriately
    def readInput(self):
        name = self.ids.ingName.text
        amount = self.ids.ingAmt.text
        unit = self.ids.ingUnit.text
        if name != "" and amount != "" and unit != "" and len(name) <= 10 and len(amount) <= 10 and len(unit) <= 10:

            if self.aap.addIngredient(name, Decimal(amount), unit):
                self.ms.clearify()
                self.ids.ingName.text = ""
                self.ids.ingAmt.text = ""
                self.ids.ingUnit.text = ""
            else:
                toast("An ingredient with that name already exists.")
        else:
            toast('One or more fields are invalid.')


# Label that instructs user to use the "+" button
class NothingThereLabel(MDLabel):
    def __draw_shadow__(self, origin, end, context=None):
        pass


# Not actually sure what this is, but whatever
class InfoLabel(MDLabel):
    def __draw_shadow__(self, origin, end, context=None):
        pass


# The class that represents the whole app

class Main(MDApp):
    app = None
    dialog = None
    sm = None
    menu = None
    frStore = None
    fzStore = None
    pnStore = None
    msStore = None

    def saveToJson(self):
        self.frStore.clear()
        self.fzStore.clear()
        self.pnStore.clear()
        self.msStore.clear()

        for ing in self.app.getFridge().getIngredient():
            self.frStore.put(ing.getName(), name=ing.getName(), quant=str(ing.getQuant()), unit=ing.getUnit(),
                             sel=ing.getSelected())

        for ing in self.app.getFreezer().getIngredient():
            self.fzStore.put(ing.getName(), name=ing.getName(), quant=str(ing.getQuant()), unit=ing.getUnit(),
                             sel=ing.getSelected())

        for ing in self.app.getPantry().getIngredient():
            self.pnStore.put(ing.getName(), name=ing.getName(), quant=str(ing.getQuant()), unit=ing.getUnit(),
                             sel=ing.getSelected())

        for ing in self.app.getMisc().getIngredient():
            self.msStore.put(ing.getName(), name=ing.getName(), quant=str(ing.getQuant()), unit=ing.getUnit(),
                             sel=ing.getSelected())

    def loadFromJson(self):

        for j in self.frStore:
            print(j)
            name = self.frStore[j]['name']
            quant = Decimal(self.frStore[j]['quant'])
            unit = self.frStore[j]['unit']
            self.app.getFridge().addIngredient(name, quant, unit)

        for j in self.fzStore:
            name = self.fzStore[j]['name']
            quant = Decimal(self.fzStore[j]['quant'])
            unit = self.fzStore[j]['unit']
            self.app.getFreezer().addIngredient(name, quant, unit)

        for j in self.pnStore:
            name = self.pnStore[j]['name']
            quant = Decimal(self.pnStore[j]['quant'])
            unit = self.pnStore[j]['unit']
            self.app.getPantry().addIngredient(name, quant, unit)

        for j in self.msStore:
            name = self.msStore[j]['name']
            quant = Decimal(self.msStore[j]['quant'])
            unit = self.msStore[j]['unit']
            self.app.getMisc().addIngredient(name, quant, unit)

    # closes current dialog
    def dialog_close(self):
        self.dialog.dismiss(force=True)

    # shows dialog for editing fridge
    def showEditDialogFr(self, ingredient: Ing.Ingredient):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             ingredient))
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing freezer
    def showEditDialogFz(self, ingredient: Ing.Ingredient):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             ingredient))
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing pantry
    def showEditDialogPn(self, ingredient: Ing.Ingredient):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             ingredient))
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing misc
    def showEditDialogMs(self, ingredient: Ing.Ingredient):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             ingredient))
        self.set_menu()
        self.dialog.open()

    # shows dialog for adding ingredient to fridge
    def showAddDialogFrg(self):
        self.dialog = AddIngredientDialog(self.app.getFridge(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app.getFridge(),
                                                                           self.sm.get_screen("Main Screen")))
        self.dialog.open()

    # shows dialog for adding ingredient to freezer
    def showAddDialogFrz(self):
        self.dialog = AddIngredientDialog(self.app.getFreezer(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app.getFreezer(),
                                                                           self.sm.get_screen("Main Screen")))
        self.dialog.open()

    # shows dialog for adding ingredient to pantry
    def showAddDialogPn(self):
        self.dialog = AddIngredientDialog(self.app.getPantry(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app.getPantry(),
                                                                           self.sm.get_screen("Main Screen")))
        self.dialog.open()

    # shows dialog for adding ingredient to misc.
    def showAddDialogMs(self):
        self.dialog = AddIngredientDialog(self.app.getMisc(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app.getMisc(),
                                                                           self.sm.get_screen("Main Screen")))
        self.dialog.open()

    # sets current menu to one for choosing whether to add/remove when editing ingredient amount
    def set_menu(self):
        mItems = [{
            'viewclass': 'OneLineListItem',
            'text': "Add",
            'on_release': lambda x='Add': self.set_item(x)
        },
            {
                'viewclass': 'OneLineListItem',
                'text': "Remove",
                'on_release': lambda x='Remove': self.set_item(x)
            }]
        self.menu = MDDropdownMenu(caller=self.dialog.content_cls.ids.ddItem,
                                   items=mItems, width_mult=2)
        self.menu.bind()

    # sets item for dropdown menu
    def set_item(self, arg):
        self.dialog.content_cls.ids.ddItem.set_item(arg)
        self.menu.dismiss()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = Apple.Application()
        self.frStore = JsonStore('fridge.json')
        self.fzStore = JsonStore('freezer.json')
        self.pnStore = JsonStore('pantry.json')
        self.msStore = JsonStore('misc.json')
        self.loadFromJson()

    # build + run app
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(self.app, name="Main Screen"))

        if check_connectivity():
            print("Connected!")
        else:
            print("Not connected.")



        return self.sm


if __name__ == '__main__':
    wx = 350
    wy = 740
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')

    app = Main()
    app.run()
