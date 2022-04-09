import requests
from py_edamam import PyEdamam


# A class which uses the Edamam API to grab recipes from the web, given a list of ingredients and calorie amount.

class RecipeGrabber:
    recipes = []
    ingredients = []
    calories = 600
    e = PyEdamam(nutrition_appid='575aad09',
                 nutrition_appkey='a06d5fcfcb82ec71c9b8566bb66ac7f3',
                 recipes_appid='575aad09',
                 recipes_appkey='a06d5fcfcb82ec71c9b8566bb66ac7f3',
                 food_appid='575aad09',
                 food_appkey='a06d5fcfcb82ec71c9b8566bb66ac7f3')

    def __init__(self, ing, cal):
        for s in ing:
            self.ingredients.append(s)

        self.calories = cal

        for recipe in self.e.search_recipe("egg and bacon"):
            print(recipe)
            print(recipe.dishType)


