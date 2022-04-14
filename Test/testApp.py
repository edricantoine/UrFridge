import unittest
import Backend.Application as App
import Backend.Fridge as Frg


class MyTestCase(unittest.TestCase):
    testapp = App.Application()

    def testAddFridge(self):
        self.assertEqual(len(self.testapp.getFridges()), 0)
        self.testapp.addFridge("Edric's Fridge")
        self.assertEqual(len(self.testapp.getFridges()), 1)
        self.assertEqual(self.testapp.getFridges()[0].getName(), "Edric's Fridge")
        self.testapp.addFridge("Aiden's Fridge")
        self.assertEqual(len(self.testapp.getFridges()), 2)
        self.assertEqual(self.testapp.getFridges()[1].getName(), "Aiden's Fridge")

    def testAddFridgeAlreadyExist(self):
        self.assertEqual(len(self.testapp.getFridges()), 0)
        self.testapp.addFridge("Edric's Fridge")
        self.assertEqual(len(self.testapp.getFridges()), 1)
        self.assertEqual(self.testapp.getFridges()[0].getName(), "Edric's Fridge")
        self.assertFalse(self.testapp.addFridge("Edric's Fridge"))

    def testRemoveFridge(self):
        self.assertEqual(len(self.testapp.getFridges()), 0)
        self.testapp.addFridge("Edric's Fridge")
        self.assertEqual(len(self.testapp.getFridges()), 1)
        self.assertEqual(self.testapp.getFridges()[0].getName(), "Edric's Fridge")
        self.testapp.addFridge("Aiden's Fridge")
        self.assertEqual(len(self.testapp.getFridges()), 2)
        self.assertEqual(self.testapp.getFridges()[1].getName(), "Aiden's Fridge")
        self.testapp.removeFridge("Edric's Fridge")
        self.assertEqual(len(self.testapp.getFridges()), 1)
        self.assertEqual(self.testapp.getFridges()[0].getName(), "Aiden's Fridge")

    def testRemoveFridgeNotExist(self):
        self.assertEqual(len(self.testapp.getFridges()), 0)
        self.testapp.addFridge("Edric's Fridge")
        self.assertEqual(len(self.testapp.getFridges()), 1)
        self.assertEqual(self.testapp.getFridges()[0].getName(), "Edric's Fridge")
        self.testapp.addFridge("Aiden's Fridge")
        self.assertEqual(len(self.testapp.getFridges()), 2)
        self.assertEqual(self.testapp.getFridges()[1].getName(), "Aiden's Fridge")
        self.assertFalse(self.testapp.removeFridge("Justin's Fridge"))


if __name__ == '__main__':
    unittest.main()
