from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast
import backend.IngList as Lis


class ListEditContent(BoxLayout):
    lis: Lis.IngList
    app = None
    c = None
    squirrel = None

    def __init__(self, l: Lis.IngList, app, c, squirrel, **kwargs):
        super().__init__(**kwargs)
        self.lis = l
        self.app = app
        self.c = c
        self.squirrel = squirrel

    def readInput(self):
        oldName = self.lis.getName()
        txt = self.ids.newListName.text
        if len(txt) < 1 or len(txt) > 10:
            toast("Invalid input entered.")
        else:
            self.lis.setName(str(txt))
            self.c.execute("""
                UPDATE lists
                SET name = ?
                WHERE name = ?
                AND owner = ?
            """, (txt, oldName, self.app.app.getId()))
            self.squirrel.commit()
            self.app.sm.get_screen("List View Edit").initializeFromList(self.lis)

        self.ids.newListName.text = ""
