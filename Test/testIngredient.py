import unittest
import Backend.Ingredient as ing


class MyTestCase(unittest.TestCase):
    i = ing.Ingredient("Eggs", 2)

    def test_setQuantRelative(self):
        self.i.setQuantRelative(3)
        self.assertEqual(self.i.getQuant(), 5)
        self.i.setQuantRelative(-4)
        self.assertEqual(self.i.getQuant(), 1)


if __name__ == '__main__':
    unittest.main()
