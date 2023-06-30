from tkinter import ttk


class SearchOptionsFrame:
    """Description"""

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db  # NOTE: not sure if this one needs the database operand

        self.frame = ttk.Frame(parent.frame, style='SearchMealTemplates.TFrame')
        # enable resizing - TODO: or more
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_widget_vars(self):
        ...
    
    def _create_widgets(self):
        ...
    
    def _grid_widgets(self):
        ...
    
    def _bind_events(self):
        ...
    
    def grid(self, row, column, sticky='we'):
        self.frame.grid(row=row, column=column, sticky=sticky)
