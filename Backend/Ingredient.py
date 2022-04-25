
class Ingredient:
    name = None
    quantity = None
    unit = None
    calories = None
    selected = None

    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.selected = False
        self.unit = unit

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

    # sets quantity of item relative to current quantity
    def setQuantRelative(self, to_add: float):
        self.quantity += to_add

    def setSelected(self, sel: bool):
        self.selected = sel
