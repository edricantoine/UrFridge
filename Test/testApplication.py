import unittest
import Backend.Fridge as Frg
import Backend.Application as App


# Joint test suite for Application and Recipe classes

class MyTestCase(unittest.TestCase):
    a = App.Application

    def testGrabRecipe(self):
        self.a = App.Application()
        self.a.fridge = Frg.Fridge("Fridge")
        self.a.freezer = Frg.Fridge("Freezer")
        self.a.pantry = Frg.Fridge("Pantry")
        self.a.misc = Frg.Fridge("Misc")

        self.a.fridge.addIngredient("Paprika", 1.0, "tsp")
        self.a.freezer.addIngredient("Blueberries", 10.0, "berries")
        self.a.pantry.addIngredient("Beef", 1.0, "steak")
        self.a.misc.addIngredient("Ciabatta", 1.0, "loaf")

        self.a.fridge.selectIngredient("Paprika", True)
        self.a.freezer.selectIngredient("Blueberries", True)
        self.a.pantry.selectIngredient("Beef", True)
        self.a.misc.selectIngredient("Ciabatta", True)
        self.a.getRecipeFromSelectedIngredients(10, None)

        for r in self.a.getRecipes():
            r.printAll()
            r.printMissed()


if __name__ == '__main__':
    unittest.main()
