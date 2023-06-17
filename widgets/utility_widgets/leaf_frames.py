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

    MUTUAL_LABEL_OPTIONS = {
        'anchor': 'center',
        'padding': 5,
        'cursor': 'hand2',
    }
    
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        self.all_row_data = []
    
    def render_row(self, row, row_data):
        bckgrnd_color = '#E3E7EA' if row % 2 == 0 else '#FFFFE6'
        # save primary key since it's used in the callbacks to distinguish between the rows
        self.p_key = row_data[0]
        # replace primary key with its row number in the table
        row_data = [row] + row_data[1:]
        for i, data in enumerate(row_data):
            lbl = ttk.Label(self.parent.frame, text=data, background=bckgrnd_color, **self.MUTUAL_LABEL_OPTIONS)
            lbl.grid(row=row, column=i, sticky='we')
            lbl.bind('<Button-4>', lambda _: self.parent.scroll_up_handler())
            lbl.bind('<Button-5>', lambda _: self.parent.scroll_down_handler())
            if self.callback is not None:
                lbl.bind('<1>', lambda _: self.callback(self.p_key))
            self.all_row_data.append(lbl)

    def render_tally_row(self, row, tally_row_data):
        # TODO: decide on the color of the tally row
        bckgrnd_color = '#E3E7EA' if row % 2 == 0 else '#FFFFE6'
        for i, data in enumerate(tally_row_data):
            lbl = ttk.Label(self.parent.frame, text=data, background=bckgrnd_color, anchor='center', padding=5)
            lbl.grid(row=row, column=i, sticky='we')
            self.all_row_data.append(lbl)

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
        self.marked_column = None
        
        self._create_widgets()
        self._grid_widgets()

    def _create_widgets(self):
        for header_lbl in self.header_labels:
            lbl = ttk.Label(self.parent.frame, text=header_lbl, borderwidth=1, relief='raised', padding=(0, 5, 0, 5), anchor='center')
            lbl.bind('<Button-4>', lambda _: self.parent.scroll_up_handler())
            lbl.bind('<Button-5>', lambda _: self.parent.scroll_down_handler())
            self.label_widgets.append(lbl)
    
    def _grid_widgets(self):
        for i, widget in enumerate(self.label_widgets):
            widget.grid(row=0, column=i, sticky='we')

    def mark_column(self, col_id, col_color=None):
        """Mark sorting column with a different color, ie. `col_color`"""

        col_color = col_color if col_color is not None else 'red'

        if self.marked_column is None:
            self.marked_column = col_id
            self.label_widgets[self.marked_column]['background'] = col_color

        # If the current marked column is about to change, set that one to system's default.
        elif self.marked_column is not None and self.marked_column != col_id:
            self.label_widgets[self.marked_column]['background'] = ''
            self.marked_column = col_id
            self.label_widgets[self.marked_column]['background'] = col_color

    def unmark_column(self):
        """Unmark sorting column, if any."""

        if self.marked_column is not None:
            self.label_widgets[self.marked_column]['background'] = ''
            self.marked_column = None


class FoodTableResultsFrame:
    """Frame for rendering food table with result(s)
    
    The frame is composed of headers, e.g. Fat, Carbs, Calories..
    and the table data associated with a particular food item.
    """

    def __init__(self, parent, table_headers):
        self.parent = parent
        self.table_headers = table_headers
        self.col_count = len(table_headers)
        self.all_rows = []
        self.tally_row = None
        
        self._create_styles()
        self.frame = ttk.Frame(parent.frame, style='FoodTableResultsFrame.TFrame')
        # enable resizing
        for i in range(self.col_count):
            self.frame.columnconfigure(i, weight=1)
        
        self._bind_events()

    def _create_styles(self):
        self.food_table_results_style = ttk.Style()
        self.food_table_results_style.configure('FoodTableResultsFrame.TFrame', background='#FFE6FF')

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

    def destroy_tally_row(self):
        """Destroy the tally row"""

        if self.tally_row is None:
            # idempotent operation
            return
        self.tally_row.destroy_row()
        self.tally_row = None
    
    def configure_style(self, style_name):
        self.frame.configure(style=style_name)

    def render_headers(self):
        self.headers_frame = FoodTableHeaders(self, self.table_headers)
    
    def render_results(self, food_tables):
        for i, food_table in enumerate(food_tables):
            row = FoodTableResult(self, self.row_callback)
            row.render_row(i + 1, food_table)
            self.all_rows.append(row)

    def render_result(self, food_table):
        """Render one result at the end of the table"""

        row = FoodTableResult(self)
        self.all_rows.append(row)
        row.render_row(len(self.all_rows), food_table)

    def render_tally_row(self, tally_row):
        if tally_row is None:
            # idempotent operation
            return
        self.tally_row = FoodTableResult(self)
        self.tally_row.render_tally_row(len(self.all_rows) + 1, tally_row)

    def mark_column(self, col_id, col_color=None):
        self.headers_frame.mark_column(col_id, col_color)

    def unmark_column(self):
        self.headers_frame.unmark_column()

    def set_row_callback(self, callback):
        """Set which callback will be called when user clicks on the name field in a row"""
        self.row_callback = callback
    
    def set_scroll_up_handler(self, callback):
        self.scroll_up_handler = callback
    
    def set_scroll_down_handler(self, callback):
        self.scroll_down_handler = callback
    
    def _bind_events(self):
        self.frame.bind('<Configure>', lambda _: self.parent.parent.handle_resizing())

