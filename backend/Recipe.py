import backend.Ingredient as Ing
from typing import List


# A class representing a Recipe with a name, id, url, calories, servings, time to prepare, missing ingredients,
# number of missing ingredients, and whether it's vegan or vegetarian

class Recipe:
    name: str
    id: int
    url: str
    calories: int
    servings: int
    minutes: int
    mIng: List[Ing.Ingredient]
    mIngCount: int
    vegan: bool
    vegetarian: bool

    def __init__(self, j_search, j_info):
        self.id = j_search['id']
        self.name = j_search['title']
        self.calories = j_info['nutrition']['nutrients'][0]['amount']
        self.url = j_info['sourceUrl']
        self.servings = j_info['servings']
        self.minutes = j_info['readyInMinutes']
        self.vegan = j_info['vegan']
        self.vegetarian = j_info['vegetarian']
        self.mIng = []
        for a in j_search['missedIngredients']:
            self.mIng.append(Ing.Ingredient(a['name'], a['amount'], a['unit']))

        self.mIngCount = len(self.mIng)

    # getters and setters

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def getUrl(self):
        return self.url

    def getCalories(self):
        return self.calories

    def getServings(self):
        return self.servings

    def getMinutes(self):
        return self.minutes

    def getMissed(self):
        return self.mIng

    def getMCount(self):
        return self.mIngCount

    def getVegan(self):
        return self.vegan

    def getVegetarian(self):
        return self.vegetarian

    # for testing purposes: prints attributes
    def printAll(self):
        print(self.getName() + " " + str(self.getId()) + " " + self.getUrl() + " " + str(self.getCalories()) + " " +
              str(self.getServings()) + " " + str(self.getMinutes()))

    def printMissed(self):
        print("You missed " + str(self.getMCount()) + " ingredients: ")
        for i in self.getMissed():
            print(i.getName())
