import Backend.Fridge as Frg
import Backend.SpRecipeGrabber as Grb
import Backend.SpRecipeGrabberTh as Grbth
import Backend.Recipe as Rec
import Backend.Ingredient as Ig
from decimal import *
from typing import List


# A class that represents the data storage of the app, with a list of fridges
class Application:
    fridge: Frg.Fridge
    pantry: Frg.Fridge
    freezer: Frg.Fridge
    misc: Frg.Fridge
    grabber = None
    grabberth = None
    recipes: List[Rec.Recipe]

    def __init__(self):
        self.fridge = Frg.Fridge("Fridge")
        self.pantry = Frg.Fridge("Pantry")
        self.freezer = Frg.Fridge("Freezer")
        self.misc = Frg.Fridge("Other")
        self.grabber = Grb.SpRecipeGrabber()
        self.grabberth = Grbth.SpRecipeGrabberTh()
        self.recipes = []

    # getters and setters

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

    def addIngredientTwo(self, ig: Ig.Ingredient, where: str):
        name = ig.getName()
        if self.fridge.verifyIngredient(name) and self.freezer.verifyIngredient(name) and self.pantry.verifyIngredient(name) and self.misc.verifyIngredient(name):
            if where == "fridge":
                self.fridge.addIngredientTwo(ig)
            elif where == "freezer":
                self.freezer.addIngredientTwo(ig)
            elif where == "pantry":
                self.pantry.addIngredientTwo(ig)
            else:
                self.misc.addIngredientTwo(ig)

            return True
        return False

    def addIngredient(self, name: str, quant: Decimal, unit: str, where: str):
        if self.fridge.verifyIngredient(name) and self.freezer.verifyIngredient(name) and self.pantry.verifyIngredient(name) and self.misc.verifyIngredient(name):
            if where == "fridge":
                self.fridge.addIngredient(name, quant, unit)
            elif where == "freezer":
                self.freezer.addIngredient(name, quant, unit)
            elif where == "pantry":
                self.pantry.addIngredient(name, quant, unit)
            else:
                self.misc.addIngredient(name, quant, unit)

            return True
        return False

    # grabs a list of num recipes using the Spoonacular API, from selected items in all four fridges

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

    def getRecipeFromSelectedIngredientsTh(self, num: int, calories: int or None):
        for i in self.fridge.getIngredient():
            if i.getSelected():
                self.grabberth.addIngredient(i)

        for i in self.freezer.getIngredient():
            if i.getSelected():
                self.grabberth.addIngredient(i)

        for i in self.pantry.getIngredient():
            if i.getSelected():
                self.grabberth.addIngredient(i)

        for i in self.misc.getIngredient():
            if i.getSelected():
                self.grabberth.addIngredient(i)

        self.recipes = self.grabberth.grabRecipe(num, calories)
