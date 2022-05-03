import Backend.SpRecipeGrabber as Grab
import Backend.Ingredient as Ing


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
    def getIngredient(self):
        return self.ingredients

    # adds an ingredient with quantity to the fridge, not selected by default
    def addIngredient(self, name: str, quant: Decimal, unit: str):
        for i in self.ingredients:
            if i.getName() == name:
                return False

        self.ingredients.append(Ing.Ingredient(name, quant, unit))
        return True

    # increases the quantity of an already existing item in the fridge by quant
    def increaseIngredient(self, name: str, quant: Decimal):
        for i in self.ingredients:
            if i.getName() == name:
                i.setQuantRelative(quant)
                return True

        return False

    # removes quant of an ingredient with given name from the fridge, deletes ing. from fridge if new quant is <= 0
    def removeIngredients(self, name: str, quant: Decimal):
        for i in self.ingredients:
            if i.getName() == name:
                i.setQuantRelative(quant * -1)
                if i.getQuant() <= 0:
                    self.ingredients.remove(i)
                    return True

        return False

    # sets ingredient's selected value to given boolean
    def selectIngredient(self, name: str, selected: bool):
        for i in self.ingredients:
            if i.getName() == name:
                i.setSelected(selected)
                return True

        return False

    # getter for name (name is unchangeable)
    def getName(self):
        return self.name
