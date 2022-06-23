from decimal import Decimal

from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast

from backend import Application as Apple, Ingredient as Ing
from ui.MainScreen import MainScreen, FridgeDisplay


class AddIngredientContent(BoxLayout):
    aap = Apple.Application
    ms: MainScreen
    type: str
    c = None
    squirrel = None

    # We implement a trifling amount of buffoonery
    def __init__(self, ferg: Apple.Application, mss: MainScreen, typ: str, c, squirrel, app, **kwargs):
        super().__init__(**kwargs)
        self.aap = ferg
        self.app = app
        self.ms = mss
        self.type = typ
        self.c = c
        self.squirrel = squirrel

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
                    self.ms.ids.frScroll.add_widget(FridgeDisplay(ig, self.aap.getFridge(), self.ms, self.app,
                                                                  self.c, self.squirrel))
                    self.c.execute("""INSERT INTO ingredients(name, amount, unit, owner, location)
                                                 VALUES(?, ?, ?, ?, ?)""",
                              (ig.getName(), ig.getQuant(), ig.getUnit(), self.aap.getId(), "Fridge"))
                    self.squirrel.commit()
                elif self.type == 'freezer':
                    self.ms.ids.fzScroll.add_widget(FridgeDisplay(ig, self.aap.getFreezer(), self.ms, self.app, self.c,
                                                                  self.squirrel))
                    self.c.execute("""INSERT INTO ingredients(name, amount, unit, owner, location)
                                                                     VALUES(?, ?, ?, ?, ?)""",
                              (ig.getName(), ig.getQuant(), ig.getUnit(), self.aap.getId(), "Freezer"))
                    self.squirrel.commit()
                elif self.type == 'pantry':
                    self.ms.ids.pnScroll.add_widget(FridgeDisplay(ig, self.aap.getPantry(), self.ms,
                                                                  self.app, self.c, self.squirrel))
                    self.c.execute("""INSERT INTO ingredients(name, amount, unit, owner, location)
                                                                     VALUES(?, ?, ?, ?, ?)""",
                              (ig.getName(), ig.getQuant(), ig.getUnit(), self.aap.getId(), "Pantry"))
                    self.squirrel.commit()
                elif self.type == 'misc':
                    self.ms.ids.msScroll.add_widget(FridgeDisplay(ig, self.aap.getMisc(), self.ms,
                                                                  self.app, self.c, self.squirrel))
                    self.c.execute("""INSERT INTO ingredients(name, amount, unit, owner, location)
                                                                     VALUES(?, ?, ?, ?, ?)""",
                              (ig.getName(), ig.getQuant(), ig.getUnit(), self.aap.getId(), "Misc"))
                    self.squirrel.commit()
                self.ids.ingName.text = ""
                self.ids.ingAmt.text = ""
                self.ids.ingUnit.text = ""

            else:
                toast("An ingredient with that name already exists.")
        else:
            toast('One or more fields are invalid.')

        self.ids.ingName.text = ""
        self.ids.ingAmt.text = ""
        self.ids.ingUnit.text = ""