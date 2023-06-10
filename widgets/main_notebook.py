from tkinter import ttk

from .notebook_tabs.create_food.create_food_table_canvas import CreateFoodTableCanvas
from .notebook_tabs.stored_food.stored_food_tables_canvas import StoredFoodTablesCanvas
from .notebook_tabs.consumed_food.consumed_food_items_canvas import ConsumedFoodItemsCanvas


class MainNotebook:
    """Notebook which provides tabs for Ranah app
    
    Each Tab implies a Canvas widget implying a Frame child
    which holds all widgets and logic needed to implement the UI.
    """

    TABS = (
        CreateFoodTableCanvas,
        StoredFoodTablesCanvas,
        ConsumedFoodItemsCanvas,
    )

    TAB_LABELS = (
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
        self.notebook = ttk.Notebook(parent, padding=5)
        self.notebook.grid(row=0, column=0, sticky='news')
        # enable resizing
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)

    def _initialize_tabs(self):
        # TODO: enable switching between the tabs with Ctrol+PageUp/PageDown
        for tab, tab_label in zip(self.TABS, self.TAB_LABELS):
            # create the tab
            canvas_tab = tab(self.notebook, self.db)
            self.notebook.add(canvas_tab.canvas, text=tab_label)

