
class Ingredient:
    name = None
    quantity = None
    calories = None
    selected = None

    def __init__(self, name: str, quantity: int, cals: int):
        self.name = name
        self.quantity = quantity
        self.selected = False
        self.calories = cals

    def getName(self):
        return self.name

    def getQuant(self):
        return self.quantity

    def getSelected(self):
        return self.selected

    def setName(self, name: str):
        self.name = name

    # sets quantity of item relative to current quantity
    def setQuantRelative(self, to_add: int):
        self.quantity += to_add

    def setSelected(self, sel: bool):
        self.selected = sel
