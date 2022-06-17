import unittest
import Backend.Fridge as Frg
import Backend.Application as App
import Backend.Ingredient as Ing
import Backend.IngList as Lis
from decimal import *


# Joint test suite for Application and Recipe classes

class MyTestCase(unittest.TestCase):
    a = App.Application

    def testGrabRecipe(self):
        self.a = App.Application()
        self.a.fridge = Frg.Fridge("Fridge")
        self.a.freezer = Frg.Fridge("Freezer")
        self.a.pantry = Frg.Fridge("Pantry")
        self.a.misc = Frg.Fridge("Misc")

        self.a.fridge.addIngredient("Paprika", Decimal(1.0), "tsp")
        self.a.freezer.addIngredient("Blueberries", Decimal(10.0), "berries")
        self.a.pantry.addIngredient("Beef", Decimal(1.0), "steak")
        self.a.misc.addIngredient("Ciabatta", Decimal(1.0), "loaf")

        self.a.fridge.selectIngredient("Paprika", True)
        self.a.freezer.selectIngredient("Blueberries", True)
        self.a.pantry.selectIngredient("Beef", True)
        self.a.misc.selectIngredient("Ciabatta", True)
        self.a.getRecipeFromSelectedIngredients(5, None)

        for r in self.a.getRecipes():
            r.printAll()
            r.printMissed()

        self.assertEqual(len(self.a.getRecipes()), 5)

    def testAddIngredientOneNoDuplicates(self):
        self.a = App.Application()
        self.a.fridge = Frg.Fridge("Fridge")
        self.a.freezer = Frg.Fridge("Freezer")
        self.a.pantry = Frg.Fridge("Pantry")
        self.a.misc = Frg.Fridge("Misc")

        self.a.addIngredient("Paprika", Decimal(1.0), "tsp", "fridge")
        self.a.addIngredient("Blueberries", Decimal(10.0), "berries", "freezer")
        self.a.addIngredient("Raspberries", Decimal(10.0), "berries", "freezer")
        self.a.addIngredient("Beef", Decimal(1.0), "steak", "pantry")
        self.a.addIngredient("Pork", Decimal(1.0), "steak", "pantry")
        self.a.addIngredient("Lamb", Decimal(1.0), "steak", "pantry")
        self.a.addIngredient("Ciabatta", Decimal(1.0), "loaf", "misc")
        self.a.addIngredient("Brioche", Decimal(1.0), "loaf", "misc")
        self.a.addIngredient("Rye", Decimal(1.0), "loaf", "misc")
        self.a.addIngredient("Baguette", Decimal(1.0), "loaf", "misc")

        self.assertEqual(len(self.a.fridge.getIngredient()), 1)
        self.assertEqual(len(self.a.freezer.getIngredient()), 2)
        self.assertEqual(len(self.a.pantry.getIngredient()), 3)
        self.assertEqual(len(self.a.misc.getIngredient()), 4)

    def testAddIngredientOneDuplicates(self):
        self.a = App.Application()
        self.a.fridge = Frg.Fridge("Fridge")
        self.a.freezer = Frg.Fridge("Freezer")
        self.a.pantry = Frg.Fridge("Pantry")
        self.a.misc = Frg.Fridge("Misc")

        self.a.addIngredient("Paprika", Decimal(1.0), "tsp", "fridge")
        self.assertFalse(self.a.addIngredient("Paprika", Decimal(2.50), "tsp", "fridge"))
        self.assertEqual(len(self.a.fridge.getIngredient()), 1)

    def testAddIngredientTwoNoDuplicates(self):
        self.a = App.Application()
        self.a.fridge = Frg.Fridge("Fridge")
        self.a.freezer = Frg.Fridge("Freezer")
        self.a.pantry = Frg.Fridge("Pantry")
        self.a.misc = Frg.Fridge("Misc")

        i1 = Ing.Ingredient("Paprika", Decimal(1.0), "tsp")
        i2 = Ing.Ingredient("Blueberries", Decimal(10.0), "berries")
        i3 = Ing.Ingredient("Beef", Decimal(1.0), "steak")
        i4 = Ing.Ingredient("Ciabatta", Decimal(1.0), "loaf")

        self.a.addIngredientTwo(i1, "fridge")
        self.a.addIngredientTwo(i2, "freezer")
        self.a.addIngredientTwo(i3, "pantry")
        self.a.addIngredientTwo(i4, "misc")

        self.assertEqual(len(self.a.fridge.getIngredient()), 1)
        self.assertEqual(len(self.a.freezer.getIngredient()), 1)
        self.assertEqual(len(self.a.pantry.getIngredient()), 1)
        self.assertEqual(len(self.a.misc.getIngredient()), 1)

    def testAddIngredientTwoDuplicates(self):
        self.a = App.Application()
        self.a.fridge = Frg.Fridge("Fridge")
        self.a.freezer = Frg.Fridge("Freezer")
        self.a.pantry = Frg.Fridge("Pantry")
        self.a.misc = Frg.Fridge("Misc")

        i1 = Ing.Ingredient("Paprika", Decimal(1.0), "tsp")
        i2 = Ing.Ingredient("Blueberries", Decimal(10.0), "berries")
        i3 = Ing.Ingredient("Beef", Decimal(1.0), "steak")
        i4 = Ing.Ingredient("Ciabatta", Decimal(1.0), "loaf")

        self.a.addIngredientTwo(i1, "fridge")
        self.a.addIngredientTwo(i2, "freezer")
        self.a.addIngredientTwo(i3, "pantry")
        self.a.addIngredientTwo(i4, "misc")

        self.assertFalse(self.a.addIngredientTwo(i1, "fridge"))
        self.assertFalse(self.a.addIngredientTwo(i2, "freezer"))
        self.assertFalse(self.a.addIngredientTwo(i3, "pantry]"))
        self.assertFalse(self.a.addIngredientTwo(i4, "misc"))

        self.assertEqual(len(self.a.fridge.getIngredient()), 1)
        self.assertEqual(len(self.a.freezer.getIngredient()), 1)
        self.assertEqual(len(self.a.pantry.getIngredient()), 1)
        self.assertEqual(len(self.a.misc.getIngredient()), 1)

    def testGetSelected(self):
        self.a = App.Application()
        self.a.fridge = Frg.Fridge("Fridge")
        self.a.freezer = Frg.Fridge("Freezer")
        self.a.pantry = Frg.Fridge("Pantry")
        self.a.misc = Frg.Fridge("Misc")

        i1 = Ing.Ingredient("Paprika", Decimal(1.0), "tsp")
        i2 = Ing.Ingredient("Blueberries", Decimal(10.0), "berries")
        i3 = Ing.Ingredient("Beef", Decimal(1.0), "steak")
        i4 = Ing.Ingredient("Ciabatta", Decimal(1.0), "loaf")

        self.a.addIngredientTwo(i1, "fridge")
        self.a.addIngredientTwo(i2, "freezer")
        self.a.addIngredientTwo(i3, "pantry")
        self.a.addIngredientTwo(i4, "misc")

        self.a.fridge.selectIngredient("Paprika", True)
        self.a.freezer.selectIngredient("Blueberries", True)
        self.a.pantry.selectIngredient("Beef", True)
        self.a.misc.selectIngredient("Ciabatta", True)

        list_sel = self.a.getSelectedIngredients()
        self.assertEqual(len(list_sel), 4)
        print("EXPECTED NO.: 4")
        for a in list_sel:
            print(a.getName())

        self.a.pantry.selectIngredient("Beef", False)
        self.a.misc.selectIngredient("Ciabatta", False)

        list_sel = self.a.getSelectedIngredients()
        self.assertEqual(len(list_sel), 2)
        print("EXPECTED NO.: 2")
        for a in list_sel:
            print(a.getName())

    def testDeselectAll(self):
        self.a = App.Application()
        self.a.fridge = Frg.Fridge("Fridge")
        self.a.freezer = Frg.Fridge("Freezer")
        self.a.pantry = Frg.Fridge("Pantry")
        self.a.misc = Frg.Fridge("Misc")

        i1 = Ing.Ingredient("Paprika", Decimal(1.0), "tsp")
        i2 = Ing.Ingredient("Blueberries", Decimal(10.0), "berries")
        i3 = Ing.Ingredient("Beef", Decimal(1.0), "steak")
        i4 = Ing.Ingredient("Ciabatta", Decimal(1.0), "loaf")

        self.a.addIngredientTwo(i1, "fridge")
        self.a.addIngredientTwo(i2, "freezer")
        self.a.addIngredientTwo(i3, "pantry")
        self.a.addIngredientTwo(i4, "misc")

        self.a.fridge.selectIngredient("Paprika", True)
        self.a.freezer.selectIngredient("Blueberries", True)
        self.a.pantry.selectIngredient("Beef", True)
        self.a.misc.selectIngredient("Ciabatta", True)

        list_sel = self.a.getSelectedIngredients()
        self.assertEqual(len(list_sel), 4)

        self.a.deselectAll()

        list_sel = self.a.getSelectedIngredients()
        self.assertEqual(len(list_sel), 0)

    def testAddRemoveListToLists(self):
        self.a = App.Application()
        i1 = Ing.Ingredient("Paprika", Decimal(1.0), "tsp")
        i2 = Ing.Ingredient("Blueberries", Decimal(10.0), "berries")
        i3 = Ing.Ingredient("Beef", Decimal(1.0), "steak")
        i4 = Ing.Ingredient("Ciabatta", Decimal(1.0), "loaf")
        list_one = Lis.IngList()
        list_one.addIngredient(i1)
        list_one.addIngredient(i2)
        list_one.addIngredient(i3)
        list_one.addIngredient(i4)

        self.a.addListToLists(list_one)
        self.assertEqual(len(self.a.getLists()), 1)
        self.assertEqual(len(self.a.getLists()[0].getList()), 4)

        self.a.removeListFromLists(list_one)
        self.assertEqual(len(self.a.getLists()), 0)

    def testWipe(self):
        self.a = App.Application()
        self.a.fridge = Frg.Fridge("Fridge")
        self.a.freezer = Frg.Fridge("Freezer")
        self.a.pantry = Frg.Fridge("Pantry")
        self.a.misc = Frg.Fridge("Misc")

        i1 = Ing.Ingredient("Paprika", Decimal(1.0), "tsp")
        i2 = Ing.Ingredient("Blueberries", Decimal(10.0), "berries")
        i3 = Ing.Ingredient("Beef", Decimal(1.0), "steak")
        i4 = Ing.Ingredient("Ciabatta", Decimal(1.0), "loaf")

        self.a.addIngredientTwo(i1, "fridge")
        self.a.addIngredientTwo(i2, "freezer")
        self.a.addIngredientTwo(i3, "pantry")
        self.a.addIngredientTwo(i4, "misc")

        self.a.set_id("Test ID")
        self.a.set_has_id(True)

        list_one = Lis.IngList()
        list_one.addIngredient(i1)
        list_one.addIngredient(i2)
        list_one.addIngredient(i3)
        list_one.addIngredient(i4)

        self.a.addListToLists(list_one)
        self.a.wipe()
        self.assertEqual(len(self.a.fridge.getIngredient()), 0)
        self.assertEqual(len(self.a.freezer.getIngredient()), 0)
        self.assertEqual(len(self.a.pantry.getIngredient()), 0)
        self.assertEqual(len(self.a.misc.getIngredient()), 0)
        self.assertEqual(len(self.a.getLists()), 0)
        self.assertEqual(self.a.getId(), "")
        self.assertFalse(self.a.getHasChosenId())


if __name__ == '__main__':
    unittest.main()
