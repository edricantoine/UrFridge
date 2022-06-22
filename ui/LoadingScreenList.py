from kivy.uix.screenmanager import Screen

from backend import IngList as Lis
from main import app


class LoadingScreenList(Screen):
    lis: Lis.IngList

    def __init__(self, lis: Lis.IngList, **kw):
        self.lis = lis
        super().__init__(**kw)

    def change_list(self, lis: Lis.IngList):
        self.lis = lis

    def on_enter(self):
        app.aap.getRecipeFromList(self.lis, app.numToGrab)
        app.sm.get_screen("Recipe List").initializeFromRecipesList(app.aap.getRecipes())
        app.sm.current = 'Recipe List'