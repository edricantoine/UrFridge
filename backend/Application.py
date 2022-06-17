import backend.Fridge as Frg
import backend.SpRecipeGrabber as Grb
import backend.SpRecipeGrabberTh as Grbth
import backend.Recipe as Rec
import backend.Ingredient as Ig
import backend.IngList as Lis
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
    user_id: str
    has_chosen_id: bool
    lists: List[Lis.IngList]

    def __init__(self):
        self.fridge = Frg.Fridge("Fridge")
        self.pantry = Frg.Fridge("Pantry")
        self.freezer = Frg.Fridge("Freezer")
        self.misc = Frg.Fridge("Other")
        self.grabber = Grb.SpRecipeGrabber()
        self.grabberth = Grbth.SpRecipeGrabberTh()
        self.recipes = []
        self.lists = []
        self.has_chosen_id = False
        self.user_id = ""

    # getters and setters

    def getHasChosenId(self):
        return self.has_chosen_id

    def getId(self):
        return self.user_id

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

    def getLists(self):
        return self.lists

    # adds an ingredient to a fridge given an Ingredient object
    def addIngredientTwo(self, ig: Ig.Ingredient, where: str):
        name = ig.getName()
        if self.fridge.verifyIngredient(name) and self.freezer.verifyIngredient(name) and self.pantry.verifyIngredient(
                name) and self.misc.verifyIngredient(name):
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

    # adds an ingredient to fridge
    def addIngredient(self, name: str, quant: Decimal, unit: str, where: str):
        if self.fridge.verifyIngredient(name) and self.freezer.verifyIngredient(name) and self.pantry.verifyIngredient(
                name) and self.misc.verifyIngredient(name):
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

    # Returns a list of selected ingredients from all four fridges
    def getSelectedIngredients(self):
        ret = []
        ret.extend(self.getFridge().getSelectedIngredients())
        ret.extend(self.getFreezer().getSelectedIngredients())
        ret.extend(self.getPantry().getSelectedIngredients())
        ret.extend(self.getMisc().getSelectedIngredients())
        return ret

    def deselectAll(self):
        for i in self.getSelectedIngredients():
            i.setSelected(False)

    # grabs a list of num recipes using the Spoonacular API, from selected items in all four fridges
    def getRecipeFromSelectedIngredients(self, num: int, calories: int or None):
        self.grabber.ingredients.clear()
        for i in self.getSelectedIngredients():
            self.grabber.addIngredient(i)

        self.recipes = self.grabber.grabRecipe(num, calories)

    def setListName(self, lis: Lis.IngList, name: str):
        for i in self.lists:
            if i.getName() == name:
                return False

        lis.setName(name)
        return True

    # grabs a list of num recipes using the Spoonacular API, given a IngList
    # TODO: test this function when it is needed
    def getRecipeFromList(self, lis: Lis.IngList, num:int):
        self.grabber.ingredients.clear()
        for i in lis:
            self.grabber.addIngredient(i)

        self.recipes = self.grabber.grabRecipe(num, None)

    # DOES NOT WORK YET. DO NOT USE
    def getRecipeFromSelectedIngredientsTh(self, num: int, calories: int or None):
        self.grabberth.ingredients.clear()
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

    def addListToLists(self, lis: Lis.IngList):
        self.lists.append(lis)

    # CAN NEVER BE CALLED WHEN lis IS NOT IN self.lists, SO DOESN'T CHECK FOR THAT.
    def removeListFromLists(self, lis: Lis.IngList):
        self.lists.remove(lis)

    def set_id(self, u_id: str):
        self.user_id = u_id

    def set_has_id(self, h_id: bool):
        self.has_chosen_id = h_id

    def wipe(self):
        self.fridge.ingredients.clear()
        self.freezer.ingredients.clear()
        self.pantry.ingredients.clear()
        self.misc.ingredients.clear()
        self.lists.clear()
        self.user_id = ""
        self.has_chosen_id = False
