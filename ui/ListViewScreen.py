from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.list import TwoLineListItem
import backend.IngList as Lis
from typing import List


def openList(ll: Lis.IngList):
    toast("List to open here: " + ll.getName())
    pass


class ListViewScreen(Screen):
    lists: List[Lis.IngList]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.lists = []

    def initializeFromListList(self, l_list):
        self.ids.viewListScroll.clear_widgets()
        self.lists = l_list
        for ll in self.lists:
            self.ids.viewListScroll.add_widget(TwoLineListItem(text=ll.getName(),
                                                               secondary_text=str(len(ll.getList())) + " items",
                                                               on_release=lambda x, value=ll: openList(value)))


class ListDisplay(TwoLineListItem):
    lis: Lis.IngList

    def __init__(self, lis: Lis.IngList, **kwargs):
        super().__init__(**kwargs)
        self.lis = lis
