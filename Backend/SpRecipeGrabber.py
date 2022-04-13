import requests
import Backend.config as config
import spoonacular as sp
import Backend.Ingredient as Ing
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

    def grabRecipe(self, num: int, calories: int or None):
        self.setCalories(calories)
        recipes: List[Tuple[int, str, int, str]] = []  # first element in tuple will be id, second will be title,
        # third is calories, fourth is url

        ingString = ""
        for i in self.ingredients:
            ingString = ingString + i.getName() + ", "

        response = self.api.search_recipes_by_ingredients(ingredients=ingString, number=num, ranking=2)
        data = response.json()
        for r in data:
            cData = self.getCalorieData(r['id'])
            recipes.append((r['id'], r['title'], cData[0], cData[1]))

        for r in recipes:
            if self.calories is not None and r[2] > self.calories:
                recipes.remove(r)

        return recipes

    def getCalorieData(self, rid: int):
        response = self.api.get_recipe_information(rid, True)
        data = response.json()

        return [data['nutrition']['nutrients'][0]['amount'], data['sourceUrl']]

    def addIngredient(self, ingredient: Ing.Ingredient):
        self.ingredients.append(ingredient)

    def getIngredients(self):
        return self.ingredients

    def setCalories(self, calories: int):
        self.calories = calories

    def getCalories(self):
        return self.calories
