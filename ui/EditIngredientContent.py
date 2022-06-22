from decimal import Decimal

from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast

from backend import Fridge as Frg, Ingredient as Ing
from ui.MainScreen import MainScreen


class EditIngredientContent(BoxLayout):
    ferg: Frg.Fridge
    ms: MainScreen
    ing: Ing.Ingredient
    type: str

    # We undertake a miniature amount of capers
    def __init__(self, ferg: Frg.Fridge, mss: MainScreen, ing: Ing.Ingredient, typ: str, c, squirrel, **kwargs):
        super().__init__(**kwargs)
        self.ferg = ferg
        self.ms = mss
        self.ing = ing
        self.type = typ
        self.c = c
        self.squirrel = squirrel

    # Reads the input of the content's textbox, and edits an ingredient amount appropriately
    def readInput(self):
        op = self.ids.ddItem.current_item
        amount = self.ids.newAmount.text
        if amount == "":
            toast("Amount field was invalid.")

        else:
            if op == "Add":
                self.ferg.increaseIngredient(self.ing.getName(), Decimal(amount))
                self.c.execute("""UPDATE ingredients
                             SET amount = ?
                             WHERE name = ? AND owner = ?""",
                          (self.ing.getQuant(), self.ing.getName(), self.ms.aap.getId()))
                self.squirrel.commit()
            elif op == "Remove":
                a = self.ferg.removeIngredients(self.ing.getName(), Decimal(amount))
                # print("?")
                if a == 1:
                    self.c.execute("""DELETE FROM ingredients
                                         WHERE name = ? AND owner = ?""", (self.ing.getName(), self.ms.aap.getId()))
                    self.squirrel.commit()
                elif a == 0:
                    self.c.execute("""UPDATE ingredients
                                 SET amount = ?
                                 WHERE name = ? AND owner = ?""",
                              (self.ing.getQuant(), self.ing.getName(), self.ms.aap.getId()))
                    self.squirrel.commit()

            else:
                toast("Invalid command issued.")

        if self.type == "fridge":
            self.ms.refreshFridge()
        elif self.type == 'freezer':
            self.ms.refreshFreezer()
            # print("!")
        elif self.type == 'pantry':
            self.ms.refreshPantry()
        elif self.type == 'misc':
            self.ms.refreshMisc()

        self.ms.refresh_homepage()
        self.ids.newAmount.text = ""
