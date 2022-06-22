from kivymd.uix.dialog import MDDialog

from backend import Fridge as Frg


class AddIngredientDialog(MDDialog):
    ferg = None

    # We act with a goal of achieving insignificant amounts of wacky antics
    def __init__(self, schlapp: Frg.Fridge, **kwargs):
        super().__init__(**kwargs)
        self.ferg = schlapp