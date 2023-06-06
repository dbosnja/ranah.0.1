from tkinter import ttk, StringVar

from constants.constants import text_constants
from ...utility_widgets import AddNewFoodItemFrame


class NutritionTableResult:
    """"Labels for rendering one nutrition table/row"""
    
    def __init__(self, parent):
        self.parent = parent
        self.all_row_data = []
    
    def render_row(self, row, row_data):
        bckgrnd_color = '#E3E7EA' if row % 2 == 0 else '#FFFFE6'
        # replace primary key with its number in the table
        row_data[0] = row
        for i, data in enumerate(row_data):
            lbl = ttk.Label(self.parent, text=data, anchor='center', padding=(5), background=bckgrnd_color)
            lbl.grid(row=row, column=i, sticky='we')
            self.all_row_data.append(lbl)
    
    def destory_row(self):
        for rd in self.all_row_data:
            rd.destroy()
        self.all_row_data = []


class NutritionTableHeaders:
    """"Labels for rendering headers of nutrition tables"""

    text_constants = text_constants

    def __init__(self, parent, header_labels):
        self.parent = parent
        self.header_labels = header_labels
        self.label_widgets = []
        
        self._create_widgets()
        self._grid_widgets()

    def _create_styles(self):
        # TODO: expose this as a configurable option via public API
        self.nutrition_table_results_style = ttk.Style()
        self.nutrition_table_results_style.configure('NutritionTableResults.TFrame', background='#ade6e1')        
    
    def _create_widgets(self):
        for header_lbl in self.header_labels:
            lbl = ttk.Label(self.parent, text=header_lbl, borderwidth=1, relief='raised', padding=(0, 5, 0, 5), anchor='center')
            self.label_widgets.append(lbl)
    
    def _grid_widgets(self):
        for i, widget in enumerate(self.label_widgets):
            widget.grid(row=0, column=i, sticky='we')


class NutritionTableResultsFrame:
    """"Frame for rendering nutrition table with result(s)
    
    The frame is composed of headers, e.g. Fat, Carbs, Calories..
    and the table data associated with a particular food item.
    """
    text_constants = text_constants

    def __init__(self, parent, table_headers):
        self.table_headers = table_headers
        self.col_count = len(table_headers)
        self.all_rows = []
        
        self._create_styles()
        self.frame = ttk.Frame(parent, style='NutritionTableResults.TFrame')
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
            row.destory_row()
        self.all_rows = []
    
    def configure_style(self, style_name):
        self.frame.configure(style=style_name)

    def render_headers(self):
        # NOTE: Do I need to save the instance of the table headers?
        headers_frame = NutritionTableHeaders(self.frame, self.table_headers)
    
    def render_results(self, food_tables):
        for i, food_table in enumerate(food_tables):
            row_frame = NutritionTableResult(self.frame)
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
        text_constants['protein_lbl'],
        text_constants['fiber_lbl'],
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
    
    def _create_widgets(self):
        self.search_food_e = ttk.Entry(self.frame, width=20, textvariable=self.search_food_e_var, font='15')
        self.search_food_lbl = ttk.Button(self.frame, text='Pretraži', command=self._search_food)
        self.food_tables_tally_lbl = ttk.Label(self.frame, borderwidth=2, relief='ridge', textvariable=self.food_tables_tally_lbl_var, padding=5)
        # this one is gridded only when a food result is actually present
        self.add_food_btn = ttk.Button(self.frame, text='Dodaj', padding=5, command=self._render_add_new_food_button)
        
        self.nutrition_table_frame = NutritionTableResultsFrame(self.frame, self.HEADER_LABELS)
    
    def _grid_widgets(self):
        self.search_food_e.grid(row=0, column=0, sticky='w', padx=(20, 0), pady=10)
        self.search_food_lbl.grid(row=1, column=0, sticky='w', padx=(20, 0), pady=(0, 10))
        self.food_tables_tally_lbl.grid(row=2, column=0, sticky='w', padx=(5, 0), pady=(30, 10))

        self.nutrition_table_frame.grid_frame(row=3, column=0, sticky='we')
    
    def _bind_events(self):
        self.search_food_e.bind('<Return>', lambda _: self._search_food())
    
    def _get_food_results(self, name_segment):
        """Fetches all food nutrition tables based on `in` operator
        
        If no name segment is given, return all nutrition tables in Ranah.
        """
        if not name_segment:
            self.food_tables = self.db.all_food_label_tables
            return
        name_segment = name_segment.lower()
        self.food_tables = [self.db.get_food_item_table(food_lbl) 
                            for food_lbl in self.db.all_food_label_names 
                            if name_segment in food_lbl.lower()]
    
    def _search_food(self):
        """Read user's input and render nutrition table rows based on a match"""
        
        food_name_entry = self.search_food_e_var.get().strip()
        # input didn't change -> rows don't change
        if self.current_entered_food_name == food_name_entry:
            return
        self.current_entered_food_name = food_name_entry
        self._get_food_results(food_name_entry)
        
        # update the number of results label
        cnt = len(self.food_tables)
        # TODO: faila za 11, 111, 101..
        text = 'rezultat' if str(cnt).endswith('1') else 'rezultata'
        self.food_tables_tally_lbl_var.set(f'{cnt} {text}')
        
        # Clear all rendered rows
        self.nutrition_table_frame.destroy_rows()
        # re-render them with the updated list of food tables
        self.nutrition_table_frame.render_results(self.food_tables)
    
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

