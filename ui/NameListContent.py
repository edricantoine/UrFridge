import json

from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast

from backend import Application as Apple, IngList as Lis


class NameListContent(BoxLayout):
    aap = Apple.Application

    def __init__(self, aap: Apple.Application, app, c, squirrel, **kwargs):
        super().__init__(**kwargs)
        self.aap = aap
        self.app = app
        self.c = c
        self.squirrel = squirrel

    def readInput(self):
        liste = Lis.IngList()
        for i in self.app.app.getSelectedIngredients():
            liste.addIngredient(i)
        name = self.ids.listName.text
        if self.app.app.setListName(liste, name):
            self.app.app.addListToLists(liste)
            listeNames = []
            for i in liste.main_list:
                listeNames.append(i.getName())
            self.c.execute("""
                        INSERT INTO lists(name, contents, owner)
                        VALUES(?, ?, ?)
                        """, (name, json.dumps(listeNames), self.app.app.getId()))
            self.squirrel.commit()
            toast("List added successfully!")
        else:
            toast("You already have a list with that name.")

        self.ids.listName.text = ""
        for l in self.app.app.getLists():
            print(l.getName())

