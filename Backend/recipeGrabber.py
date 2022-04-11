import requests
from py_edamam import PyEdamam


# A class which uses the Edamam API to grab recipes from the web, given a list of ingredients and calorie amount.
# Default ingredients list is empty, default calories is 1000, default cuisine, dish, and meal types are "All"
class RecipeGrabber:
    ingredients = []  # a list of ingredients you can search by
    calories = 1000  # Max. no of calories in desired meal
    mealType = "All"
    cuisineType = "All"
    dishType = "All"
    # object that interacts with the Edamam API
    e = PyEdamam(nutrition_appid='575aad09',
                 nutrition_appkey='a06d5fcfcb82ec71c9b8566bb66ac7f3',
                 recipes_appid='575aad09',
                 recipes_appkey='a06d5fcfcb82ec71c9b8566bb66ac7f3',
                 food_appid='575aad09',
                 food_appkey='a06d5fcfcb82ec71c9b8566bb66ac7f3')

    def __init__(self, ing=None, cal=1000, mt="All", ct="All", dt="All"):
        if ing is None:
            ing = []

        for s in ing:
            self.ingredients.append(s)
        self.calories = cal
        self.mealType = mt
        self.cuisineType = ct
        self.dishType = dt

    # grabs a recipe with the API, searching by ingredients list and max no. calories
    def grabRecipe(self):
        recipes = []  # recipes[0] will always be the label, [1] calories, [2] ingredients + quantities
        toReturn = []
        ingString = ""
        for i in self.ingredients:
            ingString = ingString + " " + i

        for recipe in self.e.search_recipe(ingString):
            if recipe.calories <= self.calories:
                recipes.append(recipe)

        for r2 in recipes:
            if (self.mealType != "All" and r2.mealType != self.mealType) or (self.dishType != "All" and r2.dishType != self.dishType) \
                    or (self.cuisineType != "All" and r2.cuisineType != self.cuisineType):
                recipes.remove(r2)

        for r3 in recipes:
            toReturn.append((r3.label, r3.calories, r3.ingredient_quantities))

        return toReturn
