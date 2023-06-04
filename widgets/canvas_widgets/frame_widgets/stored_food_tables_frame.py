from tkinter import ttk, Listbox, StringVar

from constants.constants import text_constants
from ...utility_widgets import ScrollBarWidget, NutritionTableResultsFrame, AddNewFoodItemFrame


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
        self.db = db
        self.food_tables = []
        # initialize the frame with all food tables in Ranah
        # self._get_food_results(name_segment='')

        self._create_styles()
        # main frame
        self.frame = ttk.Frame(parent, style='StoredLabels.TFrame', borderwidth=2, relief='raised')
        self.screen_width = self.frame.winfo_screenwidth()
        self.screen_height = self.frame.winfo_screenheight()
        self.frame.configure(width=self.screen_width)
        self.frame.configure(height=self.screen_height)
        self.frame.grid(row=0, column=0, sticky='news', padx=10)
        self.frame.columnconfigure(0, weight=1)

        # its children
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        
        # friend(child) frame
        self.nutrition_table_frame = NutritionTableResultsFrame(self.frame, len(self.HEADER_LABELS))
        self.nutrition_table_frame.grid_frame(row=1, column=0, sticky='wes')
        self.nutrition_table_frame.render_headers(self.HEADER_LABELS)
        self.nutrition_table_frame.render_results(self.food_tables)
    
    def _create_styles(self):
        ttk.Style().configure('StoredLabels.TFrame', background='#ade6e1')
    
    def _create_widget_vars(self):
        self.search_entry_var = StringVar()
    
    def _create_widgets(self):
        self.food_tables_tally_lbl = ttk.Label(self.frame, borderwidth=2, relief='ridge', text=f'{len(self.food_tables)} rezultata', padding=5)
        # this one is gridded only when a food result is actually present
        self.add_food_btn = ttk.Button(self.frame, text='Dodaj', padding=5, command=self._render_add_new_food_button)
    
    def _grid_widgets(self):
        self.food_tables_tally_lbl.grid(row=0, column=0, sticky='w', padx=(5, 0), pady=10)
    
    def _get_food_results(self, name_segment):
        """Fetches all food nutrition tables based on `in` operator
        
        If no name segment is given, return all nutrition tables in Ranah.
        """
        if not name_segment:
            self.food_tables = self.db.all_food_label_tables
            return
        for food_lbl in self.db.all_food_label_names:
            if name_segment.lower() in food_lbl.lower():
                self.food_tables.append(self.db.get_food_item_table(food_lbl))
    
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

