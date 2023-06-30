from tkinter import ttk

from .notebook_tabs.create_food.create_food_table_canvas import CreateFoodTableCanvas
from .notebook_tabs.stored_food.stored_food_tables_canvas import StoredFoodTablesCanvas
from .notebook_tabs.consumed_food.consumed_food_items_canvas import ConsumedFoodItemsCanvas
from .notebook_tabs.create_meal_template.create_meal_template_canvas import CreateMealTemplateCanvas
from .notebook_tabs.stored_meal_templates.stored_meal_templates_canvas import StoredMealTemplatesCanvas

from constants.constants import NotebookTabLabels


class MainNotebook:
    """Notebook which provides tabs for Ranah app
    
    Each Tab implies a Canvas widget implying a Frame child
    which holds all widgets and logic needed to implement the UI.
    """
    TAB_TYPES = (
        CreateFoodTableCanvas,
        StoredFoodTablesCanvas,
        ConsumedFoodItemsCanvas,
        CreateMealTemplateCanvas,
        StoredMealTemplatesCanvas,
    )

    TAB_LABELS = (
        e.value for e in NotebookTabLabels
    )

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.canvas_map = {}

        self._create_notebook(parent)
        self._initialize_tabs()

        self._bind_events()

    def _create_notebook(self, parent):
        self.notebook = ttk.Notebook(parent, padding=5)
        self.notebook.grid(row=0, column=0, sticky='news')
        # enable resizing
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)

    def _initialize_tabs(self):
        # TODO: enable switching between the tabs with Ctrl+PageUp/PageDown
        for tab, tab_label in zip(self.TAB_TYPES, self.TAB_LABELS):
            # create the tab
            canvas_tab = tab(self.notebook, self.db)
            self.notebook.add(canvas_tab.canvas, text=tab_label)
            self.canvas_map[tab_label] = canvas_tab

    def _bind_events(self):
        self.notebook.bind('<<NotebookTabChanged>>', lambda event: self._handle_tab_change(event))

    def _handle_tab_change(self, event):
        if event.widget.tab('current')['text'] == NotebookTabLabels.new_meal_template:
            self.canvas_map[NotebookTabLabels.new_meal_template].frame.update_food_label_names()

        elif event.widget.tab('current')['text'] == NotebookTabLabels.stored_meal_templates:
            self.canvas_map[NotebookTabLabels.stored_meal_templates].set_meal_template_names()

