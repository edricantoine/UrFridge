import backend.SpRecipeGrabber as Grab
import backend.Ingredient as Ing


from typing import List
from decimal import *


# A class representing a Fridge with a name, and in which ingredients can be stored
class Fridge:
    name = None  # the Fridge's name
    ingredients: List[Ing.Ingredient] = None  # a list of Ingredients

    def __init__(self, name: str):
        self.grabber = Grab.SpRecipeGrabber()
        self.name = name
        self.ingredients = []
        self.recipes = []

    # getter for ingredients
    # No testing needed
    def getIngredient(self):
        return self.ingredients

    # creates + adds ingredient to this fridge given parameters.
    # WILL ALWAYS BE CALLED THROUGH "APPLICATION" CLASS, SO DOES NOT CHECK DUPLICATES
    # TESTED
    def addIngredient(self, name: str, quant: Decimal, unit: str):
        self.ingredients.append(Ing.Ingredient(name, quant, unit))

    # adds ingredient directly to fridge.
    # WILL ALWAYS BE CALLED THROUGH "APPLICATION" CLASS, SO DOES NOT CHECK DUPLICATES
    # TESTED
    def addIngredientTwo(self, ig: Ing.Ingredient):
        self.ingredients.append(ig)

    # verifies that ingredient with name does not already exist in this fridge
    # TESTED
    def verifyIngredient(self, name: str):
        for i in self.ingredients:
            if i.getName() == name:
                return False

        return True

    # increases the quantity of an already existing item in the fridge by quant
    # TESTED
    def increaseIngredient(self, name: str, quant: Decimal):
        for i in self.ingredients:
            if i.getName() == name:
                i.setQuantRelative(quant)
                return True

        return False

    # removes quant of an ingredient with given name from the fridge, deletes ing. from fridge if new quant is <= 0
    # TESTED
    def removeIngredients(self, name: str, quant: Decimal):
        for i in self.ingredients:
            if i.getName() == name:
                i.setQuantRelative(quant * -1)
                if i.getQuant() <= 0:
                    self.ingredients.remove(i)
                    return 1
                return 0

        return -1

    # sets ingredient's selected value to given boolean
    # TESTED
    def selectIngredient(self, name: str, selected: bool):
        for i in self.ingredients:
            if i.getName() == name:
                i.setSelected(selected)
                return True

        return False

    # getter for name (name is unchangeable)
    # No testing needed
    def getName(self):
        return self.name

    # returns a list of all selected ingredients in this fridge
    # TESTED
    def getSelectedIngredients(self):
        ret = []
        for i in self.ingredients:
            if i.getSelected():
                ret.append(i)
        return ret

