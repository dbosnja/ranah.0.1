import re

from tkinter import ttk, DoubleVar, StringVar, TclError, messagebox

from ...utility_widgets.leaf_frames import SuccessfulLabelCreationFrame
from ...constants.constants import text_constants


class CreateFoodLabelFrame:
    """Window for creating a new food item label"""
    
    text_constants = text_constants

    # has to be updated manually!
    ROW_COUNT = 6
    COL_COUNT = 4
    
    def __init__(self, parent, db):
        self.db = db

        self._create_styles()
        
        # main frame the `self` is composed of
        self.frame = ttk.Frame(parent, style='Main.TFrame', borderwidth=2, relief='groove', padding=10)
        self.frame.grid(column=0, row=0, sticky='news')
        for i in range(self.ROW_COUNT):
            self.frame.columnconfigure(i, weight=1)


        # define validations
        self.double_pattern = re.compile('^\d*\.?\d*$')
        self._validate_double = self.frame.register(self._validate_double_input), '%P'
        
        # init and render widgets
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
    
    def _validate_double_input(self, entry_value):
        if entry_value and self.double_pattern.match(entry_value) is None:
            return False
        return True

    def _create_styles(self):
        ttk.Style().configure('Main.TFrame', background='#CCFFCC')
    
    def _create_widget_vars(self):
        self.calory_var = DoubleVar(value='')
        self.fat_var = DoubleVar(value='')
        self.saturated_fat_var = DoubleVar(value='')
        self.carbs_var = DoubleVar(value='')
        self.sugar_var = DoubleVar(value='')
        self.proteins_var = DoubleVar(value='')
        self.fiber_var = DoubleVar(value='')
        self.food_name_var = StringVar(value='')
        self.food_price_var = StringVar(value='')
        
        self.widget_double_vars = [
            self.calory_var, self.fat_var, self.saturated_fat_var,
            self.sugar_var, self.carbs_var, self.proteins_var,
            self.fiber_var, self.food_price_var
        ]
        self.widget_string_vars = [
            self.food_name_var
        ]
    
    def _reset_widget_vars(self):
        for var in self.widget_double_vars + self.widget_string_vars:
            var.set('')
    
    def _create_new_record(self, *args):
        try:
            self.food_price_var.get()
        except TclError:
            self.food_price_var.set(.0)
        if not self.food_price_var.get():
            messagebox.showerror(message='Cijena artikla nije definirana!', title='Artikl bez cijene')
            return
        
        if not self.db.is_food_name_unique(self.food_name_var.get()):
            messagebox.showerror(message=f'Naziv artikla već postoji!\n`{self.food_name_var.get()}`', title='Duplicirano ime artikla')
            return
        
        for var in self.widget_double_vars:
            try:
                var.get()
            except TclError:
                var.set(.0)
        
        record = {
            'label_name': self.food_name_var.get(),
            'calories': self.calory_var.get(),
            'fat': self.fat_var.get(),
            'saturated_fat': self.saturated_fat_var.get(),
            'carbs': self.carbs_var.get(),
            'sugars': self.sugar_var.get(),
            'proteins': self.proteins_var.get(),
            'fiber': self.fiber_var.get(),
            'price': self.food_price_var.get(),
        }
        self.db.insert_new_food_item_record(**record)
        self._reset_widget_vars()
        self._render_success_message()
    
    def _render_success_message(self):
        # TODO: replace this with messagebox widget
        self.success_msg_frame = SuccessfulLabelCreationFrame(self.frame)
        self.success_msg_frame.frame.grid(row=4, column=0, rowspan=5, columnspan=2)

    # TODO: bind ctrl+a event to every entry widget
    def _create_widgets(self):
        """Create all (direct) children widgets"""

        self.topic_lbl = ttk.Label(self.frame, text=self.text_constants['topic_lbl'], anchor='center', padding=15, width=500)
        
        self.calory_lbl = ttk.Label(self.frame, text=self.text_constants['calory_lbl'],
                                    anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.calory_e = ttk.Entry(self.frame, textvariable=self.calory_var, validate='all', validatecommand=self._validate_double,
                                  width=10, font='default 17')
        
        self.fat_lbl = ttk.Label(self.frame, text=self.text_constants['fat_lbl'], 
                                 anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.fat_e = ttk.Entry(self.frame, textvariable=self.fat_var, validate='all', validatecommand=self._validate_double,
                               width=10, font='default 17')
        
        self.saturated_fat_lbl = ttk.Label(self.frame, text=self.text_constants['sat_fat_lbl'],
                                           anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.sat_fat_e = ttk.Entry(self.frame, textvariable=self.saturated_fat_var, validate='all', validatecommand=self._validate_double,
                                   width=10, font='default 17')
        
        self.carbs_lbl = ttk.Label(self.frame, text=self.text_constants['carb_lbl'],
                                   anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.carbs_e = ttk.Entry(self.frame, textvariable=self.carbs_var, validate='all', validatecommand=self._validate_double,
                                 width=10, font='default 17')
        
        self.sugar_lbl = ttk.Label(self.frame, text=self.text_constants['sugar_lbl'], 
                                   anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.sugar_e = ttk.Entry(self.frame, textvariable=self.sugar_var, validate='all', validatecommand=self._validate_double,
                                 width=10, font='default 17')
        
        self.proteins_lbl = ttk.Label(self.frame, text=self.text_constants['protein_lbl'],
                                      anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.protein_e = ttk.Entry(self.frame, textvariable=self.proteins_var, validate='all', validatecommand=self._validate_double,
                                   width=10, font='default 17')
        
        self.fiber_lbl = ttk.Label(self.frame, text=self.text_constants['fiber_lbl'],
                                   anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.fiber_e = ttk.Entry(self.frame, textvariable=self.fiber_var, validate='all', validatecommand=self._validate_double,
                                 width=10, font='default 17')
        
        self.food_price_lbl = ttk.Label(self.frame, text=self.text_constants['food_price_lbl'],
                                   anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.food_price_e = ttk.Entry(self.frame, textvariable=self.food_price_var, validate='all', validatecommand=self._validate_double,
                                 width=10, font='default 17')
        
        self.food_name_lbl = ttk.Label(self.frame, text=self.text_constants['food_name_lbl'],
                                       anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.food_name_e = ttk.Entry(self.frame, textvariable=self.food_name_var, width=50, font='default 17')
        
        self.create_btn = ttk.Button(self.frame, text=self.text_constants['create_btn'],
                                     command=self._create_new_record, padding=4)
    
    def _grid_widgets(self):
        self.topic_lbl.grid(row=0, column=0, pady=(20, 60), columnspan=4, sticky='we')
        
        self.calory_lbl.grid(row=1, column=0, sticky='en', padx=(0, 10), pady=(0, 10))
        self.calory_e.grid(row=1, column=1, sticky='wn')
        self.fat_lbl.grid(row=1, column=2, sticky='en', padx=(0, 10))
        self.fat_e.grid(row=1, column=3, sticky='wn')
        
        self.saturated_fat_lbl.grid(row=2, column=0, sticky='en', padx=(0, 10), pady=(0, 10))
        self.sat_fat_e.grid(row=2, column=1, sticky='wn')
        self.carbs_lbl.grid(row=2, column=2, sticky='en', padx=(0, 10))
        self.carbs_e.grid(row=2, column=3, sticky='wn')
        
        self.sugar_lbl.grid(row=3, column=0, sticky='en', padx=(0, 10), pady=(0, 10))
        self.sugar_e.grid(row=3, column=1, sticky='wn')
        self.proteins_lbl.grid(row=3, column=2, sticky='en', padx=(0, 10))
        self.protein_e.grid(row=3, column=3, sticky='wn')
        
        self.fiber_lbl.grid(row=4, column=0, sticky='en', padx=(0, 10), pady=(0, 10))
        self.fiber_e.grid(row=4, column=1, sticky='wn')
        self.food_price_lbl.grid(row=4, column=2, sticky='en', padx=(0, 10), pady=(0, 10))
        self.food_price_e.grid(row=4, column=3, sticky='wn')
        
        self.food_name_lbl.grid(row=5, column=0, sticky='en', padx=(0, 10), pady=(0, 10))
        self.food_name_e.grid(row=5, column=1, sticky='wn', columnspan=3)
        
        self.create_btn.grid(row=6, column=1, pady=5, columnspan=2)
