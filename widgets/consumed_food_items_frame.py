from tkinter import ttk, StringVar

from .leaf_frames import NutritionTableResultFrame


class ConsumedFoodItemsFrame:
    """Frame representing UI for searching consumed food at some point in time"""

    def __init__(self, parent, db):
        self.db = db
        self._create_styles()

        self.frame = ttk.Frame(parent, style='ConsumedFoodItems.TFrame', borderwidth=5, relief='raised')
        self.frame.grid(row=2, column=0, sticky='nwe', padx=10)
        # Finish
        self.frame.columnconfigure(0, weight=1)

        self.nutrition_table_frame = NutritionTableResultFrame(self.frame, food_weight=True)
        self.nutrition_table_frame.grid_frame(row=8, column=0, sticky='we', columnspan=2)
        self.nutrition_table_frame.configure_style('ConsumedFoodItems.TFrame')

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('ConsumedFoodItems.TFrame', background='#F7EDD4')
    
    def _create_widget_vars(self):
        self.topic_text = 'Unesite datum za koji želite pretražiti konzmiranu hranu.'
        
        self.year_var = StringVar()
        self.month_var = StringVar()
        self.day_var = StringVar()

        self.year_text = 'Godina'
        self.month_text = 'Mjesec'
        self.day_text = 'Dan'

        self.search_btn_text = 'Pretraži'

    def _create_widgets(self):
        self.topic_lbl = ttk.Label(self.frame, text=self.topic_text)
        
        self.year_entry = ttk.Entry(self.frame, textvariable=self.year_var)
        self.month_entry = ttk.Entry(self.frame, textvariable=self.month_var)
        self.day_entry = ttk.Entry(self.frame, textvariable=self.day_var)

        self.year_lbl = ttk.Label(self.frame, text=self.year_text)
        self.month_lbl = ttk.Label(self.frame, text=self.month_text)
        self.day_lbl = ttk.Label(self.frame, text=self.day_text)

        self.search_btn = ttk.Button(self.frame, text=self.search_btn_text)

    def _grid_widgets(self):
        self.topic_lbl.grid(row=0, column=0, pady=5, columnspan=2)

        self.year_lbl.grid(row=2, column=0, pady=(0, 5))
        self.month_lbl.grid(row=4, column=0, pady=(0, 5))
        self.day_lbl.grid(row=6, column=0, pady=(0, 5))
        
        self.year_entry.grid(row=1, column=0)
        self.month_entry.grid(row=3, column=0)
        self.day_entry.grid(row=5, column=0)

        self.search_btn.grid(row=7, column=0, pady=(5, 0))
    
    def _bind_events(self):
        ...