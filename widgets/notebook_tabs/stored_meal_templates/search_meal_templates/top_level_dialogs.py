import re
from datetime import datetime

from tkinter import ttk, Toplevel, PhotoImage, StringVar

from constants.constants import consumed_food_headers, consumed_food_timestamp_map


class AddDialogTopLevel:
    """Description"""

    NORMATIVE = 100

    def __init__(self, parent, tmplt_name):
        self.parent = parent
        self.template_name =tmplt_name

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
        self.dialog_center.title('Dodaj predložak kao konzumiran')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x375+2500+370')
        self.dialog_center.minsize(600, 375)
        for col in range(4):
            self.dialog_center.columnconfigure(col, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())

    def _predefine_food_values(self):
        time_now = datetime.now()

        # strip starting zero for month and day so validation can work properly
        self.def_d = f'{time_now.day}'.lstrip('0')
        self.def_m = f'{time_now.month}'.lstrip('0')
        self.def_y = f'{time_now.year}'
        self.def_h = f'{time_now.hour}'
        self.def_min = f'{time_now.minute}'

        return [self.template_name] + [self.def_y, self.def_m, self.def_d, self.def_h, self.def_min]

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
        self.title_lbl_var = f'Unesite opcionalni postotak konzumiranja predloška\n`{self.template_name}`\ni opcionalno vrijeme konzumiranja'

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

        self.update_btn = ttk.Button(text='Dodaj', command=self._update_food_table, style='UpdateFoodTable.TButton', **self.mutual_button_options)
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
        self.parent._add_template(self)
        return
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


class DeleteDialogTopLevel:
    """Top level responsible for maneuvring deletion of a meal template"""

    def __init__(self, parent, tmplt_name):
        self.parent = parent
        self.template_name = tmplt_name

        self._initialize_dialog_window()

        self._create_mutual_button_options()

        # its children
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Trajno brisanje predloška')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x200+2450+500')
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
        self.title_lbl_var = f'Jeste li sigurni da želite trajno izbrisati predložak\n`{self.template_name}`?'

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
        self.parent._delete_template(self)


class DialogPickerTopLevel:
    """Main dialog window for operating with meal template row"""

    def __init__(self, parent, tmplt_name):
        self.parent = parent
        self.template_name = tmplt_name

        self._initialize_dialog_window()

        self._create_mutual_style_options()
        self._create_mutual_button_options()
        
        # its children
        self._create_styles()
        self._create_images()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Centar akcijâ')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'400x400+2600+300')
        self.dialog_center.minsize(400, 400)
        self.dialog_center.columnconfigure(0, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())
    
    def _create_styles(self):
        self.add_btn_style = ttk.Style()
        self.add_btn_style.configure('Add.TButton', **self.mutual_style_options)

        self.delete_btn_style = ttk.Style()
        self.delete_btn_style.configure('Delete.TButton', **self.mutual_style_options)

        self.close_btn_style = ttk.Style()
        self.close_btn_style.configure('Close.TButton', **self.mutual_style_options)
    
    def _create_images(self):
        self.add_img = PhotoImage(file='./assets/images/add_icon.png')
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
        self.title_lbl_var = f'Odaberite što želite napraviti s predloškom\n`{self.template_name}`'
    
    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2,
                                   relief='groove', background='#E57C2C', justify='center')

        self.add_btn = ttk.Button(text='Dodaj', image=self.add_img, style='Add.TButton',
                                  command=self._create_add_dialog, **self.mutual_button_options)
        self.delete_btn = ttk.Button(text='Izbriši', image=self.delete_img, style='Delete.TButton',
                                     command=self._create_delete_dialog, **self.mutual_button_options)
        self.close_btn = ttk.Button(text='Zatvori', image=self.close_img, style='Close.TButton',
                                    command=self.dialog_center.destroy, **self.mutual_button_options)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, sticky='we')

        self.add_btn.grid(row=1, column=0, pady=(50, 20))
        self.delete_btn.grid(row=2, column=0, pady=(0, 20))
        self.close_btn.grid(row=3, column=0)

    def _bind_events(self):
        ...

    def _create_delete_dialog(self):
        DeleteDialogTopLevel(self, self.template_name)

    def _create_add_dialog(self):
        AddDialogTopLevel(self, self.template_name)

    def _delete_template(self, delete_picker):
        self.parent.delete_template_permanently(self, delete_picker)

    def _add_template(self, add_picker):
        self.parent.add_template_as_consumed(self, add_picker)

