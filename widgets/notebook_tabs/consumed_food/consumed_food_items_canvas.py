from tkinter import Canvas


class ConsumedFoodItemsCanvas:
    """description"""

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.canvas = Canvas(parent)
