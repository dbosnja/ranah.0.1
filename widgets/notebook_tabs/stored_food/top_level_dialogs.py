import re
import datetime

from tkinter import ttk, Toplevel, PhotoImage, messagebox, StringVar

from constants.constants import (text_constants,
                                 nutrition_table_map,
                                 consumed_food_map,
                                 consumed_food_timestamp_map,
                                 consumed_food_headers)


class AddDialogTopLevel:
    """Description"""

    NORMATIVE = 100

    def __init__(self, parent, db, food_row):
        self.parent = parent
        self.db = db
        self.food_row = food_row
        self.label_name = food_row[nutrition_table_map['label_name']]
        self.row_p_key = food_row[nutrition_table_map['label_id']]

        self._initialize_dialog_window()

        self._define_regex()
        self.predefined_food_values = self._predefine_food_values()
        # define the validations
        self._define_validations()

        self._create_mutual_button_options()
        self._create_mutual_label_options()
        self._create_mutual_entry_options()

        # its children
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Dodaj konzumiranje prehrambenog artikla')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x375+2500+370')
        self.dialog_center.minsize(600, 375)
        for col in range(4):
            self.dialog_center.columnconfigure(col, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())

    def _predefine_food_values(self):
        time_now = datetime.datetime.now()

        # strip starting zero for month and day so validation can work properly
        self.def_d = f'{time_now.day}'.lstrip('0')
        self.def_m = f'{time_now.month}'.lstrip('0')
        self.def_y = f'{time_now.year}'
        self.def_h = f'{time_now.hour}'
        self.def_min = f'{time_now.minute}'

        return [self.label_name] + [self.def_y, self.def_m, self.def_d, self.def_h, self.def_min]

    def _define_regex(self):
        self.food_weight_with_dot_re = re.compile('^\d{,4}\.\d{,2}$')
        self.food_weight_wo_dot_re = re.compile('^\d{,4}$')

        self.consumed_time_re = re.compile('(\d{2})-(\d{2})-(\d{4}),\s*(\d{2}):(\d{2})')
        self.consumed_time_year_re = re.compile('^(^20?((2?[3-9]?)|([3-9]?[0-9]?))$)|(^2[1-9]?[0-9]?[0-9]?$)$')

        self.consumed_time_month_re = re.compile('^(^[1-9]$)|(^1[0-2]?$)$')
        self.consumed_time_day_re = re.compile('^([1-9]?$)|(^1[0-9]?$)|(^2[0-9]?$)|(^3[0-1]?$)$')

        self.consumed_time_hour_re = re.compile('^(^0[0-9]?$)|(^1[0-9]?$)|(^2[0-3]?$)$')
        self.consumed_time_minute_re = re.compile('^[0-5][0-9]?$')

    def _define_validations(self):
        self._validate_food_weight = self.dialog_center.register(self._validate_food_weight_input), '%P'
        self._validate_year = self.dialog_center.register(self._validate_year_input), '%P'
        self._validate_month = self.dialog_center.register(self._validate_month_input), '%P'
        self._validate_day = self.dialog_center.register(self._validate_day_input), '%P'
        self._validate_hour = self.dialog_center.register(self._validate_hour_input), '%P'
        self._validate_minute = self.dialog_center.register(self._validate_minute_input), '%P'

    def _validate_food_weight_input(self, entry_value):
        if entry_value:
            if '.' in entry_value and self.food_weight_with_dot_re.match(entry_value) is None:
                return False
            elif '.' not in entry_value and self.food_weight_wo_dot_re.match(entry_value) is None:
                return False
        return True

    def _validate_year_input(self, entry_value):
        if not entry_value:
            return False
        if entry_value and self.consumed_time_year_re.match(entry_value) is None:
            return False
        return True

    def _validate_month_input(self, entry_value):
        if entry_value and self.consumed_time_month_re.match(entry_value) is None:
            return False
        return True

    def _validate_day_input(self, entry_value):
        if entry_value and self.consumed_time_day_re.match(entry_value) is None:
            return False
        return True

    def _validate_hour_input(self, entry_value):
        if entry_value and self.consumed_time_hour_re.match(entry_value) is None:
            return False
        return True

    def _validate_minute_input(self, entry_value):
        if entry_value and self.consumed_time_minute_re.match(entry_value) is None:
            return False
        return True

    def _create_styles(self):
        self.add_btn_style = ttk.Style()
        self.add_btn_style.configure('UpdateFoodTable.TButton', font=(25), padding=(0, 5, 0, 5))
        self.add_btn_style.map('UpdateFoodTable.TButton', background=[('active', '#00994D')])

        self.cancel_btn_style = ttk.Style()
        self.cancel_btn_style.configure('CancelUpdate.TButton', font=(25), padding=(0, 5, 0, 5))
        self.cancel_btn_style.map('CancelUpdate.TButton', background=[('active', '#FF0000')])

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.dialog_center,
            'cursor': 'hand2',
        }

    def _create_mutual_label_options(self):
        self.mutual_label_options = {
            'master': self.dialog_center,
            'anchor': 'center',
            'borderwidth': 2,
            'relief': 'groove',
            'padding': 5,
            'font': '15',
        }

    def _create_mutual_entry_options(self):
        self.mutual_entry_options = {
            'master': self.dialog_center,
            'validate': 'key',
            'width': 10,
            'font': 'normal 17',
            'justify': 'center',
        }

    def _create_widget_vars(self):
        self.title_lbl_var = f'Unesite količinu konzumiranja za artikl\n`{self.label_name}`\ni opcionalno vrijeme konzumiranja'

        self.food_weight_var = StringVar()
        self.year_var = StringVar()
        self.month_var = StringVar()
        self.day_var = StringVar()
        self.hour_var = StringVar()
        self.minute_var = StringVar()

        self.food_name_var = StringVar()

        # NOTE: order is very important here
        self.widget_vars = (
            self.food_name_var, self.year_var, self.month_var,
            self.day_var, self.hour_var, self.minute_var
        )
        for w_var, food_value in zip(self.widget_vars, self.predefined_food_values):
            w_var.set(food_value)

    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2,
                                   relief='groove', background='#FFFFCC', justify='center')

        self.food_weight_lbl = ttk.Label(text=consumed_food_headers['food_weight'], **self.mutual_label_options)
        self.food_weight_e = ttk.Entry(textvariable=self.food_weight_var, validatecommand=self._validate_food_weight, **self.mutual_entry_options)
        self.food_weight_e.focus()
        self.year_lbl = ttk.Label(text=consumed_food_timestamp_map['year'], **self.mutual_label_options)
        self.year_e = ttk.Entry(textvariable=self.year_var, validatecommand=self._validate_year, **self.mutual_entry_options)

        self.month_lbl = ttk.Label(text=consumed_food_timestamp_map['month'], **self.mutual_label_options)
        self.month_e = ttk.Entry(textvariable=self.month_var, validatecommand=self._validate_month, **self.mutual_entry_options)
        self.day_lbl = ttk.Label(text=consumed_food_timestamp_map['day'], **self.mutual_label_options)
        self.day_e = ttk.Entry(textvariable=self.day_var, validatecommand=self._validate_day, **self.mutual_entry_options)

        self.hour_lbl = ttk.Label(text=consumed_food_timestamp_map['hour'], **self.mutual_label_options)
        self.hour_e = ttk.Entry(textvariable=self.hour_var, validatecommand=self._validate_hour, **self.mutual_entry_options)
        self.minute_lbl = ttk.Label(text=consumed_food_timestamp_map['minute'], **self.mutual_label_options)
        self.minute_e = ttk.Entry(textvariable=self.minute_var, validatecommand=self._validate_minute, **self.mutual_entry_options)

        self.food_name_lbl = ttk.Label(text=consumed_food_headers['food_name'], **self.mutual_label_options)
        self.food_name_e = ttk.Entry(self.dialog_center, textvariable=self.food_name_var, width=20,font='default 17', justify='center', state='readonly')

        self.update_btn = ttk.Button(text='Ažuriraj', command=self._update_food_table, style='UpdateFoodTable.TButton', **self.mutual_button_options)
        self.cancel_btn = ttk.Button(text='Odustani', command=self.dialog_center.destroy, style='CancelUpdate.TButton', **self.mutual_button_options)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, sticky='we', columnspan=4)

        self.food_weight_lbl.grid(row=1, column=0, sticky='we', padx=(10, 5), pady=(20, 5))
        self.food_weight_e.grid(row=1, column=1, sticky='we', padx=(5, 5), pady=(20, 5))
        self.year_lbl.grid(row=1, column=2, sticky='we', padx=(5, 5), pady=(20, 5))
        self.year_e.grid(row=1, column=3, sticky='we', padx=(5, 10), pady=(20, 5))

        self.month_lbl.grid(row=2, column=0, sticky='we', padx=(10, 5), pady=(10, 5))
        self.month_e.grid(row=2, column=1, sticky='we', padx=(5, 5), pady=(10, 5))
        self.day_lbl.grid(row=2, column=2, sticky='we', padx=(5, 5), pady=(10, 5))
        self.day_e.grid(row=2, column=3, sticky='we', padx=(5, 10), pady=(10, 5))

        self.hour_lbl.grid(row=3, column=0, sticky='we', padx=(10, 5), pady=(10, 5))
        self.hour_e.grid(row=3, column=1, sticky='we', padx=(5, 5), pady=(10, 5))
        self.minute_lbl.grid(row=3, column=2, sticky='we', padx=(5, 5), pady=(10, 5))
        self.minute_e.grid(row=3, column=3, sticky='we', padx=(5, 10), pady=(10, 5))

        self.food_name_lbl.grid(row=4, column=0, sticky='we', padx=(10, 5), pady=(10, 5))
        self.food_name_e.grid(row=4, column=1, sticky='we', columnspan=3, padx=(5, 10), pady=(10, 5))

        self.update_btn.grid(row=5, column=0, columnspan=2, sticky='e', padx=(0, 10), pady=(30, 0))
        self.cancel_btn.grid(row=5, column=2, columnspan=2, sticky='w', padx=(10, 0), pady=(30, 0))

    def _update_food_table(self):
        food_weight = self.food_weight_var.get()
        if not food_weight or food_weight == '.' or not float(food_weight):
            # idempotent operation for this conditions
            self.dialog_center.destroy()
            return

        # update numeric values
        rescaled_values = self._rescale_values(food_weight)
        consumed_food = [self.food_row[consumed_food_map['food_name']]] + [float(food_weight)] + rescaled_values

        # update datetime values
        time_now = datetime.datetime.now()
        # if any of minute, hour, day or month empty, imply current time
        minute = self.minute_var.get() or time_now.minute
        hour = self.hour_var.get() or time_now.hour
        day = self.day_var.get() or time_now.day
        month = self.month_var.get() or time_now.month
        # the only valid input for the year is a 4digit string
        year = self.year_var.get() if len(self.year_var.get()) == 4 else time_now.year
        consumed_time = f'{day}-{month}-{year}, {hour}:{minute}:{time_now.second}:{time_now.microsecond}'
        consumed_time = datetime.datetime.strptime(consumed_time, '%d-%m-%Y, %H:%M:%S:%f')
        consumed_food.append(consumed_time)

        # create record for update operation; ignore primary key
        # not really best, but this is what I get when I allow children to write to DB
        record = {
            k: consumed_food[consumed_food_map[k] - 1]
            for k in list(consumed_food_map.keys())[1:]
        }
        self.db.create_new_consumed_food_item(**record)

        self.dialog_center.destroy()
        messagebox.showinfo(title='Konzumirani artikl ažuriran',
                            message=f'Uspješno dodano {food_weight}g proizvoda',
                            parent=self.parent.dialog_center)

    def _rescale_values(self, food_weight):
        food_weight = float(food_weight)
        scale_factor = round(food_weight / self.NORMATIVE, 2)
        # fetch the food table and scale the corresponding columns
        food_table = self.db.get_food_item_table(self.label_name)
        food_table = food_table[nutrition_table_map['calories']:nutrition_table_map['price'] + 1]
        food_table = [round(x * scale_factor, 2) for x in food_table]
        # cast to int wherever it makes sense to
        food_table = [int(x) if int(x) == x else x for x in food_table]
        return food_table


class UpdateDialogTopLevel:
    """Description"""

    def __init__(self, parent, db, label_name):
        self.parent = parent
        self.db = db
        self.label_name = label_name

        self._initialize_dialog_window()

        self.predefined_food_table = self.db.get_food_item_table(self.label_name)

        # define the validations
        self.double_pattern = re.compile('^\d{,4}\.?\d{,2}$')
        self._validate_double = self.dialog_center.register(self._validate_double_input), '%P'

        # its children
        self._create_styles()
        self._create_mutual_button_options()
        self._create_mutual_label_options()
        self._create_mutual_entry_options()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Ažuriraj prehrambeni artikl')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x400+2500+370')
        self.dialog_center.minsize(600, 400)
        for col in range(4):
            self.dialog_center.columnconfigure(col, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())

    def _create_styles(self):
        self.add_btn_style = ttk.Style()
        self.add_btn_style.configure('UpdateFoodTable.TButton', font=(25), padding=(0, 5, 0, 5))
        self.add_btn_style.map('UpdateFoodTable.TButton', background=[('active', '#00994D')])

        self.cancel_btn_style = ttk.Style()
        self.cancel_btn_style.configure('CancelUpdate.TButton', font=(25), padding=(0, 5, 0, 5))
        self.cancel_btn_style.map('CancelUpdate.TButton', background=[('active', '#FF0000')])

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.dialog_center,
            'cursor': 'hand2',
        }

    def _create_mutual_label_options(self):
        self.mutual_label_options = {
            'master': self.dialog_center,
            'anchor': 'center',
            'borderwidth': 2,
            'relief': 'groove',
            'padding': 5,
            'font': '15',
        }

    def _create_mutual_entry_options(self):
        self.mutual_entry_options = {
            'master': self.dialog_center,
            'validate': 'all',
            'validatecommand': self._validate_double,
            'width': 10,
            'font': 'normal 17',
            'justify': 'center',
        }

    def _create_widget_vars(self):
        self.title_lbl_var = f'Unesite odgovarajuće izmjene za artikl\n`{self.label_name}`'

        self.calory_var = StringVar()
        self.fat_var = StringVar()
        self.saturated_fat_var = StringVar()
        self.carbs_var = StringVar()
        self.sugar_var = StringVar()
        self.fiber_var = StringVar()
        self.proteins_var = StringVar()
        self.food_price_var = StringVar()
        self.food_name_var = StringVar()

        # NOTE: order is very important here
        self.widget_vars = (
            self.food_name_var, self.calory_var, self.fat_var, self.saturated_fat_var, self.carbs_var,
            self.sugar_var, self.fiber_var, self.proteins_var, self.food_price_var
        )
        predefined_food_labels = list(nutrition_table_map.keys())[1:-2]

        for w_var, map_key in zip(self.widget_vars, predefined_food_labels):
            w_var.set(self.predefined_food_table[nutrition_table_map[map_key]])

    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2,
                                   relief='groove', background='#FFFFCC', justify='center')

        self.calory_lbl = ttk.Label(text=text_constants['calory_lbl'], **self.mutual_label_options)
        self.calory_e = ttk.Entry(textvariable=self.calory_var, **self.mutual_entry_options)
        self.fat_lbl = ttk.Label(text=text_constants['fat_lbl'], **self.mutual_label_options)
        self.fat_e = ttk.Entry(textvariable=self.fat_var, **self.mutual_entry_options)
        
        self.saturated_fat_lbl = ttk.Label(text=text_constants['sat_fat_lbl'], **self.mutual_label_options)
        self.sat_fat_e = ttk.Entry(textvariable=self.saturated_fat_var, **self.mutual_entry_options)
        self.carbs_lbl = ttk.Label(text=text_constants['carb_lbl'], **self.mutual_label_options)
        self.carbs_e = ttk.Entry(textvariable=self.carbs_var, **self.mutual_entry_options)

        self.sugar_lbl = ttk.Label(text=text_constants['sugar_lbl'], **self.mutual_label_options)
        self.sugar_e = ttk.Entry(textvariable=self.sugar_var, **self.mutual_entry_options)
        self.fiber_lbl = ttk.Label(text=text_constants['fiber_lbl'], **self.mutual_label_options)
        self.fiber_e = ttk.Entry(textvariable=self.fiber_var, **self.mutual_entry_options)
        
        self.proteins_lbl = ttk.Label(text=text_constants['protein_lbl'], **self.mutual_label_options)
        self.protein_e = ttk.Entry(textvariable=self.proteins_var, **self.mutual_entry_options)
        self.food_price_lbl = ttk.Label(text=text_constants['food_price_lbl'], **self.mutual_label_options)
        self.food_price_e = ttk.Entry(textvariable=self.food_price_var, **self.mutual_entry_options)
        
        self.food_name_lbl = ttk.Label(text=text_constants['food_name_lbl'], **self.mutual_label_options)
        self.food_name_e = ttk.Entry(self.dialog_center, textvariable=self.food_name_var, width=20,font='default 17', justify='center', state='readonly')

        self.update_btn = ttk.Button(text='Ažuriraj', command=self._update_food_table, style='UpdateFoodTable.TButton', **self.mutual_button_options)
        self.cancel_btn = ttk.Button(text='Odustani', command=self.dialog_center.destroy, style='CancelUpdate.TButton', **self.mutual_button_options)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, sticky='we', columnspan=4)

        self.calory_lbl.grid(row=1, column=0, sticky='we', padx=(10, 5), pady=(20, 5))
        self.calory_e.grid(row=1, column=1, sticky='we', padx=(5, 5), pady=(20, 5))
        self.fat_lbl.grid(row=1, column=2, sticky='we', padx=(5, 5), pady=(20, 5))
        self.fat_e.grid(row=1, column=3, sticky='we', padx=(5, 10), pady=(20, 5))

        self.saturated_fat_lbl.grid(row=2, column=0, sticky='we', padx=(10, 5), pady=(10, 5))
        self.sat_fat_e.grid(row=2, column=1, sticky='we', padx=(5, 5), pady=(10, 5))
        self.carbs_lbl.grid(row=2, column=2, sticky='we', padx=(5, 5), pady=(10, 5))
        self.carbs_e.grid(row=2, column=3, sticky='we', padx=(5, 10), pady=(10, 5))

        self.sugar_lbl.grid(row=3, column=0, sticky='we', padx=(10, 5), pady=(10, 5))
        self.sugar_e.grid(row=3, column=1, sticky='we', padx=(5, 5), pady=(10, 5))
        self.fiber_lbl.grid(row=3, column=2, sticky='we', padx=(5, 5), pady=(10, 5))
        self.fiber_e.grid(row=3, column=3, sticky='we', padx=(5, 10), pady=(10, 5))

        self.proteins_lbl.grid(row=4, column=0, sticky='we', padx=(10, 5), pady=(10, 5))
        self.protein_e.grid(row=4, column=1, sticky='we', padx=(5, 5), pady=(10, 5))
        self.food_price_lbl.grid(row=4, column=2, sticky='we', padx=(5, 5), pady=(10, 5))
        self.food_price_e.grid(row=4, column=3, sticky='we', padx=(5, 10), pady=(10, 5))

        self.food_name_lbl.grid(row=5, column=0, sticky='we', padx=(10, 5), pady=(10, 5))
        self.food_name_e.grid(row=5, column=1, sticky='we', columnspan=3, padx=(5, 10), pady=(10, 5))

        self.update_btn.grid(row=6, column=0, columnspan=2, sticky='e', padx=(0, 10), pady=(30, 10))
        self.cancel_btn.grid(row=6, column=2, columnspan=2, sticky='w', padx=(10, 0), pady=(30, 10))

    def _validate_double_input(self, entry_value):
        if entry_value and self.double_pattern.match(entry_value) is None:
            return False
        return True

    def _update_food_table(self):
        # raise error if food price not defined
        if not self.food_price_var.get():
            messagebox.showerror(message='Cijena artikla nije definirana!',
                                 title='Artikl bez cijene', parent=self.dialog_center)
            return
        
        record = {
            'label_name': self.food_name_var.get(),
            'calories': self._parse_input_to_float(self.calory_var.get()),
            'fat': self._parse_input_to_float(self.fat_var.get()),
            'saturated_fat': self._parse_input_to_float(self.saturated_fat_var.get()),
            'carbs': self._parse_input_to_float(self.carbs_var.get()),
            'sugars': self._parse_input_to_float(self.sugar_var.get()),
            'fiber': self._parse_input_to_float(self.fiber_var.get()),
            'proteins': self._parse_input_to_float(self.proteins_var.get()),
            'price': self._parse_input_to_float(self.food_price_var.get()),
        }
        self.db.update_food_item_table(**record)
        self.parent.press_serch_button()
        self.dialog_center.destroy()
        messagebox.showinfo(title='Artikl ažuriran',
                            message=f'`{self.label_name}` uspješno ažuriran.',
                            parent=self.parent.dialog_center)

    def _parse_input_to_float(self, entry_input):
        """Parses and creates a float from a string

        If string is empty, returned value is .0.
        Otherwise, float() function is used. Since entry inputs are
        validated, the function must not raise an error.
        """
        return .0 if not entry_input else float(entry_input)


class DeleteDialogTopLevel:
    """Description"""
    def __init__(self, parent, db, label_name):
        self.parent = parent
        self.db = db
        self.label_name = label_name

        self._initialize_dialog_window()

        # its children
        self._create_styles()
        self._create_mutual_button_options()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Trajno brisanje prehrambenog artikla')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x200+2500+500')
        self.dialog_center.minsize(500, 200)
        self.dialog_center.columnconfigure(0, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())

    def _create_styles(self):
        self.yes_btn_style = ttk.Style()
        self.yes_btn_style.configure('Yes.TButton', font=(25), padding=(0, 5, 0, 5))
        self.yes_btn_style.map('Yes.TButton', background=[('active', '#00994D')])

        self.no_btn_style = ttk.Style()
        self.no_btn_style.configure('No.TButton', font=(25), padding=(0, 5, 0, 5))
        self.no_btn_style.map('No.TButton', background=[('active', '#FF0000')])

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.dialog_center,
            'cursor': 'hand2',
        }

    def _create_widget_vars(self):
        self.title_lbl_var = f'Jeste li sigurni da želite trajno izbrisati artikl\n`{self.label_name}`?'

    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2,
                                   relief='groove', background='#FFFFCC', justify='center')

        self.yes_btn = ttk.Button(text='Da', style='Yes.TButton', command=self._delete_food_name, **self.mutual_button_options)
        self.no_btn = ttk.Button(text='Ne', style='No.TButton', command=self.dialog_center.destroy, **self.mutual_button_options)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, sticky='we')

        self.yes_btn.grid(row=1, column=0, pady=(20, 20))
        self.no_btn.grid(row=2, column=0, pady=(0, 20))

    def _delete_food_name(self):
        self.db.delete_food_table(self.label_name)
        self.parent.press_serch_button()
        self.dialog_center.destroy()
        self.parent.dialog_center.destroy()
        messagebox.showinfo(title='Artikl trajno izbrisan',
                            message=f'Uspješno izbrisan `{self.label_name}`',
                            parent=self.parent.parent.frame)


class DialogPickerTopLevel:
    """Description"""
    def __init__(self, parent, db, food_row):
        self.parent = parent
        self.db = db
        self.label_name = food_row[nutrition_table_map['label_name']]
        self.food_row = food_row

        self._initialize_dialog_window()

        # its children
        self._create_mutual_style_options()
        self._create_styles()
        self._create_images()
        self._create_mutual_button_options()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Centar ažuriranja')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x400+2500+326')
        self.dialog_center.minsize(500, 500)
        self.dialog_center.columnconfigure(0, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())
    
    def _create_styles(self):
        self.add_btn_style = ttk.Style()
        self.add_btn_style.configure('Add.TButton', **self.mutual_style_options)
        
        self.update_btn_style = ttk.Style()
        self.update_btn_style.configure('Update.TButton', **self.mutual_style_options)

        self.delete_btn_style = ttk.Style()
        self.delete_btn_style.configure('Delete.TButton', **self.mutual_style_options)

        self.close_btn_style = ttk.Style()
        self.close_btn_style.configure('Close.TButton', **self.mutual_style_options)
    
    def _create_images(self):
        self.add_img = PhotoImage(file='./assets/images/add_icon.png')
        self.update_img = PhotoImage(file='./assets/images/update_icon.png')
        self.delete_img = PhotoImage(file='./assets/images/delete_icon.png')
        self.close_img = PhotoImage(file='./assets/images/close_icon.png')

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.dialog_center,
            'compound': 'left',
            'cursor': 'hand2',
        }

    def _create_mutual_style_options(self):
        self.mutual_style_options = {
            'font': (25),
            'background': '#FFE6F1',
            'space': 15,
            'padding': (0, 5, 0, 5),
        }
    
    def _create_widget_vars(self):
        self.title_lbl_var = f'Odaberite što želite napraviti s artiklom\n`{self.label_name}`'
    
    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2, relief='groove', background='#E57C2C', justify='center')
        
        self.add_btn = ttk.Button(text='Dodaj', image=self.add_img, style='Add.TButton',
                                  command=self._create_add_dialog, **self.mutual_button_options)
        self.update_btn = ttk.Button(text='Ažuriraj', image=self.update_img, style='Update.TButton',
                                     command=self._create_update_dialog, **self.mutual_button_options)
        self.delete_btn = ttk.Button(text='Izbriši', image=self.delete_img, style='Delete.TButton',
                                     command=self._create_delete_dialog, **self.mutual_button_options)
        self.close_btn = ttk.Button(text='Zatvori', image=self.close_img, style='Close.TButton',
                                    command=self.dialog_center.destroy, **self.mutual_button_options)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, sticky='we')
        
        self.add_btn.grid(row=1, column=0, pady=(50, 20))
        self.update_btn.grid(row=2, column=0, pady=(0, 20))
        self.delete_btn.grid(row=3, column=0, pady=(0, 20))
        self.close_btn.grid(row=4, column=0, pady=(0, 20))

    def _bind_events(self):
        pass

    def _create_delete_dialog(self):
        DeleteDialogTopLevel(self, self.db, self.label_name)

    def _create_add_dialog(self):
        AddDialogTopLevel(self, self.db, self.food_row)
    
    def _create_update_dialog(self):
        UpdateDialogTopLevel(self, self.db, self.label_name)

    def set_serch_button(self, callback):
        """Callback for invoking search button"""

        self.press_serch_button = callback