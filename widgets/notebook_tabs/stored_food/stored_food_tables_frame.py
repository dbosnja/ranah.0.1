from tkinter import ttk, StringVar

from constants.constants import text_constants, nutrition_table_map
from ...utility_widgets.leaf_frames import FoodTableResultsFrame
from .top_level_dialogs import DialogPickerTopLevel


class StoredFoodTablesFrame:
    """Frame for rendering/filtering stored food labels/tables"""

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

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        # container for storing the nutrition table results
        self.food_tables = []

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
        # TODO: make these widget all under one single Frame parent
        self.search_food_e = ttk.Entry(self.frame, width=20, textvariable=self.search_food_e_var, font='15')
        self.search_food_lbl = ttk.Button(self.frame, text='Pretraži', command=self._search_food, cursor='hand2')
        
        self.sort_options_lbl = ttk.Label(self.frame, text='Opcije sortiranja:')
        self.sort_options_cbox = ttk.Combobox(self.frame, values=self.HEADER_LABELS[1:], state='readonly',
                                              textvariable=self.selected_sort_option_var)
        self.ascending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Uzlazno', variable=self.sort_option_direction_var, value='asc')
        self.descending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Silazno', variable=self.sort_option_direction_var, value='desc')
        self.sort_btn = ttk.Button(self.frame, text='Sortiraj', command=self._sort_results, cursor='hand2')

        self.food_tables_tally_lbl = ttk.Label(self.frame, borderwidth=2, relief='ridge', textvariable=self.food_tables_tally_lbl_var, padding=5)
        
        # NOTE: FoodTableResultsFrame is generic enough to handle various use-cases
        # in this context I'm using it as a nutrition table frame, therefore the name
        self.nutrition_table_frame = FoodTableResultsFrame(self, self.HEADER_LABELS)
        self.nutrition_table_frame.configure_style('StoredLabels.TFrame')
        self.nutrition_table_frame.set_row_callback(self._open_update_center)
        self.nutrition_table_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.nutrition_table_frame.set_scroll_down_handler(self.parent.handle_scroll_down)
    
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
        self.frame.bind('<Button-4>', lambda _: self.parent.handle_scroll_up())
        self.frame.bind('<Button-5>', lambda _: self.parent.handle_scroll_down())
    
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
            if idx == 1:
                # sort by name works based on ASCII -> compare with case insensitivity
                self.food_tables.sort(key=lambda row: row[idx].lower(), reverse=rev)
            else:
                self.food_tables.sort(key=lambda row: row[idx], reverse=rev)
            # Clear all rendered rows
            self.nutrition_table_frame.destroy_rows()
            # re-render them with the sorted list of food tables
            self.nutrition_table_frame.render_results(self.food_tables)
    
    def _open_update_center(self, food_row):
        # All operations can be done solely on the food name
        label_name_widget = food_row[nutrition_table_map['label_name']]
        DialogPickerTopLevel(self.db, label_name_widget['text'])

