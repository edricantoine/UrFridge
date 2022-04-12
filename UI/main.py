import codecs
import Backend.SpRecipeGrabber as Grab2
from kivy.app import App
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout


class myLayout(FloatLayout):
    pass


class Main(App):
    # all possible meal types
    mealTypes = ["All", "Breakfast", "Lunch", "Dinner", "Snack", "Teatime"]
    # all possible dish types
    dishTypes = ["All", "Alcohol-cocktail", "Biscuits and cookies", "Bread", "Cereals", "Condiments and sauces",
                 "Drinks",
                 "Desserts", "Egg", "Main course", "Omelet", "Pancake", "Preps", "Preserve", "Salad", "Sandwiches",
                 "Soup", "Starter"]
    # all possible regional cuisine types
    cuisineTypes = ["All", "American", "Asian", "British", "Caribbean", "Central Europe", "Chinese", "Eastern Europe",
                    "French", "Indian", "Italian", "Japanese", "Kosher", "Mediterranean", "Mexican", "Middle Eastern",
                    "Nordic", "South American", "South East Asian"]

    grb = None

    def build(self):
        grb = Grab2.SpRecipeGrabber()
        grb.grabRecipe()
        return myLayout()


if __name__ == '__main__':
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '740')
    app = Main()
    app.run()
