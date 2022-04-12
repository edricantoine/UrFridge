import requests
import Backend.config as config
import spoonacular as sp


# A class which uses the Spoonacular API to grab recipes: more accurate recipes based on ingredients,
# recipe instructions, etc.

class SpRecipeGrabber:
    api = sp.API(config.sp_key)
    ingredients = ["Eggs", "Cheese", "Bacon"]
    calories = 200

    def grabRecipe(self):
        recipes = []  # first element in tuple will be id, second will be title
        ingString = ""
        for i in self.ingredients:
            ingString = ingString + i + ", "

        response = self.api.search_recipes_by_ingredients(ingredients=ingString, number=3, ranking=2)
        data = response.json()
        for r in data:
            recipes.append((r['id'], r['title'], self.getCalorieData(r['id'])))

        for r in recipes:
            if self.calories is not None and r[2] > self.calories:
                recipes.remove(r)

        for r in recipes:
            print(r)

        return recipes

    def getCalorieData(self, id):
        response = self.api.get_recipe_information(id, True)
        data = response.json()
        print(data['nutrition']['nutrients'][0]['name'] + " " + str(data['nutrition']['nutrients'][0]['amount']) +
              " per serving")
        return data['nutrition']['nutrients'][0]['amount']
