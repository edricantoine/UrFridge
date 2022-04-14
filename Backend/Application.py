import Backend.Ingredient as Ing
import Backend.Fridge as Frg
import Backend.SpRecipeGrabber as Grb
from typing import List


# A class that represents the data storage of the app, with a list of fridges
class Application:
    fridges: List[Frg.Fridge]

    def __init__(self):
        self.fridges = []

    # Adds a fridge with given name to the App. Fails and returns false if fridge w/ that name exists.
    def addFridge(self, name):
        for f in self.fridges:
            if f.getName() == name:
                return False

        self.fridges.append(Frg.Fridge(name))
        return True

    # Removes a fridge with given name from the App. Fails and returns false if fridge w/ that name doesn't exist.
    def removeFridge(self, name):
        for f in self.fridges:
            if f.getName() == name:
                self.fridges.remove(f)
                return True

        return False

    # Getter for fridges list
    def getFridges(self):
        return self.fridges
