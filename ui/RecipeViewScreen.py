import functools

from kivy.uix.screenmanager import Screen

from ui.RecipeDisplay import RecipeDisplay
import backend.Recipe as Rec


def compareName(r1: Rec.Recipe, r2: Rec.Recipe):
    if r1.getName() < r2.getName():
        return -1
    elif r1.getName() > r2.getName():
        return 1
    else:
        return 0


def compareCals(r1: Rec.Recipe, r2: Rec.Recipe):
    if r1.getCalories() < r2.getCalories():
        return -1
    elif r1.getCalories() > r2.getCalories():
        return 1
    else:
        return 0


def compareMissed(r1: Rec.Recipe, r2: Rec.Recipe):
    if r1.getMCount() < r2.getMCount():
        return -1
    elif r1.getMCount() > r2.getMCount():
        return 1
    else:
        return 0


class RecipeViewScreen(Screen):
    recipes = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.recipes = []

    def initializeFromRecipesList(self, r_list):
        self.ids.viewScroll.clear_widgets()
        self.recipes = r_list
        for r in self.recipes:
            self.ids.viewScroll.add_widget(RecipeDisplay(r))

    def sortByName(self):
        self.ids.viewScroll.clear_widgets()
        self.recipes = sorted(self.recipes, key=functools.cmp_to_key(compareName))
        for r in self.recipes:
            self.ids.viewScroll.add_widget(RecipeDisplay(r))

    def sortByCals(self):
        self.ids.viewScroll.clear_widgets()
        self.recipes = sorted(self.recipes, key=functools.cmp_to_key(compareCals))
        for r in self.recipes:
            self.ids.viewScroll.add_widget(RecipeDisplay(r))

    def sortByMissed(self):
        self.ids.viewScroll.clear_widgets()
        self.recipes = sorted(self.recipes, key=functools.cmp_to_key(compareCals))
        for r in self.recipes:
            self.ids.viewScroll.add_widget(RecipeDisplay(r))
