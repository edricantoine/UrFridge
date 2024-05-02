from kivy.uix.screenmanager import Screen
from kivy.utils import rgba
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from backend import Application as Apple, Fridge as Frg, Ingredient as Ing
from ui.NothingThereLabel import NothingThereLabel
from ui.SpecialLabel import SpecialLabel
import os
import sys


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainScreen(Screen):
    aap = None
    app = None

    # We do a minuscule amount of initializing
    def __init__(self, aap: Apple.Application, app, c, squirrel, **kw):
        super().__init__(**kw)
        self.aap = aap
        self.app = app
        self.c = c
        self.squirrel = squirrel
        self.clearify()
        self.ids.botNav.switch_tab("home")
        self.ids.msBb.add_widget(AddIngredientButtonMs(self.aap.misc, self, "misc"))
        self.ids.msBox.add_widget(NothingThereLabel())
        self.ids.msBox.add_widget(
            MDLabel(halign='center', font_name=resource_path("DMSANS.ttf"), text='YourFridge © Edric '
                                                                                 'Antoine 2022',
                    theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))
        self.ids.pnBb.add_widget(AddIngredientButtonPn(self.aap.pantry, self, "pantry"))
        self.ids.pnBox.add_widget(NothingThereLabel())
        self.ids.pnBox.add_widget(
            MDLabel(halign='center', font_name=resource_path("DMSANS.ttf"), text='YourFridge © Edric '
                                                                                 'Antoine 2022',
                    theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))
        self.ids.fzBb.add_widget(AddIngredientButtonFz(self.aap.freezer, self, "freezer"))
        self.ids.fzBox.add_widget(NothingThereLabel())
        self.ids.fzBox.add_widget(
            MDLabel(halign='center', font_name=resource_path("DMSANS.ttf"), text='YourFridge © Edric '
                                                                                 'Antoine 2022',
                    theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))
        self.ids.frBb.add_widget(AddIngredientButtonFr(self.aap.fridge, self, "fridge"))
        self.ids.frBox.add_widget(NothingThereLabel())
        self.ids.frBox.add_widget(
            MDLabel(halign='center', font_name=resource_path("DMSANS.ttf"), text='YourFridge © Edric '
                                                                                 'Antoine 2022',
                    theme_text_color="Custom", font_size='10sp', text_color=rgba("#bec5d1")))

    # clears scrollpanes and refreshes ingredient ui for all four fridges

    def clearify(self):

        self.refreshFridge()
        self.refreshFreezer()
        self.refreshPantry()
        self.refreshMisc()

    # clears scrollpanes and refreshes ingredient ui for fridge

    def refreshFridge(self):
        self.ids.frScroll.clear_widgets()
        for i in self.aap.fridge.getIngredient():
            self.ids.frScroll.add_widget(FridgeDisplay(i, self.aap.getFridge(), self, self.app, self.c, self.squirrel))

    # clears scrollpanes and refreshes ingredient ui for freezer
    def refreshFreezer(self):
        self.ids.fzScroll.clear_widgets()
        for i in self.aap.freezer.getIngredient():
            self.ids.fzScroll.add_widget(FridgeDisplay(i, self.aap.getFreezer(), self, self.app, self.c, self.squirrel))

    # clears scrollpanes and refreshes ingredient ui for pantry
    def refreshPantry(self):
        self.ids.pnScroll.clear_widgets()
        for i in self.aap.pantry.getIngredient():
            self.ids.pnScroll.add_widget(FridgeDisplay(i, self.aap.getPantry(), self, self.app, self.c, self.squirrel))

    # clears scrollpanes and refreshes ingredient ui for misc. section
    def refreshMisc(self):
        self.ids.msScroll.clear_widgets()
        for i in self.aap.misc.getIngredient():
            self.ids.msScroll.add_widget(FridgeDisplay(i, self.aap.getMisc(), self, self.app, self.c, self.squirrel))

    # Stuff that happens whenever we re-enter the MainScreen
    def on_enter(self):
        self.clearify()
        self.refresh_homepage()

    # Refreshes the homepage - will definitely have more stuff added to this lol
    def refresh_homepage(self):
        self.ids.welcomeLabel.text = "Hello, " + self.aap.getId() + "!"
        self.ids.selectedGrid.clear_widgets()
        for i in self.aap.getSelectedIngredients():
            self.ids.selectedGrid.add_widget(SpecialLabel(text=i.getName()))
        # print("Homepage refreshed.")


class AddIngredientButtonFr(MDFloatingActionButton):
    fridge: Frg.Fridge
    ms: MainScreen
    thing: str

    # calls appropriate refresh method of main screen
    def refresh(self):
        if self.thing == "fridge":
            self.ms.refreshFridge()
        elif self.thing == 'freezer':
            self.ms.refreshFreezer()
        elif self.thing == 'pantry':
            self.ms.refreshPantry()
        elif self.thing == 'misc':
            self.ms.refreshMisc()

    # We commit a diminutive amount of tomfoolery
    def __init__(self, f: Frg.Fridge, ms: MainScreen, thing: str, **kwargs):
        super().__init__(**kwargs)
        self.fridge = f
        self.ms = ms
        self.thing = thing


class AddIngredientButtonFz(MDFloatingActionButton):
    fridge: Frg.Fridge
    ms: MainScreen
    thing: str

    # Self-explanatory
    def refresh(self):
        if self.thing == "fridge":
            self.ms.refreshFridge()
        elif self.thing == 'freezer':
            self.ms.refreshFreezer()
        elif self.thing == 'pantry':
            self.ms.refreshPantry()
        elif self.thing == 'misc':
            self.ms.refreshMisc()

    # We participate in an atomic amount of trickery
    def __init__(self, f: Frg.Fridge, ms: MainScreen, thing: str, **kwargs):
        super().__init__(**kwargs)
        self.fridge = f
        self.ms = ms
        self.thing = thing


class AddIngredientButtonMs(MDFloatingActionButton):
    fridge: Frg.Fridge
    ms: MainScreen
    thing: str

    # Self-explanatory
    def refresh(self):
        if self.thing == "fridge":
            self.ms.refreshFridge()
        elif self.thing == 'freezer':
            self.ms.refreshFreezer()
        elif self.thing == 'pantry':
            self.ms.refreshPantry()
        elif self.thing == 'misc':
            self.ms.refreshMisc()

    # We engage in a teensy amount of social experimentation
    def __init__(self, f: Frg.Fridge, ms: MainScreen, thing: str, **kwargs):
        super().__init__(**kwargs)
        self.fridge = f
        self.ms = ms
        self.thing = thing


class AddIngredientButtonPn(MDFloatingActionButton):
    fridge: Frg.Fridge
    ms: MainScreen
    thing: str

    # Self-explanatory
    def refresh(self):
        if self.thing == "fridge":
            self.ms.refreshFridge()
        elif self.thing == 'freezer':
            self.ms.refreshFreezer()
        elif self.thing == 'pantry':
            self.ms.refreshPantry()
        elif self.thing == 'misc':
            self.ms.refreshMisc()

    # We partake in a tiny portion of suspicious activity
    def __init__(self, f: Frg.Fridge, ms: MainScreen, thing: str, **kwargs):
        super().__init__(**kwargs)
        self.fridge = f
        self.ms = ms
        self.thing = thing


class FridgeDisplay(MDCard):
    ing: Ing.Ingredient
    frg = Frg.Fridge
    ms = MainScreen

    # We do a little trolling
    def __init__(self, ingredient: Ing.Ingredient, fridge: Frg.Fridge, ms: MainScreen, app, c, squirrel, **kwargs):
        super().__init__(**kwargs)
        self.ing = ingredient
        self.frg = fridge
        self.ms = ms
        self.app = app
        self.c = c
        self.squirrel = squirrel
        self.ids.fDisplayLabel.text = ingredient.getName()
        self.ids.fAmtLabel.text = str(ingredient.getQuant()) + " " + ingredient.getUnit()
        if self.ing.getSelected():
            self.ids.fDisplaySelector.active = True

    # Handles dynamic resizing of text (copied from StackOverflow lmao)
    def on_text(self):
        pass
        # if self.ids.fDisplayLabel.texture_size[0] >= self.ids.fDisplayLabel.width or \
        #         self.ids.fDisplayLabel.texture_size[1] >= self.ids.fDisplayLabel.height:
        #     self.ids.fDisplayLabel.font_size -= 7
        # if self.ids.fAmtLabel.texture_size[0] >= self.ids.fAmtLabel.width or self.ids.fAmtLabel.texture_size[
        #     1] >= self.ids.fAmtLabel.height:
        #     self.ids.fAmtLabel.font_size -= 7

    # handles checkbox changing state
    def on_checkbox(self, checkbox, value):
        if value:
            self.ing.setSelected(True)
            self.ms.ids.selectedGrid.add_widget(SpecialLabel(text=self.ing.getName()))
            # print("Ingredient " + self.ing.getName() + " is now selected")
        else:
            self.ing.setSelected(False)
            self.ms.refresh_homepage()
            # self.ms.ids.selectedGrid.remove_widget(SpecialLabel(text=self.ing.getName()))
            # print("Ingredient " + self.ing.getName() + " is now deselected")

    # calls the appropriate editing dialog
    def callEdit(self):
        if self.frg.getName() == "Fridge":
            self.app.showEditDialogFr(self.ing)
        elif self.frg.getName() == "Freezer":
            self.app.showEditDialogFz(self.ing)
        elif self.frg.getName() == "Pantry":
            self.app.showEditDialogPn(self.ing)
        else:
            self.app.showEditDialogMs(self.ing)

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

        self.c.execute("""DELETE FROM ingredients
                     WHERE name = ? AND owner = ?""", (self.ing.getName(), self.ms.aap.getId()))
        self.squirrel.commit()