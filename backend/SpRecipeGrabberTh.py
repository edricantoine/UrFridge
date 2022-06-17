import backend.config as config
import spoonacular as sp
import backend.Ingredient as Ing
import backend.Recipe as Rec
import threading
import multiprocessing as mpr
from multiprocessing import Pool
from typing import List


# A class which uses the Spoonacular API to grab recipes: more accurate recipes based on ingredients,
# recipe instructions, etc.


class SpRecipeGrabberTh:
    api = sp.API(config.sp_key)
    ingredients: List[Ing.Ingredient] = None
    calories = None
    recipes = List[Rec.Recipe]

    def __init__(self):
        self.ingredients = []
        self.recipes = []

    # grabs a number of Recipes given a list of ingredients

    def grabRecipe(self, num: int, calories: int or None):
        self.setCalories(calories)
        self.recipes = []

        ingString = ""
        for i in self.ingredients:
            ingString = ingString + i.getName() + ", "

        response = self.api.search_recipes_by_ingredients(ingredients=ingString, number=num, ranking=2)
        data = response.json()
        pool = Pool()
        pool.map(self.run, data)

        for r in self.recipes:
            if self.calories is not None and r.getCalories() > self.calories:
                self.recipes.remove(r)

        return self.recipes

    # getters and setters

    def run(self, r: dict):
        responser = self.api.get_recipe_information(r['id'], True)
        bababooey = responser.json()
        self.recipes.append(Rec.Recipe(r, bababooey))

    def addIngredient(self, ingredient: Ing.Ingredient):
        self.ingredients.append(ingredient)

    def getIngredients(self):
        return self.ingredients

    def setCalories(self, calories: int):
        self.calories = calories

    def getCalories(self):
        return self.calories

    def getRecipes(self):
        return self.recipes


class GrabberThread(threading.Thread):
    rg: SpRecipeGrabberTh
    r: dict

    def __init__(self, rg: SpRecipeGrabberTh, r: dict):
        super().__init__()
        self.rg = rg
        self.r = r

    def run(self):
        responser = self.rg.api.get_recipe_information(self.r['id'], True)
        bababooey = responser.json()
        self.rg.recipes.append(Rec.Recipe(self.r, bababooey))
