import unittest
import backend.Ingredient as ing
from decimal import *


class MyTestCase(unittest.TestCase):
    i = ing.Ingredient("Eggs", 2, "eggs")

    def test_setQuantRelative(self):
        self.i = ing.Ingredient("Eggs", Decimal(2), "eggs")
        self.i.setQuantRelative(Decimal(3))
        self.assertEqual(self.i.getQuant(), 5)
        self.i.setQuantRelative(Decimal(-4))
        self.assertEqual(self.i.getQuant(), 1)
