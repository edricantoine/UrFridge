from decimal import *


# A class representing an Ingredient in a recipe, with a name, quantity, unit, and whether it is selected.
class Ingredient:
    name: str
    quantity: Decimal
    unit: str
    selected: bool

    def __init__(self, name: str, quantity: Decimal, unit: str):
        self.name = name
        self.quantity = quantity
        self.selected = False
        self.unit = unit

    # getters and setters
    def getName(self):
        return self.name

    def getUnit(self):
        return self.unit

    def getQuant(self):
        return self.quantity

    def getSelected(self):
        return self.selected

    def setName(self, name: str):
        self.name = name

    def setSelected(self, sel: bool):
        self.selected = sel

    # sets quantity of item relative to current quantity
    def setQuantRelative(self, to_add: Decimal):
        self.quantity = Decimal(Decimal(self.quantity) + Decimal(to_add))
