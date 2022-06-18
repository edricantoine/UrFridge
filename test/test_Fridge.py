import unittest
import backend.Ingredient as Ing
import backend.Fridge as Frg
from decimal import *


class MyTestCase(unittest.TestCase):
    f = Frg.Fridge("My Fridge")

    def testAddIngredient(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12.0), "eggs")
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 12.0)

    def testAddIngredientTwo(self):
        self.f = Frg.Fridge("My Fridge")
        i = Ing.Ingredient("Soy Sauce", Decimal(1.0), "bottle")
        self.f.addIngredientTwo(i)
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Soy Sauce")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 1.0)

    def testIncreaseIngredientExisting(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12), "eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 12)
        self.f.increaseIngredient("Eggs", Decimal(2))
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 14)

    def testIncreaseIngredientNotExisting(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12), "eggs")
        self.assertFalse(self.f.increaseIngredient("Burrito", Decimal(100)))

    def testRemoveIngredientStillLeft(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12), "eggs")
        self.f.removeIngredients("Eggs", Decimal(3))
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 9)

    def testRemoveIngredientBelowZero(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12), "eggs")
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 12)
        self.f.removeIngredients("Eggs", Decimal(15))
        self.assertEqual(len(self.f.getIngredient()), 0)

    def testRemoveIngredientNotExist(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12), "eggs")
        self.assertEqual(self.f.removeIngredients("Chicken", Decimal(3)), -1)

    def testSelectExistingIngredient(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12), "eggs")
        self.f.selectIngredient("Eggs", True)
        self.assertTrue(self.f.getIngredient()[0].getSelected())
        self.f.selectIngredient("Eggs", False)
        self.assertFalse(self.f.getIngredient()[0].getSelected())

    def testSelectNonExistingIngredient(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12), "eggs")
        self.assertFalse(self.f.selectIngredient("Chicken", True))

    def testVerifyIngredient(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12.0), "eggs")
        self.assertFalse(self.f.verifyIngredient("Eggs"))
        self.assertTrue(self.f.verifyIngredient("Chimichurri"))

    def testGetSelectedIngredients(self):
        self.f = Frg.Fridge("My Fridge")
        self.f.addIngredient("Eggs", Decimal(12), "eggs")
        self.f.selectIngredient("Eggs", True)
        self.f.addIngredient("Apples", Decimal(12), "apples")
        self.f.selectIngredient("Apples", True)
        self.f.addIngredient("Bananas", Decimal(12), "bananas")
        self.f.selectIngredient("Bananas", True)

        list_sel = self.f.getSelectedIngredients()
        self.assertEqual(len(list_sel), 3)
        self.f.selectIngredient("Bananas", False)
        list_sel = self.f.getSelectedIngredients()
        self.assertEqual(len(list_sel), 2)

