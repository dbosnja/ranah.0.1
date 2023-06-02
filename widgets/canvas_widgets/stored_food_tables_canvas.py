from tkinter import Canvas


class StoredFoodTablesCanvas:
    """description"""

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.canvas = Canvas(parent)
