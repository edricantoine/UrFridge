import unittest
import Backend.Ingredient as Ing
import Backend.Fridge as Frg


class MyTestCase(unittest.TestCase):
    f = Frg.Fridge("My Fridge")

    def testAddIngredient(self):
        self.f.addIngredient("Eggs", 12)
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 12)

    def testRemoveIngredientStillLeft(self):
        self.f.addIngredient("Eggs", 12)
        self.f.removeIngredients("Eggs", 3)
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 9)

    def testRemoveIngredientBelowZero(self):
        self.f.addIngredient("Eggs", 12)
        self.assertEqual(len(self.f.getIngredient()), 1)
        self.assertEqual(self.f.getIngredient()[0].getName(), "Eggs")
        self.assertEqual(self.f.getIngredient()[0].getQuant(), 12)
        self.f.removeIngredients("Eggs", 15)
        self.assertEqual(len(self.f.getIngredient()), 0)

    def testRemoveIngredientNotExist(self):
        self.f.addIngredient("Eggs", 12)
        self.assertFalse(self.f.removeIngredients("Chicken", 3))

    def testSelectExistingIngredient(self):
        self.f.addIngredient("Eggs", 12)
        self.f.selectIngredient("Eggs", True)
        self.assertTrue(self.f.getIngredient()[0].getSelected())
        self.f.selectIngredient("Eggs", False)
        self.assertFalse(self.f.getIngredient()[0].getSelected())

    def testSelectNonExistingIngredient(self):
        self.f.addIngredient("Eggs", 12)
        self.assertFalse(self.f.selectIngredient("Chicken", True))

    def testGrabRecipe(self):
        self.f.addIngredient("Tomatoes", 12)
        self.f.addIngredient("Lettuce", 1)
        self.f.addIngredient("Apples", 3)
        self.f.addIngredient("Beef", 1)

        self.f.selectIngredient("Tomatoes", True)
        self.f.selectIngredient("Lettuce", True)
        self.f.selectIngredient("Apples", True)
        self.f.selectIngredient("Beef", True)

        self.f.getRecipeFromSelectedIngredients(3, None)
        for r in self.f.getRecipes():
            print(str(r[0]) + " " + r[1] + " " + str(r[2]) + " " + r[3])

        self.assertEqual(len(self.f.getRecipes()), 3)


if __name__ == '__main__':
    unittest.main()
