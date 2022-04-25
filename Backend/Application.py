import Backend.Ingredient as Ing
import Backend.Fridge as Frg
import Backend.SpRecipeGrabber as Grb
import Backend.Recipe as Rec
from typing import List
from typing import Tuple


# A class that represents the data storage of the app, with a list of fridges
class Application:
    fridge: Frg.Fridge
    pantry: Frg.Fridge
    freezer: Frg.Fridge
    misc: Frg.Fridge
    grabber = None
    recipes: List[Rec.Recipe]

    def __init__(self):
        self.fridge = Frg.Fridge("Fridge")
        self.pantry = Frg.Fridge("Pantry")
        self.freezer = Frg.Fridge("Freezer")
        self.misc = Frg.Fridge("Other")
        self.grabber = Grb.SpRecipeGrabber()
        self.recipes = []

    def getFridge(self):
        return self.fridge

    def getPantry(self):
        return self.pantry

    def getFreezer(self):
        return self.freezer

    def getMisc(self):
        return self.misc

    def getRecipes(self):
        return self.recipes

    def getRecipeFromSelectedIngredients(self, num: int, calories: int or None):
        for i in self.fridge.getIngredient():
            if i.getSelected():
                self.grabber.addIngredient(i)

        for i in self.freezer.getIngredient():
            if i.getSelected():
                self.grabber.addIngredient(i)

        for i in self.pantry.getIngredient():
            if i.getSelected():
                self.grabber.addIngredient(i)

        for i in self.misc.getIngredient():
            if i.getSelected():
                self.grabber.addIngredient(i)

        self.recipes = self.grabber.grabRecipe(num, calories)
