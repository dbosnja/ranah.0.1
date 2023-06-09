"""Shared frames/widgets definitions

Usually these are leaf parts of an app. They have to be generic enough
for all possible use-cases.

Currently they are mostly self-contained, meaning that generic public APIs
are exposed for maneuvering their properties, texts, grid position and so on.
"""


from tkinter import ttk


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


class FoodTableResult:
    """Labels for rendering one food table/row"""
    
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback
        self.all_row_data = []
    
    def render_row(self, row, row_data):
        bckgrnd_color = '#E3E7EA' if row % 2 == 0 else '#FFFFE6'
        # replace primary key with its number in the table
        row_data[0] = row
        for i, data in enumerate(row_data):
            lbl = ttk.Label(self.parent.frame, text=data, anchor='center', padding=(5), background=bckgrnd_color)
            lbl.grid(row=row, column=i, sticky='we')
            self.all_row_data.append(lbl)
        # change cursor for name dimension and attach an event to it
        self.all_row_data[1]['cursor'] = 'hand2'
        self.all_row_data[1].bind('<1>', lambda event: self.callback(event))
    
    def destroy_row(self):
        for rd in self.all_row_data:
            rd.destroy()
        self.all_row_data = []


class FoodTableHeaders:
    """Labels for rendering headers of food tables"""

    def __init__(self, parent, header_labels):
        self.parent = parent
        self.header_labels = header_labels
        self.label_widgets = []
        
        self._create_widgets()
        self._grid_widgets()

    def _create_widgets(self):
        for header_lbl in self.header_labels:
            lbl = ttk.Label(self.parent.frame, text=header_lbl, borderwidth=1, relief='raised', padding=(0, 5, 0, 5), anchor='center')
            self.label_widgets.append(lbl)
    
    def _grid_widgets(self):
        for i, widget in enumerate(self.label_widgets):
            widget.grid(row=0, column=i, sticky='we')


class FoodTableResultsFrame:
    """Frame for rendering food table with result(s)
    
    The frame is composed of headers, e.g. Fat, Carbs, Calories..
    and the table data associated with a particular food item.
    """

    def __init__(self, parent, table_headers):
        self.table_headers = table_headers
        self.col_count = len(table_headers)
        self.all_rows = []
        
        self._create_styles()
        self.frame = ttk.Frame(parent.frame, style='FoodTableResultsFrame.TFrame')
        # enable resizing
        for i in range(self.col_count):
            self.frame.columnconfigure(i, weight=1)

    def _create_styles(self):
        self.food_table_results_style = ttk.Style()
        self.food_table_results_style.configure('FoodTableResultsFrame.TFrame', background='#ade6e1')

    def grid_frame(self, row, column, sticky):
        self.frame.grid(row=row, column=column, sticky=sticky)
        # NOTE: gridding the whole table implies gridding the table headers as well;
        # gridding the table rows not though, due to the lazy loading architecture
        self.render_headers()
    
    def destroy_rows(self):
        """Destroy all widget rows"""
        for row in self.all_rows:
            row.destroy_row()
        self.all_rows = []
    
    def configure_style(self, style_name):
        self.frame.configure(style=style_name)

    def render_headers(self):
        # NOTE: Do I need to save the instance of the table headers?
        headers_frame = FoodTableHeaders(self, self.table_headers)
    
    def render_results(self, food_tables):
        for i, food_table in enumerate(food_tables):
            row_frame = FoodTableResult(self, self.row_callback)
            row_frame.render_row(i + 1, food_table)
            self.all_rows.append(row_frame)

    def set_row_callback(self, callback):
        """Set which callback will be called when user clicks on the name field in a row"""
        self.row_callback = callback

