import requests
import Backend.config as config
import spoonacular as sp
import Backend.Ingredient as Ing
import Backend.Recipe as Rec
from typing import List
from typing import Tuple


# A class which uses the Spoonacular API to grab recipes: more accurate recipes based on ingredients,
# recipe instructions, etc.

class SpRecipeGrabber:
    api = sp.API(config.sp_key)
    ingredients: List[Ing.Ingredient] = None
    calories = None

    def __init__(self):
        self.ingredients = []

    # grabs a number of Recipes given a list of ingredients

    def grabRecipe(self, num: int, calories: int or None):
        self.setCalories(calories)
        recipes: List[Rec.Recipe] = []

        ingString = ""
        for i in self.ingredients:
            ingString = ingString + i.getName() + ", "

        response = self.api.search_recipes_by_ingredients(ingredients=ingString, number=num, ranking=2)
        data = response.json()
        for r in data:
            responser = self.api.get_recipe_information(r['id'], True)
            bababooey = responser.json()
            recipes.append(Rec.Recipe(r, bababooey))

        for r in recipes:
            if self.calories is not None and r.getCalories() > self.calories:
                recipes.remove(r)

        return recipes

    # getters and setters

    def addIngredient(self, ingredient: Ing.Ingredient):
        self.ingredients.append(ingredient)

    def getIngredients(self):
        return self.ingredients

    def setCalories(self, calories: int):
        self.calories = calories

    def getCalories(self):
        return self.calories
