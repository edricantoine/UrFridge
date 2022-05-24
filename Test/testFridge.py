import unittest
import Backend.Ingredient as Ing
import Backend.Fridge as Frg


class MyTestCase(unittest.TestCase):
    f = Frg.Fridge("My Fridge")

    def testAddIngredient(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", 12, "eggs")
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 12)

    def testRemoveIngredientStillLeft(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", 12, "eggs")
        self.f.removeIngredients("Eggs", 3)
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 9)

    def testRemoveIngredientBelowZero(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", 12, "eggs")
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 12)
        self.f.removeIngredients("Eggs", 15)
        self.assertEqual(len(self.f.getIngredient()), 0)

    def testRemoveIngredientNotExist(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", 12, "eggs")
        self.assertEqual(self.f.removeIngredients("Chicken", 3), -1)

    def testSelectExistingIngredient(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", 12, "eggs")
        self.f.selectIngredient("Eggs", True)
        self.assertTrue(self.f.getIngredient()[0].getSelected())
        self.f.selectIngredient("Eggs", False)
        self.assertFalse(self.f.getIngredient()[0].getSelected())

    def testSelectNonExistingIngredient(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", 12, "eggs")
        self.assertFalse(self.f.selectIngredient("Chicken", True))

