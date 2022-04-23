import Backend.Ingredient as Ing
import Backend.Fridge as Frg
import Backend.SpRecipeGrabber as Grb
from typing import List


# A class that represents the data storage of the app, with a list of fridges
class Application:
    fridge: Frg.Fridge
    pantry: Frg.Fridge
    freezer: Frg.Fridge
    misc: Frg.Fridge

    def __init__(self):
        self.fridge = Frg.Fridge("Fridge")
        self.pantry = Frg.Fridge("Pantry")
        self.freezer = Frg.Fridge("Freezer")
        self.misc = Frg.Fridge("Other")

    def getFridge(self):
        return self.fridge

    def getPantry(self):
        return self.pantry

    def getFreezer(self):
        return self.freezer

    def getMisc(self):
        return self.misc
