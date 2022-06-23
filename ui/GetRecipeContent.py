from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast

from backend import Application as Apple
from ui.MainScreen import MainScreen

import http.client as httplib


def check_connectivity():
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()


class GetRecipeContent(BoxLayout):
    aap = Apple.Application
    ms: MainScreen

    def __init__(self, aap: Apple.Application, mss: MainScreen, app, **kwargs):
        super().__init__(**kwargs)
        self.aap = aap
        self.ms = mss
        self.app = app

    def readInput(self):
        amt = self.ids.numRecipes.text
        if amt == "" or len(amt) >= 2:
            toast("Invalid input.")
        else:
            selected = self.aap.getSelectedIngredients()
            numSelected = len(selected)
            if numSelected == 0:
                toast("Select some ingredients first!")
            else:
                if check_connectivity():
                    numToGrab = int(self.ids.numRecipes.text)
                    self.app.numToGrab = numToGrab
                    self.app.sm.current = 'Loading Screen'

                else:
                    toast("Please connect to the internet first.")

        self.ids.numRecipes.text = ""
