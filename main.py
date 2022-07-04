import sys

from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.config import Config
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from decimal import *
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivy.lang import Builder
import sqlite3
import backend.Ingredient as Ing
import backend.Application as Apple
import backend.IngList as Lis
import http.client as httplib
import os
import json

from ui.AddIngredientContent import AddIngredientContent
from ui.AddIngredientDialog import AddIngredientDialog
from ui.EditIngredientContent import EditIngredientContent
from ui.GetRecipeContent import GetRecipeContent
from ui.ListViewScreen import ListViewScreen
from ui.LoadingScreen import LoadingScreen
from ui.LoginScreen import LoginScreen
from ui.MainScreen import MainScreen
from ui.NameListContent import NameListContent
from ui.RecipeViewScreen import RecipeViewScreen
from ui.ListViewEditScreen import ListViewEditScreen
from ui.ListEditDialog import ListEditDialog
from ui.ListEditContent import ListEditContent

Builder.load_file('./ui/NameListContent.kv')
Builder.load_file('./ui/AddIngredientContent.kv')
Builder.load_file('./ui/LoginScreen.kv')
Builder.load_file('./ui/LoginLayout.kv')
Builder.load_file('./ui/LoadingScreen.kv')
Builder.load_file('./ui/LoadingScreenList.kv')
Builder.load_file('./ui/RecipeViewScreen.kv')
Builder.load_file('./ui/GetRecipeContent.kv')
Builder.load_file('./ui/EditIngredientContent.kv')
Builder.load_file('./ui/FridgeDisplay.kv')
Builder.load_file('./ui/ListViewScreen.kv')
Builder.load_file('./ui/ListViewEditScreen.kv')
Builder.load_file('./ui/ListEditContent.kv')

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


# Class holding all the stuff in the login screen


# The main screen, with the bottom navigation panels + their contents


# screen for viewing lists


# holds all screens in app
class WindowManager(ScreenManager):
    pass


# the MDCard that holds ingredient name + buttons for editing ingredient


# Button that adds an ingredient (fridge)


# Same as above, but for freezer


# Same as above, but for pantry


# Same as above, but for misc.


# The dialog that helps to add an ingredient


# The dialog that helps to edit an ingredient amount
class EditIngredientDialog(MDDialog):
    pass


class GetRecipeDialog(MDDialog):
    pass


class NameListDialog(MDDialog):
    pass


# The content of the EditIngredientDialog


# The content of the AddIngredientDialog


# Label that instructs user to use the "+" button


# The class that represents the whole app

class Main(MDApp):
    app = None
    dialog = None
    gr_dialog = None
    nl_dialog = None
    add_dialog = None
    ed_dialog = None
    ls_dialog = None
    sm = None
    menu = None
    menu_t = None
    menu_sort = None
    menu_list = None
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

    # saves the currently selected ingredients to a new List
    def saveSelectedToList(self):
        pass

    # closes current dialog
    def dialog_close(self):
        self.dialog.dismiss(force=True)

    # shows dialog for editing fridge
    def showEditDialogFr(self, ingredient: Ing.Ingredient):
        self.dialog = self.ed_dialog
        self.dialog.content_cls.ferg = self.app.getFridge()
        self.dialog.content_cls.ing = ingredient
        self.dialog.content_cls.type = "fridge"

        self.set_menu()
        self.dialog.open()

    # shows dialog for editing freezer
    def showEditDialogFz(self, ingredient: Ing.Ingredient):
        self.dialog = self.ed_dialog
        self.dialog.content_cls.ferg = self.app.getFreezer()
        self.dialog.content_cls.ing = ingredient
        self.dialog.content_cls.type = "freezer"
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing pantry
    def showEditDialogPn(self, ingredient: Ing.Ingredient):
        self.dialog = self.ed_dialog
        self.dialog.content_cls.ferg = self.app.getPantry()
        self.dialog.content_cls.ing = ingredient
        self.dialog.content_cls.type = "pantry"
        self.set_menu()
        self.dialog.open()

    # shows dialog for editing misc
    def showEditDialogMs(self, ingredient: Ing.Ingredient):
        self.dialog = self.ed_dialog
        self.dialog.content_cls.ferg = self.app.getMisc()
        self.dialog.content_cls.ing = ingredient
        self.dialog.content_cls.type = "misc"
        self.set_menu()
        self.dialog.open()

    # shows dialog for adding ingredient to fridge
    def showAddDialogFrg(self):
        self.dialog = self.add_dialog
        self.dialog.ferg = self.app.getFridge()
        self.dialog.content_cls.type = 'fridge'
        self.dialog.open()

    # shows dialog for adding ingredient to freezer
    def showAddDialogFrz(self):
        self.dialog = self.add_dialog
        self.dialog.ferg = self.app.getFreezer()
        self.dialog.content_cls.type = 'freezer'
        self.dialog.open()

    # shows dialog for adding ingredient to pantry
    def showAddDialogPn(self):
        self.dialog = self.add_dialog
        self.dialog.ferg = self.app.getPantry()
        self.dialog.content_cls.type = 'pantry'
        self.dialog.open()

    # shows dialog for adding ingredient to misc.
    def showAddDialogMs(self):
        self.dialog = self.add_dialog
        self.dialog.ferg = self.app.getMisc()
        self.dialog.content_cls.type = 'misc'
        self.dialog.open()

    def showGetRecipeDialog(self):
        self.dialog = self.gr_dialog
        self.dialog.open()

    def showNameListDialog(self):
        self.dialog = self.nl_dialog
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

    def set_menu_list(self):
        self.menu_list.open()

    def openListViewScreen(self):
        self.sm.get_screen("List View").initializeFromListList(self.app.getLists())
        self.sm.current = "List View"

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

    def set_item_list(self, arg):
        self.sm.get_screen("List View").ids.sortItemList.set_item(arg)
        if arg == "Name":
            self.sm.get_screen("List View").sortByName()
        elif arg == "# Items":
            self.sm.get_screen("List View").sortByNumIngredients()
        self.menu_list.dismiss()

    def switchToMain(self):
        self.app.deselectAll()
        self.sm.get_screen('Main Screen').refresh_homepage()
        self.sm.current = 'Main Screen'
        self.sm.get_screen('Recipe List').ids.sortItem.set_item("Sort by...")

    def switchToListViewAndDelete(self, lis: Lis.IngList):
        self.app.getLists().remove(lis)
        c.execute("""
            DELETE FROM lists 
            WHERE name = ?
            AND owner = ?
        """, (lis.getName(), self.app.getId()))
        squirrel.commit()
        self.sm.get_screen("List View").initializeFromListList(self.app.getLists())
        self.sm.current = "List View"

    def openListViewEditName(self, lis: Lis.IngList):
        self.dialog = self.ls_dialog
        self.dialog.content_cls.lis = lis
        self.dialog.open()

    # Ok this one's actually important so I'll comment it
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_list = None
        self.mItems_sort = None
        self.mItems = None
        self.mItems_t = None
        self.mItems_list = None
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
        command = """
        CREATE TABLE IF NOT EXISTS lists(
        name varchar(25) NOT NULL,
        contents varchar(255) NOT NULL,
        owner varchar(25) NOT NULL,
        FOREIGN KEY(owner) REFERENCES users(id)
        )
        """
        c.execute(command)
        squirrel.commit()
        # Checks for a logged-in user, if it is found, initializes app to that user's saved state
        c.execute("""SELECT * FROM users WHERE logged = 1""")
        data = c.fetchall()
        # print(data)
        if len(data) != 0:
            # print("Already logged in...")
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
            # print("!")
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
            # print("?")
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
            # print("yeeby")

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
        # print(data)
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
        # print(data)
        for d in data:
            i = Ing.Ingredient(d[0], d[1], d[2])
            self.app.getFreezer().addIngredientTwo(i)

        c.execute("""SELECT * FROM ingredients WHERE owner = ? AND location = 'Pantry'""", (u_id,))
        data = c.fetchall()
        # print(data)
        for d in data:
            i = Ing.Ingredient(d[0], d[1], d[2])
            self.app.getPantry().addIngredientTwo(i)

        c.execute("""SELECT * FROM ingredients WHERE owner = ? AND location = 'Misc'""", (u_id,))
        data = c.fetchall()
        # print(data)
        for d in data:
            i = Ing.Ingredient(d[0], d[1], d[2])
            self.app.getMisc().addIngredientTwo(i)

        c.execute("""SELECT * FROM lists WHERE owner = ?""", (u_id,))
        data = c.fetchall()
        # print(data)
        for d in data:
            liste = Lis.IngList()
            name = d[0]
            contents = d[1]
            contentsList = json.loads(contents)
            for s in contentsList:
                liste.addIngredient(Ing.Ingredient(s, Decimal(1), "unit"))

            liste.setName(name)
            self.app.addListToLists(liste)

    # calls static resource path function
    def resource_path(self, relative_path):
        # print(self.app.getId())
        return resource_path(relative_path)

    # build + run app
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.sm = ScreenManager()

        self.sm.add_widget(MainScreen(self.app, app, c, squirrel, name="Main Screen"))
        self.sm.add_widget(LoginScreen(self.app, app, name="Login Screen"))
        self.sm.add_widget(LoadingScreen(app, name="Loading Screen"))
        self.sm.add_widget(RecipeViewScreen(name="Recipe List"))
        self.sm.add_widget(ListViewScreen(app, name="List View"))
        self.sm.add_widget(ListViewEditScreen(name="List View Edit"))

        self.dialog = EditIngredientDialog(type="custom",
                                           title="Edit Ingredient",
                                           content_cls=EditIngredientContent(self.app.getFridge(),
                                                                             self.sm.get_screen("Main Screen"),
                                                                             Ing.Ingredient(".", Decimal(0), "."),
                                                                             "fridge", c, squirrel))
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

        self.mItems_list = [{
            'viewclass': 'OneLineListItem',
            'text': 'Name',
            'on_release': lambda x='Name': self.set_item_list(x)
        },
            {
                'viewclass': 'OneLineListItem',
                'text': '# Items',
                'on_release': lambda x='# Items': self.set_item_list(x)
            }
        ]

        self.menu_sort = MDDropdownMenu(caller=self.sm.get_screen("Recipe List").ids.sortItem, items=self.mItems_sort,
                                        width_mult=2)

        self.menu_list = MDDropdownMenu(caller=self.sm.get_screen("List View").ids.sortItemList, items=self.mItems_list,
                                        width_mult=2)

        self.gr_dialog = GetRecipeDialog(type="custom",
                                         title="Get Recipes",
                                         content_cls=GetRecipeContent(self.app, self.sm.get_screen("Main Screen"), app))

        self.nl_dialog = NameListDialog(type="custom",
                                        title="Name List",
                                        content_cls=NameListContent(self.app, app, c, squirrel))

        self.add_dialog = AddIngredientDialog(self.app.getFridge(), type="custom",
                                              title="New Ingredient",
                                              content_cls=AddIngredientContent(self.app,
                                                                               self.sm.get_screen("Main Screen"),
                                                                               "fridge", c, squirrel, app))

        self.ed_dialog = EditIngredientDialog(type="custom",
                                              title="Edit Ingredient",
                                              content_cls=EditIngredientContent(self.app.getPantry(),
                                                                                self.sm.get_screen("Main Screen"),
                                                                                Ing.Ingredient(".", Decimal(0.0), "."),
                                                                                "pantry", c, squirrel))
        self.ls_dialog = ListEditDialog(type="custom",
                                        title="Edit List Name",
                                        content_cls=ListEditContent(Lis.IngList(), app, c, squirrel))

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
