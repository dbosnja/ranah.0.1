"""Shared frames/widgets definitions

Usually these are leaf parts of an app. They have to be generic enough
for all possible use-cases.

Currently they are mostly self-contained, meaning that no public API
is exposed for maneuvering their properties, texts, grid position and so on.
This is a good starting point when bumping ranah to a new version.
"""

import re

from tkinter import ttk, DoubleVar

from constants.constants import text_constants


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
        self.ok_button = ttk.Button(self.frame, text=self.ok_text, command=self._grid_forget)
        self.message_lbl = ttk.Label(self.frame, text=self.message_text)
    
    def _grid_widgets(self):
        self.message_lbl.grid(row=0, column=0, pady=15, padx=5)
        self.ok_button.grid(row=1, column=0, pady=15, padx=5)
    
    def _grid_forget(self):
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


class NutritionTableResult:
    """"Frame for rendering one nutrition table/row"""

    # TODO: add configurable background color and enable resizing

    COL_COUNT = 12

    def __init__(self, parent):
        self.parent = parent
    
    def render_row(self, row, row_data):
        for i, data in enumerate(row_data):
            lbl = ttk.Label(self.parent, text=data, anchor='center', padding=(5))
            if row % 2 == 0:
                lbl.configure(background='#E3E7EA')
            else:
                lbl.configure(background='#ffffe6')
            lbl.grid(row=row, column=i, sticky='we')


class NutritionTableHeaders:
    """"Labels for rendering headers of nutrition tables"""

    text_constants = text_constants

    def __init__(self, parent, header_labels):
        self.parent = parent
        self.header_labels = header_labels
        self.label_widgets = []
        
        self._create_widgets()
        self._grid_widgets()

    def _create_styles(self):
        # TODO: expose this as a configurable option via public API
        self.nutrition_table_results_style = ttk.Style()
        self.nutrition_table_results_style.configure('NutritionTableResults.TFrame', background='#ade6e1')        
    
    def _create_widgets(self):
        for header_lbl in self.header_labels:
            lbl = ttk.Label(self.parent, text=header_lbl, borderwidth=1, relief='raised', padding=(0, 5, 0, 5), anchor='center')
            self.label_widgets.append(lbl)
    
    def _grid_widgets(self):
        for i, widget in enumerate(self.label_widgets):
            widget.grid(row=0, column=i, sticky='we')


class NutritionTableResultsFrame:
    """"Frame for rendering nutrition table with result(s)
    
    The frame is composed of headers, e.g. Fat, Carbs, Calories..
    and the table data associated with a particular food item.
    """
    text_constants = text_constants

    def __init__(self, parent, col_count):
        self.col_count = col_count
        self._create_styles()
        
        self.frame = ttk.Frame(parent, style='NutritionTableResults.TFrame')
        # enable resizing
        for i in range(self.col_count):
            self.frame.columnconfigure(i, weight=1)
            

    def _create_styles(self):
        # TODO: expose this as a configurable option via public API
        self.nutrition_table_results_style = ttk.Style()
        self.nutrition_table_results_style.configure('NutritionTableResults.TFrame', background='#ade6e1')
    
    def grid_frame(self, row, column, sticky):
        self.frame.grid(row=row, column=column, sticky=sticky)
    
    def grid_forget(self):
        self.frame.grid_forget()
    
    def configure_style(self, style_name):
        self.frame.configure(style=style_name)

    def render_headers(self, header_labels):
        headers_frame = NutritionTableHeaders(self.frame, header_labels)
    
    def render_results(self, food_tables):
        for i, food_table in enumerate(food_tables):
            row_frame = NutritionTableResult(self.frame)
            row_frame.render_row(i + 1, food_table)


class AddNewFoodItemFrame:
    """Frame representing a pop-up message for storing new (eaten) food item :)
    
    Renders `Add` and `Cancel` buttons.
    `Add` adds a new record(row) in ranah database and quits the pop-up, while
    the `Cancel` only does the latter
    """

    def __init__(self, parent, food_name=None, callback=None):
        self.parent = parent
        self.food_name = food_name
        self.callback = callback
        
        self.frame = ttk.Frame(parent, padding=(10), borderwidth=2, relief='ridge', style='AddFoodItem.TFrame')

        # define validations
        # TODO: DRY: isolate this validations in a separate function(I don't want inheritance for this) -> CreateFoodLabelFrame
        self.double_pattern = re.compile('^\d*\.?\d*$')
        self._validate_double = self.frame.register(self._validate_double_input), '%P'
        
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _create_styles(self):
        ttk.Style().configure('AddFoodItem.TFrame', background='#8d9f66')
    
    def _create_widget_vars(self):
        self.add_text = 'Dodaj'
        self.cancel_text = 'Obustavi'
        self.msg_text = f'Unesite količinu odabranog artikla u gramima i kliknute `{self.add_text}` ' \
                        f'za trajnu pohranu ili `{self.cancel_text}` za prekid.'
        self.food_weight_var = DoubleVar(value='')
    
    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.frame, text=self.food_name, background='white', anchor='center')
        self.msg_lbl = ttk.Label(self.frame, text=self.msg_text)
        self.add_button = ttk.Button(self.frame, text=self.add_text, command=self._add_new_food_item, state='disabled')
        self.cancel_btn = ttk.Button(self.frame, text=self.cancel_text, command=self._grid_forget)
        self.food_weight_entry = ttk.Entry(self.frame, validate='all', validatecommand=self._validate_double, textvariable=self.food_weight_var)
    
    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, pady=5, padx=5, columnspan=2)
        self.msg_lbl.grid(row=1, column=0, pady=(15, 20), padx=5, columnspan=2)
        self.food_weight_entry.grid(row=2, column=0, pady=10, padx=5, columnspan=2)
        self.add_button.grid(row=3, column=0, pady=5, padx=5, sticky='e')
        self.cancel_btn.grid(row=3, column=1, pady=5, padx=5, sticky='w')
    
    def _grid_forget(self):
        """Remove this frame from its parent mapping"""
        self.frame.grid_forget()
    
    def _add_new_food_item(self):
        if self.callback is None:
            print('I should not be writing this, but the callback is void, does it make sense to be None?')
        self.callback(food_item_weight=float(self.food_weight_var.get()))
        self._grid_forget()
        # TODO: add new leaf frame indicating successful storing message

    def _validate_double_input(self, entry_value):
        if not entry_value:
            self.add_button.state(['disabled'])
        if entry_value and self.double_pattern.match(entry_value) is None:
            return False
        elif entry_value and self.double_pattern.match(entry_value) is not None:
            self.add_button.state(['!disabled'])
            return True
        return True
