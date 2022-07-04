from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineListItem
import backend.IngList as Lis


class ListViewEditScreen(Screen):
    lis: Lis.IngList

    def __init__(self, **kw):
        super().__init__(**kw)
        self.lis = None

    def initializeFromList(self, lis: Lis.IngList):
        self.lis = lis
        self.ids.listNameLabel.text = self.lis.getName()
        self.ids.lveScroll.clear_widgets()
        for i in self.lis.getList():
            self.ids.lveScroll.add_widget(OneLineListItem(text=i.getName()))

