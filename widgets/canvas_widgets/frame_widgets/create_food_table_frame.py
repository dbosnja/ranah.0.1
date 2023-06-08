import re

from tkinter import ttk, StringVar, messagebox

from constants.constants import text_constants


class CreateFoodLabelFrame:
    """Frame for creating a new food item label
    
    This Frame consists of all widgets needed to implement UI for creating a new
    nutrition table of a food article. Those would be mostly Labels, Entries and Buttons.
    It also has access to database API in order to store changes permanently.

    The necessary conditions to create a new food table is to have a non-empty, non-duplicated
    food name and a price. Validations for float values are included.
    """
    
    text_constants = text_constants

    # has to be updated manually!
    COL_COUNT = 4
    
    def __init__(self, parent, db):
        self.db = db

        self._create_styles()
        
        # main frame the `self` is composed of
        self.frame = ttk.Frame(parent, style='Main.TFrame', borderwidth=2, relief='groove', padding=10)
        self.frame.grid(column=0, row=0, sticky='news')
        for i in range(self.COL_COUNT):
            self.frame.columnconfigure(i, weight=1)

        # define the validations
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
        ttk.Style().configure('Create.TButton', font='10')
    
    def _create_widget_vars(self):
        self.calory_var = StringVar()
        self.fat_var = StringVar()
        self.saturated_fat_var = StringVar()
        self.carbs_var = StringVar()
        self.sugar_var = StringVar()
        self.fiber_var = StringVar()
        self.proteins_var = StringVar()
        self.food_price_var = StringVar()
        self.food_name_var = StringVar()
        
        self.entry_vars = [
            self.calory_var, self.fat_var, self.saturated_fat_var,
            self.carbs_var, self.sugar_var, self.proteins_var,
            self.fiber_var, self.food_name_var, self.food_price_var,
        ]
    
    def _reset_widget_vars(self):
        for var in self.entry_vars:
            var.set('')
    
    def _parse_input_to_float(self, entry_input):
        """Parses and creates a float from a string

        If string is empty, returned value is .0.
        Otherwise, float() function is used. Since entry inputs are
        validated, the function must not raise an error.
        """
        return .0 if not entry_input else float(entry_input)

    def _create_new_record(self, *args):
        stripped_food_name = self.food_name_var.get().strip()
        
        # raise error if food name not defined
        if not stripped_food_name:
            messagebox.showerror(message='Ime artikla nije definirano!', title='Artikl bez imena')
            return
        
        # raise error if food name already present in Ranah
        if not self.db.is_food_name_unique(stripped_food_name):
            messagebox.showerror(message=f'Naziv artikla već postoji!\n`{stripped_food_name}`', title='Duplicirano ime artikla')
            return
        
        # raise error if food price not defined
        if not self.food_price_var.get():
            messagebox.showerror(message='Cijena artikla nije definirana!', title='Artikl bez cijene')
            return
        
        record = {
            'label_name': stripped_food_name,
            'calories': self._parse_input_to_float(self.calory_var.get()),
            'fat': self._parse_input_to_float(self.fat_var.get()),
            'saturated_fat': self._parse_input_to_float(self.saturated_fat_var.get()),
            'carbs': self._parse_input_to_float(self.carbs_var.get()),
            'sugars': self._parse_input_to_float(self.sugar_var.get()),
            'fiber': self._parse_input_to_float(self.fiber_var.get()),
            'proteins': self._parse_input_to_float(self.proteins_var.get()),
            'price': self._parse_input_to_float(self.food_price_var.get()),
        }
        self.db.insert_new_food_item_record(**record)
        self._reset_widget_vars()
        self._render_success_message(stripped_food_name)
    
    def _render_success_message(self, temp_food_name):
        messagebox.showinfo(title='Novi artikl kreiran',
                            message=f'Uspješno kreirana nova nutritivna tablica u ranahu\n`{temp_food_name}`')

    # TODO: bind ctrl+a event to every entry widget
    def _create_widgets(self):
        """Create all (direct) children widgets"""

        self.topic_lbl = ttk.Label(self.frame, text=self.text_constants['topic_lbl'], anchor='center', padding=15, width=500, font=8)
        
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

        self.fiber_lbl = ttk.Label(self.frame, text=self.text_constants['fiber_lbl'],
                                   anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.fiber_e = ttk.Entry(self.frame, textvariable=self.fiber_var, validate='all', validatecommand=self._validate_double,
                                 width=10, font='default 17')

        self.proteins_lbl = ttk.Label(self.frame, text=self.text_constants['protein_lbl'],
                                      anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.protein_e = ttk.Entry(self.frame, textvariable=self.proteins_var, validate='all', validatecommand=self._validate_double,
                                   width=10, font='default 17')
        
        self.food_price_lbl = ttk.Label(self.frame, text=self.text_constants['food_price_lbl'],
                                   anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.food_price_e = ttk.Entry(self.frame, textvariable=self.food_price_var, validate='all', validatecommand=self._validate_double,
                                 width=10, font='default 17')
        
        self.food_name_lbl = ttk.Label(self.frame, text=self.text_constants['food_name_lbl'],
                                       anchor='center', borderwidth=2, relief='groove', padding=5, font='10')
        self.food_name_e = ttk.Entry(self.frame, textvariable=self.food_name_var, width=50, font='default 17')
        
        self.create_btn = ttk.Button(self.frame, text=self.text_constants['create_btn'],
                                     command=self._create_new_record, padding=5, style='Create.TButton')
    
    def _grid_widgets(self):
        self.topic_lbl.grid(row=0, column=0, pady=(60, 100), columnspan=4, sticky='we')
        
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
        self.fiber_lbl.grid(row=3, column=2, sticky='en', padx=(0, 10), pady=(0, 10))
        self.fiber_e.grid(row=3, column=3, sticky='wn')

        self.proteins_lbl.grid(row=4, column=0, sticky='en', padx=(0, 10))
        self.protein_e.grid(row=4, column=1, sticky='wn')
        self.food_price_lbl.grid(row=4, column=2, sticky='en', padx=(0, 10), pady=(0, 10))
        self.food_price_e.grid(row=4, column=3, sticky='wn')
        
        self.food_name_lbl.grid(row=5, column=0, sticky='en', padx=(0, 10), pady=(0, 10))
        self.food_name_e.grid(row=5, column=1, sticky='wn', columnspan=3)
        
        self.create_btn.grid(row=6, column=1, pady=5, columnspan=2)

