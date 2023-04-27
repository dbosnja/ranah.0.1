"""Shared frames/widgets definitions

Usually these are leaf parts of an app. They have to be generic enough
for all possible use-cases.

Currently they are mostly self-contained, meaning that no public API
is exposed for maneuvering their properties, texts, grid position and so on.
This is a good starting point when bumping ranah to a new version.
"""

from tkinter import ttk

from .constants import text_constants


class SuccessfulLabelCreationFrame:
    """Leaf Frame
    
    Shows info when a new food label table was successfully created.
    """

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent, padding=(10), borderwidth=2, relief='ridge', style='Success.TFrame')
        
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _create_styles(self):
        ttk.Style().configure('Success.TFrame', background='#8d9f66')
    
    def _create_widget_vars(self):
        self.ok_text = 'Ok'
        self.message_text = 'Uspješno kreirana nova nutritivna tablica u Ranahu.'
    
    def _create_widgets(self):
        self.ok_button = ttk.Button(self.frame, text=self.ok_text, command=self._remove_widgets)
        self.message_lbl = ttk.Label(self.frame, text=self.message_text)
    
    def _grid_widgets(self):
        self.message_lbl.grid(row=0, column=0, pady=15, padx=5)
        self.ok_button.grid(row=1, column=0, pady=15, padx=5)
    
    def _remove_widgets(self):
        """Remove this frame from its parent mapping"""
        self.frame.grid_forget()


class ScrollBarWidget:
    """Scroll bar type"""

    def __init__(self, parent):
        """Create new scroll-bar and hook it to the parent in appropriate orientation"""
        self.scroll_bar = ttk.Scrollbar(parent)
    
    def attach_to_scrollable(self, scrollable_widget, orient='vertical'):
        if orient == 'horizontal':
            scrollable_widget.configure(xscrollcommand=self.scroll_bar.set)
            command = scrollable_widget.xview
        else:
            scrollable_widget.configure(yscrollcommand=self.scroll_bar.set)
            command = scrollable_widget.yview
        self.scroll_bar.configure(orient=orient, command=command)
    
    def grid(self, row, column, sticky=None, columnspan=None, padx=None, pady=None):
        self.scroll_bar.grid(row=row, column=column, sticky=sticky, columnspan=columnspan, pady=pady, padx=padx)


class NutritionTableResultFrame:
    """"Frame for rendering nutrition table with result(s)
    
    The frame is composed of headers, e.g. Fat, Carbs, Calories..
    and the table data associated with a particular food item.
    """

    text_constants = text_constants

    def __init__(self, parent):
        self._create_styles()
        
        self.frame = ttk.Frame(parent, style='NutritionTableResults.TFrame')
        # enable resizing
        for i in range(9):
            self.frame.columnconfigure(i, weight=1)
        self.grid_frame(row=4, column=0, sticky='we')

        self._create_widgets()
        self._grid_widgets()

    def _create_styles(self):
        # TODO: expose this as a configurable option via public API
        ttk.Style().configure('NutritionTableResults.TFrame', background='#ade6e1')
    
    def grid_frame(self, row=None, column=None, sticky=None):
        self.frame.grid(row=row or 4, column=column or 0, sticky=sticky or 'we')
    
    def _create_widgets(self):
        self.food_number_lbl = ttk.Label(self.frame, text='#', borderwidth=2, relief='raised', padding=8, anchor='center')
        self.food_name_lbl = ttk.Label(self.frame, text=self.text_constants['food_name_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.calories_lbl = ttk.Label(self.frame, text=self.text_constants['calory_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.fat_lbl = ttk.Label(self.frame, text=self.text_constants['fat_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.sat_fat_lbl = ttk.Label(self.frame, text=self.text_constants['sat_fat_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.carbs_lbl = ttk.Label(self.frame, text=self.text_constants['carb_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.sugar_lbl = ttk.Label(self.frame, text=self.text_constants['sugar_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.protein_lbl = ttk.Label(self.frame, text=self.text_constants['protein_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.fiber_lbl = ttk.Label(self.frame, text=self.text_constants['fiber_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
    
    def _grid_widgets(self):
        self.food_number_lbl.grid(row=0, column=0, padx=5, pady=10, sticky='we')
        self.food_name_lbl.grid(row=0, column=1, padx=5, pady=10, sticky='we')
        self.calories_lbl.grid(row=0, column=2, padx=5, pady=10, sticky='we')
        self.fat_lbl.grid(row=0, column=3, padx=5, pady=10, sticky='we')
        self.sat_fat_lbl.grid(row=0, column=4, padx=5, pady=10, sticky='we')
        self.carbs_lbl.grid(row=0, column=5, padx=5, pady=10, sticky='we')
        self.sugar_lbl.grid(row=0, column=6, padx=5, pady=10, sticky='we')
        self.protein_lbl.grid(row=0, column=7, padx=5, pady=10, sticky='we')
        self.fiber_lbl.grid(row=0, column=8, padx=5, pady=10, sticky='we')
    
    def grid_forget(self):
        self.frame.grid_forget()