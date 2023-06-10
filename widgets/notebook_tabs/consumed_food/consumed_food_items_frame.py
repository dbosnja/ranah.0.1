import datetime

from tkinter import ttk, StringVar

from ...utility_widgets.leaf_frames import FoodTableResultsFrame 
from constants.constants import consumed_food_headers

class ConsumedFoodItemsFrame:
    """Frame representing UI for searching consumed food at some point in time"""

    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self._create_styles()

        self.frame = ttk.Frame(parent.canvas, style='ConsumedFoodItems.TFrame')
        self.frame.grid(row=0, column=0, sticky='news')
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('ConsumedFoodItems.TFrame', background='#FFE6FF')

    def _create_widget_vars(self):
        pass

    def _create_widgets(self):
        self.search_btn = ttk.Button(self.frame, text='Search', command=self._search_foods)
        
        self.consumed_food_table_frame = FoodTableResultsFrame(self, consumed_food_headers.values())
        self.consumed_food_table_frame.configure_style('ConsumedFoodItems.TFrame')
        self.consumed_food_table_frame.set_row_callback(lambda _: ...)

    def _grid_widgets(self):
        self.search_btn.grid(row=0, column=0)
        self.consumed_food_table_frame.grid_frame(row=1, column=0, sticky='we')
    
    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda event: self.parent._handle_scroll_up(event))
        self.frame.bind('<Button-5>', lambda event: self.parent._handle_scroll_down(event))
    
    def _search_foods(self):
        self.consumed_foods = self.db.get_consumed_food_on_date(datetime.datetime.strptime('01-06-23', '%d-%m-%y'))
        self.consumed_food_table_frame.destroy_rows()
        self.consumed_food_table_frame.render_results(self.consumed_foods)

