from tkinter import ttk

from .canvas_widgets import CreateFoodTableCanvas, StoredFoodTablesCanvas, ConsumedFoodItemsCanvas


class MainNotebook:
    """Notebook which provides tabs for Ranah app
    
    Each Tab implies a Canvas widget implying a Frame child
    which holds all widgets and logic needed to implement the UI.
    """

    TABS = (
        CreateFoodTableCanvas,
        StoredFoodTablesCanvas,
        ConsumedFoodItemsCanvas
    )

    TABS_LABELS = (
        'Nova nutritivna tablica',
        'Sve nutritivne tablice',
        'Konzumirana hrana',
    )

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self._create_notebook(parent)
        self._initialize_tabs()
        
    
    def _create_notebook(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=0, column=0, sticky='news')
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)
    
    def _initialize_tabs(self):
        for tab, tab_label in zip(self.TABS, self.TABS_LABELS):
            # create the tab
            canvas_tab = tab(self.notebook, self.db)
            self.notebook.add(canvas_tab.canvas, text=tab_label)
