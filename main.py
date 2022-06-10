import functools
import sys

from kivy.utils import rgba
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import ThreeLineListItem
from kivymd.toast import toast
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.card import MDCard
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.menu import MDDropdownMenu
from decimal import *
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
import sqlite3
import Backend.Ingredient as Ing
import Backend.Application as Apple
import Backend.Fridge as Frg
import Backend.Recipe as Rec
import http.client as httplib
import os

app_path = os.path.dirname(os.path.abspath(__file__))
squirrel = sqlite3.connect(os.path.join(app_path, 'userdata.db'), detect_types=sqlite3.PARSE_DECLTYPES)
c = squirrel.cursor()


# Main class for screens + custom widgets

# Gets an absolute path to a resource (copied off of StackOverflow lmao)
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Makes decimals not fucky
def adapt_decimal(d):
    return str(d)


# see above
def convert_decimal(s):
    return Decimal(s.decode('ascii'))


# Register the adapter
sqlite3.register_adapter(Decimal, adapt_decimal)

# Register the converter
sqlite3.register_converter("decimal", convert_decimal)


# Returns true if connected to internet, false otherwise
def check_connectivity():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()


# Class representing the 'login' screen
class LoginScreen(Screen):
    app = None

    def __init__(self, apple: Apple.Application, **kw):
        super().__init__(**kw)
        self.app = apple
        self.ids.loginGrid.add_widget(LoginLayout(self.app))


# Class holding all the stuff in the login screen
class LoginLayout(GridLayout):
    app = None

    def __init__(self, apple: Apple.Application, **kwargs):
        super().__init__(**kwargs)
        self.app = apple


class LoadingScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self):
        app.app.getRecipeFromSelectedIngredients(app.numToGrab, None)
        app.sm.get_screen("Recipe List").initializeFromRecipesList(app.app.getRecipes())
        app.sm.current = 'Recipe List'


# The main screen, with the bottom navigation panels + their contents

class MainScreen(Screen):
    app = None

    # We do a minuscule amount of initializing
    def __init__(self, aap: Apple.Application, **kw):
        super().__init__(**kw)
        self.app = aap
        self.clearify()
        self.ids.botNav.switch_tab("home")
        self.ids.msBb.add_widget(AddIngredientButtonMs(self.app.misc, self, "misc"))
        self.ids.msBox.add_widget(NothingThereLabel())
        self.ids.msBox.add_widget(
            MDLabel(halign='center', font_name=resource_path("DMSANS.ttf"), text='YourFridge © Edric '
                                                                                 'Antoine 2022',
                    theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))
        self.ids.pnBb.add_widget(AddIngredientButtonPn(self.app.pantry, self, "pantry"))
        self.ids.pnBox.add_widget(NothingThereLabel())
        self.ids.pnBox.add_widget(
            MDLabel(halign='center', font_name=resource_path("DMSANS.ttf"), text='YourFridge © Edric '
                                                                                 'Antoine 2022',
                    theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))
        self.ids.fzBb.add_widget(AddIngredientButtonFz(self.app.freezer, self, "freezer"))
        self.ids.fzBox.add_widget(NothingThereLabel())
        self.ids.fzBox.add_widget(
            MDLabel(halign='center', font_name=resource_path("DMSANS.ttf"), text='YourFridge © Edric '
                                                                                 'Antoine 2022',
                    theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))
        self.ids.frBb.add_widget(AddIngredientButtonFr(self.app.fridge, self, "fridge"))
        self.ids.frBox.add_widget(NothingThereLabel())
        self.ids.frBox.add_widget(
            MDLabel(halign='center', font_name=resource_path("DMSANS.ttf"), text='YourFridge © Edric '
                                                                                 'Antoine 2022',
                    theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))

    # clears scrollpanes and refreshes ingredient UI for all four fridges

    def clearify(self):

        self.refreshFridge()
        self.refreshFreezer()
        self.refreshPantry()
        self.refreshMisc()

    # clears scrollpanes and refreshes ingredient UI for fridge

    def refreshFridge(self):
        self.ids.frScroll.clear_widgets()
        for i in self.app.fridge.getIngredient():
            self.ids.frScroll.add_widget(FridgeDisplay(i, self.app.getFridge(), self))

    # clears scrollpanes and refreshes ingredient UI for freezer
    def refreshFreezer(self):
        self.ids.fzScroll.clear_widgets()
        for i in self.app.freezer.getIngredient():
            self.ids.fzScroll.add_widget(FridgeDisplay(i, self.app.getFreezer(), self))

    # clears scrollpanes and refreshes ingredient UI for pantry
    def refreshPantry(self):
        self.ids.pnScroll.clear_widgets()
        for i in self.app.pantry.getIngredient():
            self.ids.pnScroll.add_widget(FridgeDisplay(i, self.app.getPantry(), self))

    # clears scrollpanes and refreshes ingredient UI for misc. section
    def refreshMisc(self):
        self.ids.msScroll.clear_widgets()
        for i in self.app.misc.getIngredient():
            self.ids.msScroll.add_widget(FridgeDisplay(i, self.app.getMisc(), self))

    # Stuff that happens whenever we re-enter the MainScreen
    def on_enter(self):
        self.clearify()
        self.refresh_homepage()

    # Refreshes the homepage - will definitely have more stuff added to this lol
    def refresh_homepage(self):
        self.ids.welcomeLabel.text = "Hello, " + self.app.getId() + "!"
        self.ids.selectedGrid.clear_widgets()
        for i in self.app.getSelectedIngredients():
            self.ids.selectedGrid.add_widget(SpecialLabel(text=i.getName()))
        print("Homepage refreshed.")


# holds all screens in app
class WindowManager(ScreenManager):
    pass


class SpecialLabel(MDLabel):
    pass


def compareName(r1: Rec.Recipe, r2: Rec.Recipe):
    if r1.getName() < r2.getName():
        return -1
    elif r1.getName() > r2.getName():
        return 1
    else:
        return 0


def compareCals(r1: Rec.Recipe, r2: Rec.Recipe):
    if r1.getCalories() < r2.getCalories():
        return -1
    elif r1.getCalories() > r2.getCalories():
        return 1
    else:
        return 0


def compareMissed(r1: Rec.Recipe, r2: Rec.Recipe):
    if r1.getMCount() < r2.getMCount():
        return -1
    elif r1.getMCount() > r2.getMCount():
        return 1
    else:
        return 0


class RecipeViewScreen(Screen):
    recipes = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.recipes = []

    def initializeFromRecipesList(self, r_list):
        self.recipes = r_list
        for r in self.recipes:
            self.ids.viewScroll.add_widget(RecipeDisplay(r))

    def sortByName(self):
        self.ids.viewScroll.clear_widgets()
        self.recipes = sorted(self.recipes, key=functools.cmp_to_key(compareName))
        for r in self.recipes:
            self.ids.viewScroll.add_widget(RecipeDisplay(r))

    def sortByCals(self):
        self.ids.viewScroll.clear_widgets()
        self.recipes = sorted(self.recipes, key=functools.cmp_to_key(compareCals))
        for r in self.recipes:
            self.ids.viewScroll.add_widget(RecipeDisplay(r))

    def sortByMissed(self):
        self.ids.viewScroll.clear_widgets()
        self.recipes = sorted(self.recipes, key=functools.cmp_to_key(compareCals))
        for r in self.recipes:
            self.ids.viewScroll.add_widget(RecipeDisplay(r))


class RecipeDisplay(MDCardSwipe):
    rec: Rec.Recipe

    def toastPlaceholder(self, tlli):
        toast("Coming soon: " + tlli.text)

    def __init__(self, rec: Rec.Recipe, **kwargs):
        super().__init__(**kwargs)
        self.rec = rec
        self.ids.recFront.add_widget(ThreeLineListItem(text=self.rec.getName(),
                                                       secondary_text=str(self.rec.getCalories()) + " cal.",
                                                       tertiary_text="Missed ingredients: " + str(self.rec.getMCount()),
                                                       on_release=self.toastPlaceholder))


# the MDCard that holds ingredient name + buttons for editing ingredient
class FridgeDisplay(MDCard):
    ing: Ing.Ingredient
    frg = Frg.Fridge
    ms = MainScreen

    # Handles dynamic resizing of text (copied from StackOverflow lmao)
    def on_text(self):
        if self.ids.fDisplayLabel.texture_size[0] >= self.ids.fDisplayLabel.width or \
                self.ids.fDisplayLabel.texture_size[1] >= self.ids.fDisplayLabel.height:
            self.ids.fDisplayLabel.font_size -= 7
        if self.ids.fAmtLabel.texture_size[0] >= self.ids.fAmtLabel.width or self.ids.fAmtLabel.texture_size[
            1] >= self.ids.fAmtLabel.height:
            self.ids.fAmtLabel.font_size -= 7

    # handles checkbox changing state
    def on_checkbox(self, checkbox, value):
        if value:
            self.ing.setSelected(True)
            self.ms.ids.selectedGrid.add_widget(SpecialLabel(text=self.ing.getName()))
            print("Ingredient " + self.ing.getName() + " is now selected")
        else:
            self.ing.setSelected(False)
            self.ms.refresh_homepage()
            # self.ms.ids.selectedGrid.remove_widget(SpecialLabel(text=self.ing.getName()))
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

    # We do a little trolling
    def __init__(self, ingredient: Ing.Ingredient, fridge: Frg.Fridge, ms: MainScreen, **kwargs):
        super().__init__(**kwargs)
        self.ing = ingredient
        self.frg = fridge
        self.ms = ms
        self.ids.fDisplayLabel.text = ingredient.getName()
        self.ids.fAmtLabel.text = str(ingredient.getQuant()) + " " + ingredient.getUnit()
        if self.ing.getSelected():
            self.ids.fDisplaySelector.active = True

    # deletes an ingredient
    def deletus_ingredient(self):

        self.frg.removeIngredients(self.ing.getName(), self.ing.getQuant())
        if self.frg.getName() == "Fridge":
            self.ms.ids.frScroll.remove_widget(self)
        elif self.frg.getName() == "Freezer":
            self.ms.ids.fzScroll.remove_widget(self)
        elif self.frg.getName() == "Pantry":
            self.ms.ids.pnScroll.remove_widget(self)
        else:
            self.ms.ids.msScroll.remove_widget(self)

        self.ms.refresh_homepage()

        c.execute("""DELETE FROM ingredients
                     WHERE name = ? AND owner = ?""", (self.ing.getName(), self.ms.app.getId()))
        squirrel.commit()


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

    # We commit a diminutive amount of tomfoolery
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

    # Self-explanatory
    def refresh(self):
        if self.type == "fridge":
            self.ms.refreshFridge()
        elif self.type == 'freezer':
            self.ms.refreshFreezer()
        elif self.type == 'pantry':
            self.ms.refreshPantry()
        elif self.type == 'misc':
            self.ms.refreshMisc()

    # We participate in an atomic amount of trickery
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

    # Self-explanatory
    def refresh(self):
        if self.type == "fridge":
            self.ms.refreshFridge()
        elif self.type == 'freezer':
            self.ms.refreshFreezer()
        elif self.type == 'pantry':
            self.ms.refreshPantry()
        elif self.type == 'misc':
            self.ms.refreshMisc()

    # We partake in a tiny portion of suspicious activity
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

    # Self-explanatory
    def refresh(self):
        if self.type == "fridge":
            self.ms.refreshFridge()
        elif self.type == 'freezer':
            self.ms.refreshFreezer()
        elif self.type == 'pantry':
            self.ms.refreshPantry()
        elif self.type == 'misc':
            self.ms.refreshMisc()

    # We engage in a teensy amount of social experimentation
    def __init__(self, f: Frg.Fridge, ms: MainScreen, type: str, **kwargs):
        super().__init__(**kwargs)
        self.fridge = f
        self.ms = ms
        self.type = type


# The dialog that helps to add an ingredient
class AddIngredientDialog(MDDialog):
    ferg = None

    # We act with a goal of achieving insignificant amounts of wacky antics
    def __init__(self, schlapp: Frg.Fridge, **kwargs):
        super().__init__(**kwargs)
        self.ferg = schlapp


# The dialog that helps to edit an ingredient amount
class EditIngredientDialog(MDDialog):
    pass


class GetRecipeDialog(MDDialog):
    pass


# The content of the EditIngredientDialog
class EditIngredientContent(BoxLayout):
    ferg: Frg.Fridge
    ms: MainScreen
    ing: Ing.Ingredient
    type: str

    # Reads the input of the content's textbox, and edits an ingredient amount appropriately
    def readInput(self):
        op = self.ids.ddItem.current_item
        amount = self.ids.newAmount.text
        if amount == "":
            toast("Amount field was invalid.")

        else:
            if op == "Add":
                self.ferg.increaseIngredient(self.ing.getName(), Decimal(amount))
                c.execute("""UPDATE ingredients
                             SET amount = ?
                             WHERE name = ? AND owner = ?""",
                          (self.ing.getQuant(), self.ing.getName(), self.ms.app.getId()))
                squirrel.commit()
            elif op == "Remove":
                a = self.ferg.removeIngredients(self.ing.getName(), Decimal(amount))
                print("?")
                if a == 1:
                    c.execute("""DELETE FROM ingredients
                                         WHERE name = ? AND owner = ?""", (self.ing.getName(), self.ms.app.getId()))
                    squirrel.commit()
                elif a == 0:
                    c.execute("""UPDATE ingredients
                                 SET amount = ?
                                 WHERE name = ? AND owner = ?""",
                              (self.ing.getQuant(), self.ing.getName(), self.ms.app.getId()))
                    squirrel.commit()

            else:
                toast("Invalid command issued.")

        if self.type == "fridge":
            self.ms.refreshFridge()
        elif self.type == 'freezer':
            self.ms.refreshFreezer()
            print("!")
        elif self.type == 'pantry':
            self.ms.refreshPantry()
        elif self.type == 'misc':
            self.ms.refreshMisc()

        self.ms.refresh_homepage()
        self.ids.newAmount.text = ""

    # We undertake a miniature amount of capers
    def __init__(self, ferg: Frg.Fridge, mss: MainScreen, ing: Ing.Ingredient, typ: str, **kwargs):
        super().__init__(**kwargs)
        self.ferg = ferg
        self.ms = mss
        self.ing = ing
        self.type = typ


class GetRecipeContent(BoxLayout):
    aap = Apple.Application
    ms: MainScreen

    def __init__(self, aap: Apple.Application, mss: MainScreen, **kwargs):
        super().__init__(**kwargs)
        self.aap = aap
        self.ms = mss

    def readInput(self):
        amt = self.ids.numRecipes.text
        if amt == "" or len(amt) >= 2:
            toast("Invalid input.")
        else:
            selected = self.aap.getSelectedIngredients()
            numSelected = len(selected)
            if numSelected == 0:
                toast("Select some ingredients first!")
            else:
                if check_connectivity():
                    numToGrab = int(self.ids.numRecipes.text)
                    app.numToGrab = numToGrab
                    app.sm.current = 'Loading Screen'
                else:
                    toast("Please connect to the internet first.")


# The content of the AddIngredientDialog
class AddIngredientContent(BoxLayout):
    aap = Apple.Application
    ms: MainScreen
    type: str

    # We implement a trifling amount of buffoonery
    def __init__(self, ferg: Apple.Application, mss: MainScreen, typ: str, **kwargs):
        super().__init__(**kwargs)
        self.aap = ferg
        self.ms = mss
        self.type = typ

    # Reads the input of the content's textboxes, adds an ingredient or shows an error appropriately
    def readInput(self):
        name = self.ids.ingName.text
        amount = self.ids.ingAmt.text
        unit = self.ids.ingUnit.text
        if name != "" and amount != "" and unit != "" and name != "REGISTERED" and len(name) <= 10 and len(
                amount) <= 10 and len(unit) <= 10:
            ig = Ing.Ingredient(name, Decimal(amount), unit)
            if self.aap.addIngredientTwo(ig, self.type):
                if self.type == "fridge":
                    self.ms.ids.frScroll.add_widget(FridgeDisplay(ig, self.aap.getFridge(), self.ms))
                    c.execute("""INSERT INTO ingredients(name, amount, unit, owner, location)
                                                 VALUES(?, ?, ?, ?, ?)""",
                              (ig.getName(), ig.getQuant(), ig.getUnit(), self.aap.getId(), "Fridge"))
                    squirrel.commit()
                elif self.type == 'freezer':
                    self.ms.ids.fzScroll.add_widget(FridgeDisplay(ig, self.aap.getFreezer(), self.ms))
                    c.execute("""INSERT INTO ingredients(name, amount, unit, owner, location)
                                                                     VALUES(?, ?, ?, ?, ?)""",
                              (ig.getName(), ig.getQuant(), ig.getUnit(), self.aap.getId(), "Freezer"))
                    squirrel.commit()
                elif self.type == 'pantry':
                    self.ms.ids.pnScroll.add_widget(FridgeDisplay(ig, self.aap.getPantry(), self.ms))
                    c.execute("""INSERT INTO ingredients(name, amount, unit, owner, location)
                                                                     VALUES(?, ?, ?, ?, ?)""",
                              (ig.getName(), ig.getQuant(), ig.getUnit(), self.aap.getId(), "Pantry"))
                    squirrel.commit()
                elif self.type == 'misc':
                    self.ms.ids.msScroll.add_widget(FridgeDisplay(ig, self.aap.getMisc(), self.ms))
                    c.execute("""INSERT INTO ingredients(name, amount, unit, owner, location)
                                                                     VALUES(?, ?, ?, ?, ?)""",
                              (ig.getName(), ig.getQuant(), ig.getUnit(), self.aap.getId(), "Misc"))
                    squirrel.commit()
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
    menu_t = None
    menu_sort = None
    j_store = None
    numToGrab = None

    # here for use in kv files
    def toasty(self, msg):
        toast(msg)

    # Saves current ingredients to a JsonStore (currently not being used, but here just in case)
    def saveToJson(self):
        self.j_store.clear()

        for ing in self.app.getFridge().getIngredient():
            self.j_store.put(ing.getName(), name=ing.getName(), quant=str(ing.getQuant()), unit=ing.getUnit(),
                             sel=ing.getSelected(), place="Fridge")

        for ing in self.app.getFreezer().getIngredient():
            self.j_store.put(ing.getName(), name=ing.getName(), quant=str(ing.getQuant()), unit=ing.getUnit(),
                             sel=ing.getSelected(), place="Freezer")

        for ing in self.app.getPantry().getIngredient():
            self.j_store.put(ing.getName(), name=ing.getName(), quant=str(ing.getQuant()), unit=ing.getUnit(),
                             sel=ing.getSelected(), place="Pantry")

        for ing in self.app.getMisc().getIngredient():
            self.j_store.put(ing.getName(), name=ing.getName(), quant=str(ing.getQuant()), unit=ing.getUnit(),
                             sel=ing.getSelected(), place="Misc")

    # Loads current ingredients from a JsonStore (currently not being used, but here just in case)
    def loadFromJson(self):

        for j in self.j_store:
            if j != 'REGISTERED':
                name = self.j_store[j]['name']
                quant = Decimal(self.j_store[j]['quant'])
                unit = self.j_store[j]['unit']
                place = self.j_store[j]['place']

                if place == "Fridge":
                    self.app.getFridge().addIngredient(name, quant, unit)
                elif place == "Freezer":
                    self.app.getFreezer().addIngredient(name, quant, unit)
                elif place == "Pantry":
                    self.app.getPantry().addIngredient(name, quant, unit)
                elif place == "Misc":
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
                                                                             ingredient, "fridge"))
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing freezer
    def showEditDialogFz(self, ingredient: Ing.Ingredient):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFreezer(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             ingredient, "freezer"))
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing pantry
    def showEditDialogPn(self, ingredient: Ing.Ingredient):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getPantry(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             ingredient, "pantry"))
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing misc
    def showEditDialogMs(self, ingredient: Ing.Ingredient):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getMisc(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             ingredient, "misc"))
        self.set_menu()
        self.dialog.open()

    # shows dialog for adding ingredient to fridge
    def showAddDialogFrg(self):
        self.dialog = AddIngredientDialog(self.app.getFridge(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app,
                                                                           self.sm.get_screen("Main Screen"), "fridge"))
        self.dialog.open()

    # shows dialog for adding ingredient to freezer
    def showAddDialogFrz(self):
        self.dialog = AddIngredientDialog(self.app.getFreezer(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app,
                                                                           self.sm.get_screen("Main Screen"),
                                                                           "freezer"))
        self.dialog.open()

    # shows dialog for adding ingredient to pantry
    def showAddDialogPn(self):
        self.dialog = AddIngredientDialog(self.app.getPantry(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app,
                                                                           self.sm.get_screen("Main Screen"), "pantry"))
        self.dialog.open()

    # shows dialog for adding ingredient to misc.
    def showAddDialogMs(self):
        self.dialog = AddIngredientDialog(self.app.getMisc(), type="custom",
                                          title="New Ingredient",
                                          content_cls=AddIngredientContent(self.app,
                                                                           self.sm.get_screen("Main Screen"), "misc"))
        self.dialog.open()

    def showGetRecipeDialog(self):
        self.dialog = GetRecipeDialog(type="custom",
                                      title="Get Recipes",
                                      content_cls=GetRecipeContent(self.app, self.sm.get_screen("Main Screen")))
        self.dialog.open()

    # Sets up 'Options/Logout' menu

    def set_menu_main(self, button):
        self.menu_t.caller = button
        self.menu_t.open()

    # sets current menu to one for choosing whether to add/remove when editing ingredient amount
    def set_menu(self):
        self.menu.caller = self.dialog.content_cls.ids.ddItem

    def set_menu_sort(self):
        self.menu_sort.open()

    # sets item for dropdown menu
    def set_item(self, arg):
        self.dialog.content_cls.ids.ddItem.set_item(arg)
        self.menu.dismiss()

    def set_item_sort(self, arg):
        self.sm.get_screen('Recipe List').ids.sortItem.set_item(arg)
        if arg == "Name":
            self.sm.get_screen('Recipe List').sortByName()
        elif arg == "Calories":
            self.sm.get_screen('Recipe List').sortByCals()
        elif arg == "# Missing Ingredients":
            self.sm.get_screen('Recipe List').sortByMissed()
        else:
            toast("Invalid input. Please try again.")
        self.menu_sort.dismiss()

    def switchToMain(self):
        self.app.deselectAll()
        self.sm.get_screen('Main Screen').refresh_homepage()
        self.sm.current = 'Main Screen'
        self.sm.get_screen('Recipe List').ids.sortItem.set_item("Sort by...")

    # Ok this one's actually important so I'll comment it
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mItems_sort = None
        self.mItems = None
        self.mItems_t = None
        self.menu_t = None
        self.numToGrab = 1
        self.app = Apple.Application()
        self.app.wipe()
        # Here is where I would load from json if I were to use it
        self.j_store = JsonStore('ingredience.json')
        # self.loadFromJson()
        # self.loadRegState()
        # Creates db tables in sqlite (if they dont exist ofc)
        command = """
        CREATE TABLE IF NOT EXISTS users(
        id varchar(25) NOT NULL,
        logged int NOT NULL
        )
        """
        c.execute(command)
        command = """
        CREATE TABLE IF NOT EXISTS ingredients(
        name varchar(25) NOT NULL,
        amount decimal(10, 2) NOT NULL,
        unit varchar(25) NOT NULL,
        owner varchar(25) NOT NULL,
        location varchar(25) NOT NULL,
        FOREIGN KEY(owner) REFERENCES users(id)
        )
        """
        c.execute(command)
        squirrel.commit()
        # Checks for a logged-in user, if it is found, initializes app to that user's saved state
        c.execute("""SELECT * FROM users WHERE logged = 1""")
        data = c.fetchall()
        print(data)
        if len(data) != 0:
            print("Already logged in...")
            self.initializeFromId(data[0][0])

    # ignore this lol
    def loadRegState(self):
        if "REGISTERED" in self.j_store:
            self.app.set_has_id(True)
            self.app.set_id(self.j_store['REGISTERED']['name'])
        else:
            self.app.set_has_id(False)

    # Is called when login button is pressed.
    def login(self, u_id: str):
        # Finds list of users with u_id matching id
        c.execute("""SELECT * FROM users WHERE id = ?""", (u_id,))
        data = c.fetchall()
        # print(data)
        if len(data) == 0:  # new user
            print("!")
            c.execute("""UPDATE users 
                         SET logged = 0 
                         WHERE logged = 1""")
            c.execute("INSERT INTO users (id, logged) VALUES (?, ?)", (u_id, 1))
            c.execute("""UPDATE users
                         SET logged = 1
                         WHERE id = ?""", (u_id,))
            squirrel.commit()

            self.app.set_has_id(True)
            self.app.set_id(u_id)
            # self.j_store.put("REGISTERED", name=u_id)
            self.sm.current = 'Main Screen'
        else:  # returning user
            print("?")
            c.execute("""UPDATE users 
                         SET logged = 0 
                         WHERE logged = 1""")
            c.execute("""UPDATE users
                         SET logged = 1
                         WHERE id = ?""", (u_id,))
            squirrel.commit()
            self.app.set_has_id(True)
            self.app.set_id(u_id)
            self.sm.current = 'Main Screen'
            self.initializeFromId(u_id)
            print("yeeby")

    # logs user out of app, wipes app state, dismisses menu
    def logout(self):
        c.execute("""UPDATE users
                     SET logged = 0
                     WHERE logged = 1""")
        squirrel.commit()
        self.app.wipe()
        self.sm.current = "Login Screen"
        self.menu_t.dismiss()

    # loads ingredients matching the user's id from sqlite db into their proper places
    def initializeFromId(self, u_id: str):
        self.app.set_id(u_id)
        self.app.set_has_id(True)
        c.execute("""SELECT * FROM ingredients WHERE owner = ? AND location = 'Fridge'""", (u_id,))
        data = c.fetchall()
        print(data)
        # for i in self.app.getFridge().getIngredient():
        #     print(i.getName())
        for d in data:
            # print("1")
            i = Ing.Ingredient(d[0], d[1], d[2])
            self.app.getFridge().addIngredientTwo(i)

        # for i in self.app.getFridge().getIngredient():
        #     print(i.getName())

        c.execute("""SELECT * FROM ingredients WHERE owner = ? AND location = 'Freezer'""", (u_id,))
        data = c.fetchall()
        print(data)
        for d in data:
            i = Ing.Ingredient(d[0], d[1], d[2])
            self.app.getFreezer().addIngredientTwo(i)

        c.execute("""SELECT * FROM ingredients WHERE owner = ? AND location = 'Pantry'""", (u_id,))
        data = c.fetchall()
        print(data)
        for d in data:
            i = Ing.Ingredient(d[0], d[1], d[2])
            self.app.getPantry().addIngredientTwo(i)

        c.execute("""SELECT * FROM ingredients WHERE owner = ? AND location = 'Misc'""", (u_id,))
        data = c.fetchall()
        print(data)
        for d in data:
            i = Ing.Ingredient(d[0], d[1], d[2])
            self.app.getMisc().addIngredientTwo(i)

    # calls static resource path function
    def resource_path(self, relative_path):
        print(self.app.getId())
        return resource_path(relative_path)

    # build + run app
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.sm = ScreenManager()

        if check_connectivity():
            print("Connected!")
        else:
            print("Not connected.")

        self.sm.add_widget(MainScreen(self.app, name="Main Screen"))
        self.sm.add_widget(LoginScreen(self.app, name="Login Screen"))
        self.sm.add_widget(LoadingScreen(name="Loading Screen"))
        self.sm.add_widget(RecipeViewScreen(name="Recipe List"))

        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             Ing.Ingredient(".", Decimal(0), "."),
                                                                             "fridge"))
        self.mItems = [{
            'viewclass': 'OneLineListItem',
            'text': "Add",
            'on_release': lambda x='Add': self.set_item(x)
        },
            {
                'viewclass': 'OneLineListItem',
                'text': "Remove",
                'on_release': lambda x='Remove': self.set_item(x)
            }]
        self.menu = MDDropdownMenu(items=self.mItems, width_mult=2)

        self.mItems_t = [{
            'viewclass': 'OneLineListItem',
            'text': 'Options',
            'on_release': lambda x='Options': toast("Options coming soon...")
        },
            {
                'viewclass': 'OneLineListItem',
                'text': 'Logout',
                'on_release': lambda x='Logout': self.logout()
            }]
        self.menu_t = MDDropdownMenu(caller=self.sm.get_screen("Main Screen").ids.mainToolbar, items=self.mItems_t,
                                     width_mult=2)

        self.mItems_sort = [{
            'viewclass': 'OneLineListItem',
            'text': 'Name',
            'on_release': lambda x='Name': self.set_item_sort(x)
        },
            {
                'viewclass': 'OneLineListItem',
                'text': 'Calories',
                'on_release': lambda x='Calories': self.set_item_sort(x)
            },
            {
                'viewclass': 'OneLineListItem',
                'text': '# Missing Ingredients',
                'on_release': lambda x='# Missing Ingredients': self.set_item_sort(x)
            }]

        self.menu_sort = MDDropdownMenu(caller=self.sm.get_screen("Recipe List").ids.sortItem, items=self.mItems_sort,
                                        width_mult=2)

        c.execute("""SELECT * FROM users WHERE logged = 1""")
        data = c.fetchall()
        # print(data[0][0])
        if len(data) == 0:
            self.sm.current = 'Login Screen'
        else:
            self.sm.current = 'Main Screen'

        return self.sm


if __name__ == '__main__':
    LabelBase.register(name="DMSans", fn_regular=resource_path("DMSANS.ttf"))
    wx = 350
    wy = 740
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')

    Window.size = (wx, wy)
    app = Main()
    app.run()
