import webbrowser

from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import ThreeLineListItem

from backend import Recipe as Rec


class RecipeDisplay(MDCardSwipe):
    rec: Rec.Recipe

    def openInBrowser(self, x):
        webbrowser.open(self.rec.getUrl())

    def __init__(self, rec: Rec.Recipe, **kwargs):
        super().__init__(**kwargs)
        self.rec = rec
        self.ids.recFront.add_widget(ThreeLineListItem(text=self.rec.getName(),
                                                       secondary_text=str(self.rec.getCalories()) + " cal.",
                                                       tertiary_text="Missed ingredients: " + str(self.rec.getMCount()),
                                                       on_release=self.openInBrowser))