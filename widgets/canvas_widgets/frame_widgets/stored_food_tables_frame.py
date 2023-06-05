from tkinter import ttk, StringVar

from constants.constants import text_constants
from ...utility_widgets import NutritionTableResultsFrame, AddNewFoodItemFrame


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
        self.frame = ttk.Frame(parent.canvas, style='StoredLabels.TFrame', borderwidth=2, relief='raised')
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

