import codecs
import Backend.recipeGrabber as Grab
from kivy.app import App
from kivy.uix.label import Label


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
        label = Label(text="Testing",
                      size_hint=(.5, .5),
                      pos_hint={'center_x': .5, 'center_y': .5})
        self.grb = Grab.RecipeGrabber()

        return label


if __name__ == '__main__':
    app = Main()
    app.run()
