import functools

from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.list import TwoLineListItem
import backend.IngList as Lis
from typing import List


def openList(ll: Lis.IngList, app):
    app.sm.get_screen("List View Edit").initializeFromList(ll)
    app.sm.current = "List View Edit"
    pass


def compareListName(l1: Lis.IngList, l2: Lis.IngList):
    if l1.getName() < l2.getName():
        return -1
    elif l1.getName() > l2.getName():
        return 1
    else:
        return 0


def compareListNum(l1: Lis.IngList, l2: Lis.IngList):
    if len(l1.getList()) < len(l2.getList()):
        return -1
    elif len(l1.getList()) > len(l2.getList()):
        return 1
    else:
        return 0


class ListViewScreen(Screen):
    lists: List[Lis.IngList]
    app = None

    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.lists = []
        self.app = app

    def initializeFromListList(self, l_list):
        self.ids.viewListScroll.clear_widgets()
        self.lists = l_list
        for ll in self.lists:
            self.ids.viewListScroll.add_widget(TwoLineListItem(text=ll.getName(),
                                                               secondary_text=str(len(ll.getList())) + " items",
                                                               on_release=lambda x, value=ll: openList(value,
                                                                                                       self.app)))

    def sortByName(self):
        self.ids.viewListScroll.clear_widgets()
        self.lists = sorted(self.lists, key=functools.cmp_to_key(compareListName))
        for ll in self.lists:
            self.ids.viewListScroll.add_widget(TwoLineListItem(text=ll.getName(),
                                                               secondary_text=str(len(ll.getList())) + " items",
                                                               on_release=lambda x, value=ll: openList(value,
                                                                                                       self.app)))

    def sortByNumIngredients(self):
        self.ids.viewListScroll.clear_widgets()
        self.lists = sorted(self.lists, key=functools.cmp_to_key(compareListNum))
        for ll in self.lists:
            self.ids.viewListScroll.add_widget(TwoLineListItem(text=ll.getName(),
                                                               secondary_text=str(len(ll.getList())) + " items",
                                                               on_release=lambda x, value=ll: openList(value,
                                                                                                       self.app)))


class ListDisplay(TwoLineListItem):
    lis: Lis.IngList

    def __init__(self, lis: Lis.IngList, **kwargs):
        super().__init__(**kwargs)
        self.lis = lis
