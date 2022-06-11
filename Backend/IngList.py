import Backend.Ingredient as Ing
from typing import List


# Simple class representing a list of ingredients (like a shopping list) that can be saved & accessed
# by the user

class IngList:
    main_list: List[Ing.Ingredient]
    name: str

    def __init__(self):
        self.main_list = []

    def getList(self):
        return self.main_list

    def getName(self):
        return self.name

    def setName(self, name: str):
        self.name = name

    def addIngredient(self, ing: Ing.Ingredient):
        self.main_list.append(ing)
