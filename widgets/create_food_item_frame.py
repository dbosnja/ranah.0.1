import re

from tkinter import ttk, DoubleVar, StringVar, TclError

from .leaf_frames import SuccessfulLabelCreationFrame


class CreateFoodItemFrame:
    """Window for creating a new food item label
    
    It is a direct (first) child of the root Window manager.
    """
    text_constants = {
        'topic_lbl': 'Nutritivne vrijednosti na 100 grama',
        'calory_lbl': 'Kalorije',
        'fat_lbl': 'Masti',
        'sat_fat_lbl': 'Zasićene masti',
        'carb_lbl': 'Ugljikohidrati',
        'sugar_lbl': 'Šećeri',
        'protein_lbl': 'Bjelančevine',
        'fiber_lbl': 'Vlakna',
        'food_name_lbl': 'Ime',
        'create_btn': 'Kreiraj',
    }
    def __init__(self, parent, db):
        self.db = db
        
        # main frame the `self` is composed of
        self.frame = ttk.Frame(parent, style='Main.TFrame', borderwidth=5, relief='raised')
        self.frame.grid(column=0, row=0, sticky='wen', padx=10)
        self.frame.columnconfigure(0, weight=1, minsize=50)
        self.frame.columnconfigure(1, weight=1, minsize=50)

        # define validations
        self.double_pattern = re.compile('^\d*\.?\d*$')
        self._validate_double = (self.frame.register(self._validate_double_input), '%P')
        self._validate_food_name = (self.frame.register(self._validate_food_name_input), '%P')
        
        # init and render widgets
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
    
    def _validate_double_input(self, entry_value):
        if entry_value == '.':
            return True
        if entry_value and self.double_pattern.match(entry_value) is None:
            return False
        return True
    
    def _validate_food_name_input(self, food_name):
        # TODO: don't check against db on every keystroke
        # at least not until it's indexed
        if food_name and self.db.is_food_name_unique(food_name):
            self.create_btn.state(['!disabled'])
            return True
        self.create_btn.state(['disabled'])
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
        
        self.widget_double_vars = [
            self.calory_var, self.fat_var, self.saturated_fat_var,
            self.sugar_var, self.carbs_var, self.proteins_var,
            self.fiber_var
        ]
        self.widget_string_vars = [
            self.food_name_var
        ]
    
    def _reset_widget_vars(self):
        for var in self.widget_double_vars + self.widget_string_vars:
            var.set('')
    
    def _create_new_record(self, *args):
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
        }
        self.db.insert_new_food_item_record(**record)
        self._reset_widget_vars()
        self._render_success_message()
    
    def _render_success_message(self):
        self.success_msg_frame = SuccessfulLabelCreationFrame(self.frame)
        self.success_msg_frame.frame.grid(row=4, column=0, rowspan=5, columnspan=2)

    # TODO: bind ctrl+a event to every entry widget
    def _create_widgets(self):
        """Create all (direct) children widgets"""

        self.topic_lbl = ttk.Label(self.frame, text=self.text_constants['topic_lbl'], anchor='center')
        
        self.calory_lbl = ttk.Label(self.frame, text=self.text_constants['calory_lbl'],
                                    anchor='center', borderwidth=2, relief='groove', padding=(5))
        self.calory_e = ttk.Entry(self.frame, textvariable=self.calory_var, validate='all', validatecommand=self._validate_double)
        
        self.fat_lbl = ttk.Label(self.frame, text=self.text_constants['fat_lbl'], 
                                 anchor='center', borderwidth=2, relief='groove', padding=(5))
        self.fat_e = ttk.Entry(self.frame, textvariable=self.fat_var, validate='all', validatecommand=self._validate_double)
        
        self.saturated_fat_lbl = ttk.Label(self.frame, text=self.text_constants['sat_fat_lbl'],
                                           anchor='center', borderwidth=2, relief='groove', padding=(5))
        self.sat_fat_e = ttk.Entry(self.frame, textvariable=self.saturated_fat_var, validate='all', validatecommand=self._validate_double)
        
        self.carbs_lbl = ttk.Label(self.frame, text=self.text_constants['carb_lbl'],
                                   anchor='center', borderwidth=2, relief='groove', padding=(5))
        self.carbs_e = ttk.Entry(self.frame, textvariable=self.carbs_var, validate='all', validatecommand=self._validate_double)
        
        self.sugar_lbl = ttk.Label(self.frame, text=self.text_constants['sugar_lbl'], 
                                   anchor='center', borderwidth=2, relief='groove', padding=(5))
        self.sugar_e = ttk.Entry(self.frame, textvariable=self.sugar_var, validate='all', validatecommand=self._validate_double)
        
        self.proteins_lbl = ttk.Label(self.frame, text=self.text_constants['protein_lbl'],
                                      anchor='center', borderwidth=2, relief='groove', padding=(5))
        self.protein_e = ttk.Entry(self.frame, textvariable=self.proteins_var, validate='all', validatecommand=self._validate_double)
        
        self.fiber_lbl = ttk.Label(self.frame, text=self.text_constants['fiber_lbl'],
                                   anchor='center', borderwidth=2, relief='groove', padding=(5))
        self.fiber_e = ttk.Entry(self.frame, textvariable=self.fiber_var, validate='all', validatecommand=self._validate_double)
        
        self.food_name_lbl = ttk.Label(self.frame, text=self.text_constants['food_name_lbl'],
                                       anchor='center', borderwidth=2, relief='groove', padding=(5))
        self.food_name_e = ttk.Entry(self.frame, textvariable=self.food_name_var,
                                     validate='all', validatecommand=self._validate_food_name)
        
        self.create_btn = ttk.Button(self.frame, text=self.text_constants['create_btn'],
                                     command=self._create_new_record, state='disabled')
    
    def _grid_widgets(self):
        self.topic_lbl.grid(row=0, column=0, pady=20, columnspan=2)
        self.calory_lbl.grid(row=1, column=0)
        self.calory_e.grid(row=1, column=1, pady=10)
        self.fat_lbl.grid(row=2, column=0)
        self.fat_e.grid(row=2, column=1, pady=10)
        self.saturated_fat_lbl.grid(row=3, column=0)
        self.sat_fat_e.grid(row=3, column=1, pady=10)
        self.carbs_lbl.grid(row=4, column=0)
        self.carbs_e.grid(row=4, column=1, pady=10)
        self.sugar_lbl.grid(row=5, column=0)
        self.sugar_e.grid(row=5, column=1, pady=10)
        self.proteins_lbl.grid(row=6, column=0)
        self.protein_e.grid(row=6, column=1, pady=10)
        self.fiber_lbl.grid(row=7, column=0)
        self.fiber_e.grid(row=7, column=1, pady=10)
        self.food_name_lbl.grid(row=8, column=0)
        self.food_name_e.grid(row=8, column=1, pady=10)
        self.create_btn.grid(row=9, column=1, pady=10)
