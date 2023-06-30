from tkinter import ttk

from .search_options_frame import SearchOptionsFrame


class SearchMealTemplatesFrame:
    """Main Frame for searchin, sorting and rendering meal templates.
    
    Frame has 3 Frame children.
    
    First Frame is in charge of representing UI and logic for searching all
    stored meal templates.

    Second Frame is in charge of sorting options.

    Third Frame handles rendering of meal templates in a table-like diplay.
    """

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self._create_styles()

        self.frame = ttk.Frame(parent.canvas, style='SearchMealTemplates.TFrame', borderwidth=10, relief='flat', padding=20)
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('SearchMealTemplates.TFrame', background='black')
    
    def _create_widget_vars(self):
        ...
    
    def _create_widgets(self):
        self.search_options_frame = SearchOptionsFrame(self, self.db)
    
    def _grid_widgets(self):
        self.search_options_frame.grid(row=0, column=0, sticky='we')
    
    def _bind_events(self):
        ...