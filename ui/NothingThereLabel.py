from kivymd.uix.label import MDLabel


class NothingThereLabel(MDLabel):
    def __draw_shadow__(self, origin, end, context=None):
        pass