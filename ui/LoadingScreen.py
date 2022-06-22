from kivy.uix.screenmanager import Screen


class LoadingScreen(Screen):

    def __init__(self, app, **kw):
        self.app = app
        super().__init__(**kw)

    def on_enter(self):
        self.app.aap.getRecipeFromSelectedIngredients(app.numToGrab, None)
        self.app.sm.get_screen("Recipe List").initializeFromRecipesList(app.aap.getRecipes())
        self.app.sm.current = 'Recipe List'
