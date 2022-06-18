import unittest
import backend.Ingredient as Ing
import backend.IngList as Lis
from decimal import *


class MyTestCase(unittest.TestCase):
    i = Lis.IngList()

    def testAddIngredient(self):
        self.i = Lis.IngList()
        i1 = Ing.Ingredient("mangoes", Decimal(1.0), "fruit")
        i2 = Ing.Ingredient("papayas", Decimal(2.0), "fruits")
        i3 = Ing.Ingredient("watermelons", Decimal(12304.12), "fruits")

        self.i.addIngredient(i1)
        self.i.addIngredient(i2)
        self.i.addIngredient(i3)

        self.assertEqual(len(self.i.getList()), 3)
