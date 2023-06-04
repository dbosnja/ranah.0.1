import re
from datetime import date

from tkinter import ttk, StringVar

from .leaf_frames import NutritionTableResultsFrame


class ConsumedFoodItemsFrame:
    """Frame representing UI for searching consumed food at some point in time"""

    def __init__(self, parent, db):
        self.db = db
        self._create_styles()

        self.frame = ttk.Frame(parent, style='ConsumedFoodItems.TFrame', borderwidth=5, relief='raised')
        self.frame.grid(row=2, column=0, sticky='nwe', padx=10)
        # enable resizing
        self.frame.columnconfigure(0, weight=1)
        # for i in range(9):
        #     self.frame.rowconfigure(i, weight=1)
            

        self.nutrition_table_frame = NutritionTableResultsFrame(self.frame, food_weight=True)
        self.nutrition_table_frame.grid_frame(row=8, column=0, sticky='we', columnspan=2)
        self.nutrition_table_frame.configure_style('ConsumedFoodItems.TFrame')

        # validations
        self.validate_year = self.frame.register(self._validate_year), '%P'
        self.validate_month = self.frame.register(self._validate_month), '%P'
        self.validate_day = self.frame.register(self._validate_day), '%P'

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('ConsumedFoodItems.TFrame', background='#F7EDD4')
    
    def _validate_year(self, year_value):
        # no regex party
        if len(year_value) == 1:
            return year_value == '2'
        elif len(year_value) == 2:
            # century
            return year_value == '20'
        elif len(year_value) == 3:
            # decade
            return year_value[2].isdigit() and year_value[2] >= '2'
        elif len(year_value) == 4:
            return year_value[3].isdigit()
        elif len(year_value) > 4:
            return False
        
        return True
    
    def _validate_month(self, month_value):
        # still no regex party
        if len(month_value) == 1:
            return month_value.isdigit()
        elif len(month_value) == 2:
            if month_value[0] == '0':
                return month_value[1].isdigit() and month_value[1] >= '1'
            elif month_value[0] == '1':
                return month_value[1] in ('0', '1', '2')
            else:
                return False
        elif len(month_value) > 2:
            return False
        
        return True

    def _validate_day(self, day_value):
        if len(day_value) == 1:
            return bool(re.match('\d{1}', day_value))
        elif len(day_value) == 2:
            return bool(re.match('(0[1-9])|((1|2)\d)|(3[0,1])', day_value))
        elif len(day_value) > 2:
            return False
        return True
    
    def _create_widget_vars(self):
        self.topic_text = 'Unesite datum za koji želite pretražiti konzumiranu hranu.'
        
        self.year_var = StringVar()
        self.month_var = StringVar()
        self.day_var = StringVar()

        self.year_text = 'Godina'
        self.month_text = 'Mjesec'
        self.day_text = 'Dan'

        self.search_btn_text = 'Pretraži'

    def _create_widgets(self):
        self.topic_lbl = ttk.Label(self.frame, text=self.topic_text)
        
        # TODO: refactor this part to dropdown lists
        self.year_entry = ttk.Entry(self.frame, textvariable=self.year_var, validate='all', validatecommand=self.validate_year)
        self.month_entry = ttk.Entry(self.frame, textvariable=self.month_var, validate='all', validatecommand=self.validate_month)
        self.day_entry = ttk.Entry(self.frame, textvariable=self.day_var, validate='all', validatecommand=self.validate_day)

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
        self.search_btn.configure(command=self._search_consumed_food)
    
    def _search_consumed_food(self):
        # TODO: user must not pass all 3 values here; only one is required to do the query -> ranah1.0
        y, m, d = self.year_var.get(), self.month_var.get().zfill(2), self.day_var.get().zfill(2)
        try:
            # TODO: padd left with zeros, only months and days
            target_date = date.fromisoformat(f'{y}-{m}-{d}')
        except ValueError:
            # TODO: create message panel explaining the error
            ...
        consumed_foods_on_date = self.db.get_consumed_food_on_date(target_date)
        self._render_consumed_food(consumed_foods_on_date)
    
    def _render_consumed_food(self, consumed_food):
        # TODO: refactor; this method should rely on internal method of the NutritionTableResultsFrame
        # NOTE: Repetition of code already! :) (stored_food_labels_frame.py)
        
        # first clear all rendered results(if any)
        self.nutrition_table_frame.grid_forget()
        
        # re-render the table headers
        self.nutrition_table_frame = NutritionTableResultsFrame(self.frame, food_weight=True)
        self.nutrition_table_frame.grid_frame(row=8, column=0, sticky='we', columnspan=2)
        self.nutrition_table_frame.configure_style('ConsumedFoodItems.TFrame')

        if not consumed_food:
            return

        consumed_food_sums = [len(consumed_food), 'Sve zajedno']

        for i, _ in enumerate(consumed_food[0]):
            # NOTE: terrible; this will go away once the method is internalized
            if i in (0, 1, len(consumed_food[0]) - 1):
                continue
            consumed_food_sums.append(sum(food[i] for food in consumed_food))

        for col_idx, val in enumerate(consumed_food_sums):
                # TODO: make this try/except clause a bit less painful, ie remove it completely
                try:
                    val = round(float(val), 2)
                except ValueError:
                    ...
                lbl = ttk.Label(self.nutrition_table_frame.frame, text=val, borderwidth=2,
                                relief='raised', padding=8, anchor='center', background='#ffffcc')
                lbl.grid(row=1, column=col_idx, padx=5)
            
