from kivy.utils import rgba
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.card import MDCard
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
import http.client as httplib
import os
import json

app_path = os.path.dirname(os.path.abspath(__file__))
squirrel = sqlite3.connect(os.path.join(app_path, 'userdata.db'))
c = squirrel.cursor()


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


class LoginScreen(Screen):
    app = None

    def __init__(self, apple: Apple.Application, **kw):
        super().__init__(**kw)
        self.app = apple
        self.ids.loginGrid.add_widget(LoginLayout(self.app))


class LoginLayout(GridLayout):
    app = None

    def __init__(self, apple: Apple.Application, **kwargs):
        super().__init__(**kwargs)
        self.app = apple


# The main screen, with the bottom navigation panels + their contents

class MainScreen(Screen):
    app = None

    def __init__(self, aap: Apple.Application, **kw):
        super().__init__(**kw)
        self.app = aap
        self.clearify()
        self.ids.botNav.switch_tab("home")
        self.ids.msBb.add_widget(AddIngredientButtonMs(self.app.misc, self, "misc"))
        self.ids.msBox.add_widget(NothingThereLabel())
        self.ids.msBox.add_widget(MDLabel(halign='center', font_name='DMSans-Regular', text='YourFridge © Edric '
                                                                                            'Antoine 2022',
                                          theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))
        self.ids.pnBb.add_widget(AddIngredientButtonPn(self.app.pantry, self, "pantry"))
        self.ids.pnBox.add_widget(NothingThereLabel())
        self.ids.pnBox.add_widget(MDLabel(halign='center', font_name='DMSans-Regular', text='YourFridge © Edric '
                                                                                            'Antoine 2022',
                                          theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))
        self.ids.fzBb.add_widget(AddIngredientButtonFz(self.app.freezer, self, "freezer"))
        self.ids.fzBox.add_widget(NothingThereLabel())
        self.ids.fzBox.add_widget(MDLabel(halign='center', font_name='DMSans-Regular', text='YourFridge © Edric '
                                                                                            'Antoine 2022',
                                          theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))
        self.ids.frBb.add_widget(AddIngredientButtonFr(self.app.fridge, self, "fridge"))
        self.ids.frBox.add_widget(NothingThereLabel())
        self.ids.frBox.add_widget(MDLabel(halign='center', font_name='DMSans-Regular', text='YourFridge © Edric '
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


# holds all screens in app
class WindowManager(ScreenManager):
    pass


# the MDCard that holds ingredient name + buttons for editing ingredient
class FridgeDisplay(MDCard):
    ing: Ing.Ingredient
    frg = Frg.Fridge
    ms = MainScreen

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
        if self.frg.getName() == "Fridge":
            self.ms.ids.frScroll.remove_widget(self)
        elif self.frg.getName() == "Freezer":
            self.ms.ids.fzScroll.remove_widget(self)
        elif self.frg.getName() == "Pantry":
            self.ms.ids.pnScroll.remove_widget(self)
        else:
            self.ms.ids.msScroll.remove_widget(self)

        # TODO: delete from db


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
    type: str

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

        # TODO: Check if item is removed, remove from db, otherwise edit db

        if self.type == "fridge":
            self.ms.refreshFridge()
        elif self.type == 'freezer':
            self.ms.refreshFreezer()
        elif self.type == 'pantry':
            self.ms.refreshPantry()
        elif self.type == 'misc':
            self.ms.refreshMisc()
        self.ids.newAmount.text = ""

    def __init__(self, ferg: Frg.Fridge, mss: MainScreen, ing: Ing.Ingredient, typ: str, **kwargs):
        super().__init__(**kwargs)
        self.ferg = ferg
        self.ms = mss
        self.ing = ing
        self.type = typ


# The content of the AddIngredientDialog
class AddIngredientContent(BoxLayout):
    aap = Apple.Application
    ms: MainScreen
    type: str

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
                elif self.type == 'freezer':
                    self.ms.ids.fzScroll.add_widget(FridgeDisplay(ig, self.aap.getFreezer(), self.ms))
                elif self.type == 'pantry':
                    self.ms.ids.pnScroll.add_widget(FridgeDisplay(ig, self.aap.getPantry(), self.ms))
                elif self.type == 'misc':
                    self.ms.ids.msScroll.add_widget(FridgeDisplay(ig, self.aap.getMisc(), self.ms))
                self.ids.ingName.text = ""
                self.ids.ingAmt.text = ""
                self.ids.ingUnit.text = ""
                # TODO: save new ingredient to SQL database here
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
    j_store = None

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
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             ingredient, "freezer"))
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing pantry
    def showEditDialogPn(self, ingredient: Ing.Ingredient):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             ingredient, "pantry"))
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing misc
    def showEditDialogMs(self, ingredient: Ing.Ingredient):
        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
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
        self.j_store = JsonStore('ingredience.json')
        # self.loadFromJson()
        # self.loadRegState()
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

    def loadRegState(self):
        if "REGISTERED" in self.j_store:
            self.app.set_has_id(True)
            self.app.set_id(self.j_store['REGISTERED']['name'])
        else:
            self.app.set_has_id(False)

    def login(self, u_id: str):
        c.execute("""SELECT * FROM users WHERE id = ?""", (u_id,))
        data = c.fetchall()
        print(data)
        if len(data) == 0:  # new user
            print("!")
            c.execute("""UPDATE users 
                         SET logged = 0 
                         WHERE logged = 1""")
            c.execute("INSERT INTO users (id, logged) VALUES (?, ?)", (u_id, 1))
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

    def logout(self):
        c.execute("""UPDATE users
                     SET logged = 0
                     WHERE logged = 1""")
        squirrel.commit()
        self.app.wipe()

    def initializeFromId(self, u_id: str):
        pass

    # build + run app
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(self.app, name="Main Screen"))
        self.sm.add_widget(LoginScreen(self.app, name="Login Screen"))

        if check_connectivity():
            print("Connected!")
        else:
            print("Not connected.")

        # TODO: Keep last user logged in and initialize the app to their state
        self.sm.current = 'Login Screen'

        return self.sm


if __name__ == '__main__':
    wx = 350
    wy = 740
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')

    Window.size = (wx, wy)
    app = Main()
    app.run()
