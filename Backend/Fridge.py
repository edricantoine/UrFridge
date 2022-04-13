import Backend.SpRecipeGrabber as Grab
import Backend.Ingredient as Ing
from typing import List
from typing import Tuple


# A class representing a Fridge with a name, and in which ingredients can be stored
class Fridge:
    grabber = None  # the SpRecipeGrabber it will use to grab recipes
    name = None  # the Fridge's name
    ingredients: List[Ing.Ingredient] = None  # a list of Ingredients
    recipes: List[Tuple[int, str, int, str]]

    def __init__(self, name: str):
        self.grabber = Grab.SpRecipeGrabber()
        self.name = name
        self.ingredients = []
        self.recipes = []

    # getter for ingredients
    def getIngredient(self):
        return self.ingredients

    # adds an ingredient with quantity to the fridge, not selected by default
    def addIngredient(self, name: str, quant: int):
        self.ingredients.append(Ing.Ingredient(name, quant))

    # increases the quantity of an already existing item in the fridge by quant
    def increaseIngredient(self, name: str, quant: int):
        for i in self.ingredients:
            if i.getName() == name:
                i.setQuantRelative(quant)
                return True

        return False

    # removes quant of an ingredient with given name from the fridge, deletes ing. from fridge if new quant is <= 0
    def removeIngredients(self, name: str, quant: int):
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

    # getter + setter for name
    def setName(self, name: str):
        self.name = name

    def getName(self):
        return self.name

    # getter for grabber
    def getGrabber(self):
        return self.grabber

    # getter for recipes
    def getRecipes(self):
        return self.recipes

    def getRecipeFromSelectedIngredients(self, num: int, calories: int or None):
        for i in self.ingredients:
            if i.getSelected():
                self.grabber.addIngredient(i)

        self.recipes = self.grabber.grabRecipe(num, calories)


