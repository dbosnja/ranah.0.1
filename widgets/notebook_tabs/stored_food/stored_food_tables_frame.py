from tkinter import ttk, StringVar

from constants.constants import nutrition_table_map, nutrition_table_headers
from ...utility_widgets.leaf_frames import FoodTableResultsFrame
from .top_level_dialogs import DialogPickerTopLevel


class StoredFoodSearchOptionsFrame:
    """Frame for rendering options of searching and sorting for stored foods tab."""

    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self._create_styles()

        self.frame = ttk.Frame(parent.frame, style='SFoodSearchOptions.TFrame', padding=(40, 30))

        self._create_mutual_combobox_options()

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

    def _create_mutual_combobox_options(self):
        self.mutual_cbox_options = {
            'master': self.frame,
            'height': 6,
            'state': 'readonly',
            'width': 5,
        }

    def _create_styles(self):
        ttk.Style().configure('SFoodSearchOptions.TFrame', background='#F8FCE8', borderwidth=3, relief='ridge')
        ttk.Style().configure('SFoodTopic.TLabel', anchor='center', borderwidth=2, relief='ridge', background='#BFBFBF', font='default 12')
        ttk.Style().configure('SFoodText.TLabel', anchor='center', padding=2, font='default 12', background='#F8FCE8')
        ttk.Style().configure('SFoodSearch.TButton', anchor='center', padding=5, font='default 11')
        ttk.Style().configure('SFoodRadio.TRadiobutton', anchor='center', padding=5, font='default 10', background='#BFBFBF')

    def _create_widget_vars(self):
        self.search_name_e_var = StringVar()
        self.selected_sort_option_var = StringVar()
        self.sort_option_direction_var = StringVar(value='asc')

    def _create_widgets(self):
        self.search_options_topic_lbl = ttk.Label(self.frame, text='Opcije pretraživanja', style='SFoodTopic.TLabel', padding=6)
        self.search_name_lbl = ttk.Label(self.frame, text='Naziv pohranjenog artikla', style='SFoodText.TLabel')
        self.search_name_e = ttk.Entry(self.frame, textvariable=self.search_name_e_var, font='default 12')
        self.search_btn = ttk.Button(self.frame, text='Pretraži', command=self._search_foods, style='SFoodSearch.TButton', cursor='hand2')

        self.vertical_separator = ttk.Separator(self.frame, orient='vertical')

        self.sort_options_topic_lbl = ttk.Label(self.frame, text='Opcije sortiranja', style='SFoodTopic.TLabel', padding=6)
        self.sort_options_cbox = ttk.Combobox(self.frame, values=list(nutrition_table_headers.values())[1:], state='readonly',
                                              textvariable=self.selected_sort_option_var, cursor='hand2')
        self.ascending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Uzlazno',
                                                          variable=self.sort_option_direction_var, value='asc',
                                                          style='SFoodRadio.TRadiobutton', cursor='hand2')
        self.descending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Silazno',
                                                           variable=self.sort_option_direction_var, value='desc',
                                                           style='SFoodRadio.TRadiobutton', cursor='hand2')
        self.sort_btn = ttk.Button(self.frame, text='Sortiraj', style='SFoodSearch.TButton', cursor='hand2', command=self._sort_results)

    def _grid_widgets(self):
        self.search_options_topic_lbl.grid(row=0, column=0, columnspan=6, pady=(0, 30))
        self.search_name_lbl.grid(row=1, column=0, columnspan=3, padx=(0, 5), pady=(0, 10))
        self.search_name_e.grid(row=1, column=3, columnspan=3, pady=(0, 10))
        self.search_btn.grid(row=2, column=0, columnspan=6, pady=(30, 0))

        self.vertical_separator.grid(row=0, column=6, rowspan=3, sticky='ns', padx=(60, 0))

        self.sort_options_topic_lbl.grid(row=0, column=7, columnspan=5, padx=(60, 0), pady=(0, 30))
        self.sort_options_cbox.grid(row=1, column=7, columnspan=3, padx=(60, 15), pady=(0, 10))
        self.ascending_sort_option_rbtn.grid(row=1, column=10, padx=(0, 15), pady=(0, 10))
        self.descending_sort_option_rbtn.grid(row=1, column=11, pady=(0, 10))
        self.sort_btn.grid(row=2, column=8, columnspan=5, pady=(20, 0))

    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.scroll_up_handler())
        self.frame.bind('<Button-5>', lambda _: self.scroll_down_handler())
        self.search_name_e.bind('<Return>', lambda _: self._search_foods())

    def _search_foods(self):
        food_name = self.search_name_e_var.get().strip()
        self.parent.search_food(food_name)

    def _sort_results(self):
        sort_option = self.selected_sort_option_var.get()
        if sort_option:
            sort_direction = self.sort_option_direction_var.get()
            rev = True if sort_direction == 'desc' else False
            self.parent.sort_results(sort_option, rev)

    def grid_frame(self, row, column, sticky):
        self.frame.grid(row=row, column=column, sticky=sticky, padx=(20), pady=(0, 20))

    def configure_style(self, style_name):
        self.frame.configure(style=style_name)

    def set_scroll_up_handler(self, callback):
        self.scroll_up_handler = callback

    def set_scroll_down_handler(self, callback):
        self.scroll_down_handler = callback


class StoredFoodTablesFrame:
    """Frame for rendering/filtering stored food labels/tables"""

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
        ttk.Style().configure('StoredFoodTopic.TLabel', anchor='center', font='Helvetica 15', padding=20)
    
    def _create_widget_vars(self):
        self.topic_lbl_text = 'Pretraži trajno pohranjene prehrambene nutritivne tablice'
        self.food_tables_tally_lbl_var = StringVar(value='0 rezultata')
    
    def _create_widgets(self):
        self.topic_lbl = ttk.Label(self.frame, text=self.topic_lbl_text, style='StoredFoodTopic.TLabel')

        self.stored_food_search_options_frame = StoredFoodSearchOptionsFrame(self, self.db)
        self.stored_food_search_options_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.stored_food_search_options_frame.set_scroll_down_handler(self.parent.handle_scroll_down)

        self.food_tables_tally_lbl = ttk.Label(self.frame, borderwidth=2, relief='ridge', textvariable=self.food_tables_tally_lbl_var, padding=5)
        
        # NOTE: FoodTableResultsFrame is generic enough to handle various use-cases
        # in this context I'm using it as a nutrition table frame, therefore the name
        self.nutrition_table_frame = FoodTableResultsFrame(self, nutrition_table_headers.values())
        self.nutrition_table_frame.configure_style('StoredLabels.TFrame')
        self.nutrition_table_frame.set_row_callback(self._open_update_center)
        self.nutrition_table_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.nutrition_table_frame.set_scroll_down_handler(self.parent.handle_scroll_down)
    
    def _grid_widgets(self):
        self.topic_lbl.grid(row=0, column=0, sticky='we', padx=(15, 30), pady=(50, 30))
        self.stored_food_search_options_frame.grid_frame(row=1, column=0, sticky='w')
        self.food_tables_tally_lbl.grid(row=2, column=0, sticky='w', padx=(5, 0), pady=(30, 10))
        self.nutrition_table_frame.grid_frame(row=3, column=0, sticky='we')
    
    def _bind_events(self):
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

    def search_food(self, food_name_entry):
        """Render nutrition food table rows based on a match"""

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

    def sort_results(self, sort_option, rev):
        for k, v in nutrition_table_headers.items():
            if v == sort_option:
                idx = nutrition_table_map[k]
                break
        self.nutrition_table_frame.mark_column(idx)
        if idx == 1:
            # sort by name works based on ASCII -> compare with case insensitivity
            self.food_tables.sort(key=lambda row: row[idx].lower(), reverse=rev)
        else:
            self.food_tables.sort(key=lambda row: row[idx], reverse=rev)
        # Clear all rendered rows
        self.nutrition_table_frame.destroy_rows()
        # re-render them with the sorted list of food tables
        self.nutrition_table_frame.render_results(self.food_tables)

    def _open_update_center(self, p_key):
        # All operations can be done solely on the food table name
        table_row = self.db.get_food_item_table_by_primary_key(p_key)
        label_name = table_row[nutrition_table_map['label_name']]
        DialogPickerTopLevel(self.db, label_name)

