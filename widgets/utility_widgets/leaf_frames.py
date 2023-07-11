"""Shared frames/widgets definitions

Usually these are leaf parts of an app. They have to be generic enough
for all possible use-cases.

Currently they are mostly self-contained, meaning that generic public APIs
are exposed for maneuvering their properties, texts, grid position and so on.
"""

from functools import partial

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
    
    def __init__(self, parent):
        self.parent = parent
        self.all_row_data = []
    
    def render_row(self, row, row_data, events_map, events_map_pkey):
        """Render a row in the food table and attach specific event handler"""

        # NOTE: could have been configurable color
        bckgrnd_color = '#E3E7EA' if row % 2 == 0 else '#FFFFE6'

        # save primary key since it's used in the callbacks to distinguish between the rows
        self.p_key = row_data[0]
        # replace primary key with its row number in the table
        row_data = [row] + row_data[1:]

        # NOTE: Have to use here `partial`, otherwise `ev_handler` reference will point to
        # the last value left in the iteration, ie all lambdas will call the same callback
        em_pkey = {
            event: partial(lambda _, event_handler: event_handler(self.p_key), event_handler=ev_handler)
            for event, ev_handler in events_map_pkey.items()
        }
        em = {
            event: partial(lambda event, event_handler: event_handler(event), event_handler=ev_handler)
            for event, ev_handler in events_map.items()
        }
        events_map = {**em_pkey, **em}
        for i, data in enumerate(row_data):
            lbl = ttk.Label(self.parent.frame, text=data, background=bckgrnd_color, **self.MUTUAL_LABEL_OPTIONS)
            lbl.grid(row=row, column=i, sticky='we')
            # apply events and event handlers
            for event, event_handler in events_map.items():
                lbl.bind(event, event_handler)
            self.all_row_data.append(lbl)

    def render_tally_row(self, row, tally_row_data, events_map):
        # TODO: decide on the color of the tally row
        bckgrnd_color = '#E3E7EA' if row % 2 == 0 else '#FFFFE6'
        events_map = {
            event: partial(lambda event, event_handler: event_handler(event), event_handler=ev_handler)
            for event, ev_handler in events_map.items()
        }
        for i, data in enumerate(tally_row_data):
            lbl = ttk.Label(self.parent.frame, text=data, background=bckgrnd_color, anchor='center', padding=5)
            lbl.grid(row=row, column=i, sticky='we')
            # apply events and event handlers
            for event, event_handler in events_map.items():
                lbl.bind(event, event_handler)
            self.all_row_data.append(lbl)

    def destroy_row(self):
        for rd in self.all_row_data:
            rd.destroy()
        self.all_row_data = []

    @property
    def primary_key(self):
        return self.p_key


class FoodTableHeaders:
    """Labels for rendering headers of food tables"""

    def __init__(self, parent, header_labels):
        self.parent = parent
        self.header_labels = header_labels
        self.label_widgets = []
        self.marked_column = None

    def render_headers(self, events_map):
        events_map = {
            event: partial(lambda event, event_handler: event_handler(event), event_handler=ev_handler)
            for event, ev_handler in events_map.items()
        }
        for i, header_lbl in enumerate(self.header_labels):
            lbl = ttk.Label(self.parent.frame, text=header_lbl, borderwidth=1, relief='raised', padding=(0, 5, 0, 5), anchor='center')
            # apply events and event handlers
            for event, event_handler in events_map.items():
                lbl.bind(event, event_handler)
            lbl.grid(row=0, column=i, sticky='we')
            self.label_widgets.append(lbl)

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

        # Headers Frame
        self.headers_frame = FoodTableHeaders(self, self.table_headers)
        
        self._bind_events()

    def _create_styles(self):
        self.food_table_results_style = ttk.Style()
        self.food_table_results_style.configure('FoodTableResultsFrame.TFrame', background='#FFE6FF')

    def grid_frame(self, row, column, sticky):
        self.frame.grid(row=row, column=column, sticky=sticky)

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

    def render_headers(self, header_events):
        self.headers_frame.render_headers(header_events)
    
    def render_results(self, food_tables, row_events, row_events_pkey):
        for i, food_table in enumerate(food_tables):
            row = FoodTableResult(self)
            row.render_row(i + 1, food_table, row_events, row_events_pkey)
            self.all_rows.append(row)

    def render_result(self, food_table, row_events={}, row_events_pkey={}):
        """Render one result at the end of the table"""

        row = FoodTableResult(self)
        self.all_rows.append(row)
        row.render_row(len(self.all_rows), food_table, row_events, row_events_pkey)

    def render_result_at(self, idx, food_table, row_events={}, row_events_pkey={}):
        """Render one result at the position `idx`"""

        row = FoodTableResult(self)
        row.render_row(idx + 1, food_table, row_events, row_events_pkey)
        self.all_rows.insert(idx, row)

    def destroy_row(self, p_key):
        """Destroy the row with primary key corresponding with `p_key`"""

        for i, row in enumerate(self.all_rows):
            if row.primary_key == p_key:
                idx = i
                break
        self.all_rows[idx].destroy_row()
        self.all_rows.pop(idx)

    def render_tally_row(self, tally_row, events_map={}):
        if tally_row is None:
            # idempotent operation
            return
        self.tally_row = FoodTableResult(self)
        self.tally_row.render_tally_row(len(self.all_rows) + 1, tally_row, events_map)

    def mark_column(self, col_id, col_color=None):
        self.headers_frame.mark_column(col_id, col_color)

    def unmark_column(self):
        self.headers_frame.unmark_column()

    def _bind_events(self):
        self.frame.bind('<Configure>', lambda _: self.parent.parent.handle_resizing())

