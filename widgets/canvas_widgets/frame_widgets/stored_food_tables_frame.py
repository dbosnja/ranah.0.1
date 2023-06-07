import re

from tkinter import ttk, StringVar, Toplevel, PhotoImage, messagebox

from constants.constants import text_constants
from ...utility_widgets import AddNewFoodItemFrame


class AddDialogTopLevel:
    """Description"""

    NORMATIVE = 100
    # NOTE: Not really the best way, but I'll live with it
    TABLE_DIMENSIONS = (
        'food_name',
        'food_weight',
        'calories',
        'fat',
        'saturated_fat',
        'carbs',
        'sugars',
        'fiber',
        'proteins',
        'price',
    )
    def __init__(self, parent, db, label_name):
        self.parent = parent
        self.db = db
        self.label_name = label_name

        self._initialize_dialog_window()

        # define the validations
        self.double_pattern = re.compile('^\d*\.?\d*$')
        self._validate_double = self.dialog_center.register(self._validate_double_input), '%P'

        # its children
        self._create_styles()
        self._create_mutual_button_options()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Dodaj konzumiranje prehrambenog artikla')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x250+2500+475')
        self.dialog_center.minsize(500, 250)
        self.dialog_center.columnconfigure(0, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())

    def _create_styles(self):
        self.add_btn_style = ttk.Style()
        self.add_btn_style.configure('AddWeight.TButton', font=(25), padding=(0, 5, 0, 5))
        self.add_btn_style.map('AddWeight.TButton', background=[('active', '#00994D')])

        self.cancel_btn_style = ttk.Style()
        self.cancel_btn_style.configure('Cancel.TButton', font=(25), padding=(0, 5, 0, 5))
        self.cancel_btn_style.map('Cancel.TButton', background=[('active', '#FF0000')])

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.dialog_center,
            'cursor': 'hand2',
        }

    def _create_widget_vars(self):
        self.title_lbl_var = f'Unesite količinu konzumiranja za proizvod\n`{self.label_name}`'
        self.weight_e_var = StringVar()

    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2,
                                   relief='groove', background='#FFFFCC', justify='center')

        self.weight_e = ttk.Entry(self.dialog_center, textvariable=self.weight_e_var, validate='all',
                                  validatecommand=self._validate_double, width=10, font='default 17', justify='center')
        self.weight_e.focus()

        self.add_btn = ttk.Button(text='Dodaj', style='AddWeight.TButton', command=self._add_consumed_weight, **self.mutual_button_options)
        self.cancel_btn = ttk.Button(text='Odustani', style='Cancel.TButton', command=self.dialog_center.destroy, **self.mutual_button_options)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, sticky='we')

        self.weight_e.grid(row=1, column=0, pady=(20, 0))

        self.add_btn.grid(row=2, column=0, pady=(20, 20))
        self.cancel_btn.grid(row=3, column=0, pady=(0, 20))

    def _validate_double_input(self, entry_value):
        if entry_value and self.double_pattern.match(entry_value) is None:
            return False
        return True

    def _add_consumed_weight(self):
        # scale the values according to the food_label and create new consumed food record
        # destroy the current dialog
        # show info msg
        entered_weight = self.weight_e_var.get()
        if not entered_weight:
            return
        entered_weight = float(entered_weight)
        scale_factor = round(entered_weight / self.NORMATIVE, 2)
        food_table = self.db.get_food_item_table(self.label_name)
        # NOTE: this would look nicer If I've used SQLAlchemy ORM
        food_table = food_table[1:-2]
        food_table.insert(1, entered_weight)
        food_table = food_table[0:2] + [d * scale_factor for d in food_table[2:]]

        values = {
            k: v
            for k, v in zip(self.TABLE_DIMENSIONS, food_table)
        }
        self.db.create_new_consumed_food_item(**values)
        self.dialog_center.destroy()
        messagebox.showinfo(title='Konzumirana masa dodana',
                            message=f'Uspješno dodano {entered_weight}g proizvoda',
                            parent=self.parent.dialog_center)


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
        self.dialog_center.destroy()
        messagebox.showinfo(title='Artikl trajno izbrisan',
                            message=f'Uspješno izbrisan `{self.label_name}`',
                            parent=self.parent.dialog_center)


class DialogPickerTopLevel:
    """Description"""
    def __init__(self, db, label_name):
        self.db = db
        self.label_name = label_name

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
        self.title_lbl_var = f'Odaberite što želite napraviti s proizvodom\n`{self.label_name}`'
    
    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2, relief='groove', background='#E57C2C', justify='center')
        
        self.add_btn = ttk.Button(text='Dodaj', image=self.add_img, style='Add.TButton', command=self._create_add_dialog, **self.mutual_button_options)
        self.update_btn = ttk.Button(text='Ažuriraj', image=self.update_img, style='Update.TButton', **self.mutual_button_options)
        self.delete_btn = ttk.Button(text='Izbriši', image=self.delete_img,
                                     command=self._create_delete_dialog, style='Delete.TButton', **self.mutual_button_options)
        self.close_btn = ttk.Button(text='Zatvori', image=self.close_img,style='Close.TButton',
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
        AddDialogTopLevel(self, self.db, self.label_name)


class NutritionTableResult:
    """Labels for rendering one nutrition table/row"""
    
    def __init__(self, parent):
        self.parent = parent
        self.all_row_data = []
    
    def render_row(self, row, row_data):
        bckgrnd_color = '#E3E7EA' if row % 2 == 0 else '#FFFFE6'
        # replace primary key with its number in the table
        row_data[0] = row
        for i, data in enumerate(row_data):
            lbl = ttk.Label(self.parent.frame, text=data, anchor='center', padding=(5), background=bckgrnd_color)
            lbl.grid(row=row, column=i, sticky='we')
            self.all_row_data.append(lbl)
        # change cursor for name dimension and attach an event to it
        self.all_row_data[1]['cursor'] = 'hand2'
        self.all_row_data[1].bind('<1>', lambda event: self.parent.parent._open_update_center(event))
    
    def destroy_row(self):
        for rd in self.all_row_data:
            rd.destroy()
        self.all_row_data = []


class NutritionTableHeaders:
    """Labels for rendering headers of nutrition tables"""

    text_constants = text_constants

    def __init__(self, parent, header_labels):
        self.parent = parent
        self.header_labels = header_labels
        self.label_widgets = []
        
        self._create_widgets()
        self._grid_widgets()

    def _create_styles(self):
        # TODO: expose this as a configurablsearch_food_ee option via public API
        self.nutrition_table_results_style = ttk.Style()
        self.nutrition_table_results_style.configure('NutritionTableResults.TFrame', background='#ade6e1')        
    
    def _create_widgets(self):
        for header_lbl in self.header_labels:
            lbl = ttk.Label(self.parent.frame, text=header_lbl, borderwidth=1, relief='raised', padding=(0, 5, 0, 5), anchor='center')
            self.label_widgets.append(lbl)
    
    def _grid_widgets(self):
        for i, widget in enumerate(self.label_widgets):
            widget.grid(row=0, column=i, sticky='we')


class NutritionTableResultsFrame:
    """Frame for rendering nutrition table with result(s)
    
    The frame is composed of headers, e.g. Fat, Carbs, Calories..
    and the table data associated with a particular food item.
    """
    text_constants = text_constants

    def __init__(self, parent, table_headers):
        self.parent = parent
        self.table_headers = table_headers
        self.col_count = len(table_headers)
        self.all_rows = []
        
        self._create_styles()
        self.frame = ttk.Frame(parent.frame, style='NutritionTableResults.TFrame')
        # enable resizing
        for i in range(self.col_count):
            self.frame.columnconfigure(i, weight=1)

    def _create_styles(self):
        # TODO: expose this as a configurable option via public API
        self.nutrition_table_results_style = ttk.Style()
        self.nutrition_table_results_style.configure('NutritionTableResults.TFrame', background='#ade6e1')
    
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
    
    def configure_style(self, style_name):
        self.frame.configure(style=style_name)

    def render_headers(self):
        # NOTE: Do I need to save the instance of the table headers?
        headers_frame = NutritionTableHeaders(self, self.table_headers)
    
    def render_results(self, food_tables):
        for i, food_table in enumerate(food_tables):
            row_frame = NutritionTableResult(self)
            row_frame.render_row(i + 1, food_table)
            self.all_rows.append(row_frame)


class StoredFoodTablesFrame:
    """Frame for rendering/filtering stored food labels/tables"""

    text_constants = text_constants
    HEADER_LABELS = (
        '#',
        text_constants['food_name_lbl'],
        text_constants['calory_lbl'],
        text_constants['fat_lbl'],
        text_constants['sat_fat_lbl'],
        text_constants['carb_lbl'],
        text_constants['sugar_lbl'],
        text_constants['fiber_lbl'],
        text_constants['protein_lbl'],
        text_constants['food_price_lbl'],
        text_constants['food_created_on'],
        text_constants['food_updated_on'],
    )
    # 100 grams is a normative
    NORMATIVE = 100

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        # container for storing the nutrition table results
        self.food_tables = []
        self.current_entered_food_name = None

        self._create_styles()
        # main frame
        self.frame = ttk.Frame(parent.canvas, style='StoredLabels.TFrame')
        self.frame.grid(row=0, column=0, sticky='news')
        self.frame.columnconfigure(0, weight=1)

        # its children
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('StoredLabels.TFrame', background='#ade6e1')
    
    def _create_widget_vars(self):
        self.search_food_e_var = StringVar()
        self.food_tables_tally_lbl_var = StringVar()
        self.food_tables_tally_lbl_var.set('0 rezultata')
        self.selected_sort_option_var = StringVar()
        self.sort_option_direction_var = StringVar()
    
    def _create_widgets(self):
        self.search_food_e = ttk.Entry(self.frame, width=20, textvariable=self.search_food_e_var, font='15')
        self.search_food_lbl = ttk.Button(self.frame, text='Pretraži', command=self._search_food)
        
        self.sort_options_lbl = ttk.Label(self.frame, text='Opcije sortiranja:')
        self.sort_options_cbox = ttk.Combobox(self.frame, values=self.HEADER_LABELS[1:], textvariable=self.selected_sort_option_var)
        self.sort_options_cbox.state(['readonly'])
        self.ascending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Uzlazno', variable=self.sort_option_direction_var, value='asc')
        self.descending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Silazno', variable=self.sort_option_direction_var, value='desc')
        self.sort_btn = ttk.Button(self.frame, text='Sortiraj', command=self._sort_results)

        
        self.food_tables_tally_lbl = ttk.Label(self.frame, borderwidth=2, relief='ridge', textvariable=self.food_tables_tally_lbl_var, padding=5)
        # this one is gridded only when a food result is actually present
        self.add_food_btn = ttk.Button(self.frame, text='Dodaj', padding=5, command=self._render_add_new_food_button)
        
        self.nutrition_table_frame = NutritionTableResultsFrame(self, self.HEADER_LABELS)
    
    def _grid_widgets(self):
        self.search_food_e.grid(row=0, column=0, sticky='w', padx=(20, 0), pady=10)
        self.search_food_lbl.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(0, 50))
        
        self.sort_options_lbl.grid(row=2, column=0, sticky='w', padx=(20, 0), pady=(0, 10))
        self.sort_options_cbox.grid(row=3, column=0, sticky='w', padx=(20, 0), pady=(0, 10))
        self.ascending_sort_option_rbtn.grid(row=4, column=0, sticky='w', padx=(20, 0), pady=(0, 10))
        self.descending_sort_option_rbtn.grid(row=5, column=0, sticky='w', padx=(20, 0), pady=(0, 10))
        self.sort_btn.grid(row=6, column=0, sticky='w', padx=(20, 0), pady=(0, 10))
        
        self.food_tables_tally_lbl.grid(row=7, column=0, sticky='w', padx=(5, 0), pady=(30, 10))

        self.nutrition_table_frame.grid_frame(row=8, column=0, sticky='we')
    
    def _bind_events(self):
        self.search_food_e.bind('<Return>', lambda _: self._search_food())
    
    def _get_food_results(self, name_segment):
        """Fetches all food nutrition tables based on `in` operator
        
        If no name segment is given, return all nutrition tables in Ranah.
        """
        if not name_segment:
            return self.db.all_food_label_tables
        name_segment = name_segment.lower()
        food_tables = [self.db.get_food_item_table(food_lbl) 
                            for food_lbl in self.db.all_food_label_names 
                            if name_segment in food_lbl.lower()]
        return food_tables
    
    def _search_food(self):
        """Read user's input and render nutrition table rows based on a match"""
        
        food_name_entry = self.search_food_e_var.get().strip()
        # input didn't change -> rows don't change
        # TODO: this is bad when user wants to check for successful update/deletion; try to do better
        # if self.current_entered_food_name == food_name_entry:
        #     return
        self.current_entered_food_name = food_name_entry
        self.food_tables = self._get_food_results(food_name_entry)
        
        # update the number of results label
        cnt = len(self.food_tables)
        cnt_s = str(cnt).zfill(2)
        text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        self.food_tables_tally_lbl_var.set(f'{cnt} {text}')
        
        # Clear all rendered rows
        self.nutrition_table_frame.destroy_rows()
        # re-render them with the updated list of food tables
        self.nutrition_table_frame.render_results(self.food_tables)
    
    def _sort_results(self):
        sort_direction = self.sort_option_direction_var.get()
        rev = True if sort_direction == 'desc' else False
        sort_option = self.selected_sort_option_var.get()
        if sort_option:
            idx = self.HEADER_LABELS.index(sort_option)
            self.food_tables.sort(key=lambda row: row[idx], reverse=rev)
            # Clear all rendered rows
            self.nutrition_table_frame.destroy_rows()
            # re-render them with the sorted list of food tables
            self.nutrition_table_frame.render_results(self.food_tables)
    
    def _open_update_center(self, event):
        DialogPickerTopLevel(self.db, event.widget['text'])
    
    def _render_add_new_food_button(self):
        afi_frame = AddNewFoodItemFrame(self.frame, food_name=self.selected_food_name, callback=self._add_new_food_item)
        # TODO: I guess this should be part of public API
        afi_frame.frame.grid(row=0, column=0, rowspan=5, columnspan=2, sticky='n')
    
    def _add_new_food_item(self, food_item_weight):
        """Connect to db and create a new (eaten) food item"""

        ratio = food_item_weight / self.NORMATIVE
        # NOTE: quite ugly, should be better when I switch to sqlAlchemy ORM
        food_name, *food_nutrition = self.db.get_food_item_table(self.selected_food_name)[0][1:]
        # TODO: this is tightly coupled with the db schema,
        # meaning if schema changes I need to change this list definition throughout the app
        food_nutrition_column = ['calories', 'fat', 'saturated_fat', 'carbs', 'sugars', 'proteins', 'fiber']
        record = {c: float(n) * ratio for c, n in zip(food_nutrition_column, food_nutrition)}
        record['food_name'] = food_name
        record['food_weight'] = food_item_weight
        self.db.create_new_consumed_food_item(**record)

