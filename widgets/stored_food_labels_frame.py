from tkinter import ttk, Listbox, StringVar

from .constants import text_constants
from .leaf_frames import ScrollBarWidget, NutritionTableResultFrame, AddNewFoodItemFrame


class StoredFoodLabelsFrame:
    """Frame for rendering/filtering stored food labels/tables"""

    text_constants = text_constants
    # 100 grams is a normative
    normative = 100

    def __init__(self, parent, db):
        self.db = db
        self.food_label_names = self.db.all_food_label_names
        # a reference to the current list of food label names exposed on UI
        self.current_food_label_names = self.food_label_names

        # main frame
        self.frame = ttk.Frame(parent, style='StoredLabels.TFrame', borderwidth=5, relief='raised')
        self.frame.grid(row=1, column=0, sticky='nwe', padx=10)
        self.frame.columnconfigure(0, weight=1)

        # its children
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        
        # friend(child) frame
        self.nutrition_table_frame = NutritionTableResultFrame(self.frame)
        
        self._bind_events()

        # style the list-box
        self._style_lbox_items()
    
    def _create_styles(self):
        ttk.Style().configure('StoredLabels.TFrame', background='#ade6e1')
    
    def _create_widget_vars(self):
        self.food_label_names_lboxvar = StringVar(value=self.food_label_names)
        self.search_entry_var = StringVar()
    
    def _create_widgets(self):
        # TODO: this Listbox has to be a self-contained type -> it's going to be shared throughout the app
        self.food_names_lbox = Listbox(self.frame, height=5, listvariable=self.food_label_names_lboxvar, width=30)
        self.food_names_lbox_scroll_bar = ScrollBarWidget(self.frame)
        self.food_names_lbox_scroll_bar.attach_to_scrollable(self.food_names_lbox)
        self.food_tables_tally_lbl = ttk.Label(self.frame, borderwidth=2, relief='ridge', text=f'{len(self.food_label_names)} rezultata', padding=5)
        
        self.search_btn = ttk.Button(self.frame, text='Pretraži po imenu', width=30)
        self.search_entry = ttk.Entry(self.frame, width=30, textvariable=self.search_entry_var)
        self.refresh_btn = ttk.Button(self.frame, text='Osvježi', width=30)

        # this one is gridded only when a food result is actually present
        self.add_food_btn = ttk.Button(self.frame, text='Dodaj', padding=5, command=self._render_add_new_food_button)
    
    def _grid_widgets(self):
        self.food_names_lbox.grid(row=0, column=0, pady=5, columnspan=2, sticky='we')
        self.food_names_lbox_scroll_bar.grid(row=0, column=1, sticky='ns', pady=5)
        
        self.food_tables_tally_lbl.grid(row=1, column=0, sticky='w', padx=(5, 0))
        self.search_entry.grid(row=1, column=0, pady=5, columnspan=2)
        self.search_btn.grid(row=2, column=0, pady=5, columnspan=2)
        self.refresh_btn.grid(row=3, column=0, pady=5, columnspan=2)
    
    def _bind_events(self):
        self.refresh_btn.configure(command=self._refresh_food_names)
        self.search_btn.configure(command=self._search_by_name)
        self.food_names_lbox.bind('<Double-1>', self._get_record_from_doubleclick)

    
    def _refresh_food_names(self):
        self.food_label_names = self.db.all_food_label_names
        self.food_label_names_lboxvar.set(self.food_label_names)
        self.food_names_lbox.configure(listvariable=self.food_label_names_lboxvar)
        self.search_entry_var.set('')
        self.current_food_label_names = self.food_label_names
        self.food_tables_tally_lbl.configure(text=f'{len(self.food_label_names)} rezultata')
        
        self.nutrition_table_frame.grid_forget()
        self.nutrition_table_frame = NutritionTableResultFrame(self.frame)
        # style again the food_names_lbox
        self._style_lbox_items()

        self.add_food_btn.grid_forget()
    
    def _search_by_name(self):
        search_token = self.search_entry_var.get()
        self.filtered_names = [name for name in self.food_label_names if search_token.lower() in name.lower()]
        self.filtered_names_var = StringVar(value=self.filtered_names)
        self.food_names_lbox.configure(listvariable=self.filtered_names_var)
        self.food_names_lbox.see(0)
        text = f'{len(self.filtered_names)} rezultata' if len(self.filtered_names) > 1 else f'{len(self.filtered_names)} rezultat'
        self.food_tables_tally_lbl.configure(text=text)
        self.current_food_label_names = self.filtered_names
    
    def _get_record_from_doubleclick(self, event):
        # Currently only one item box can be selected
        food_idx = self.food_names_lbox.curselection()[0]
        food_name = self.current_food_label_names[food_idx]
        self._render_searched_result(self.db.get_food_item_table(food_name))
    
    def _style_lbox_items(self):
        for i in range(0, len(self.food_label_names), 2):
            self.food_names_lbox.itemconfigure(i, background='#fff3e6')

    def _render_searched_result(self, food_results):
        # TODO: refactor; this method should rely on internal method of the NutritionTableResultFrame
        
        # first clear all rendered results(if any)
        self.nutrition_table_frame.grid_forget()
        # re-render the table headers
        self.nutrition_table_frame = NutritionTableResultFrame(self.frame)

        # Expected to be a 1-element list, could change in future
        for row_idx, food_table_record in enumerate(food_results):
            food_table_record = list(food_table_record[1:])
            for col_idx, val in enumerate([row_idx + 1] + food_table_record):
                # TODO: make this try/except clause a bit less painful, ie remove it completely
                try:
                    val = round(float(val), 2)
                except ValueError:
                    # only for name column
                    # this is a hack, it would be best to have an actual mapping between 
                    # db column names and the actual values
                    self.selected_food_name = val
                lbl = ttk.Label(self.nutrition_table_frame.frame, text=val, borderwidth=2,
                                relief='raised', padding=8, anchor='center', background='#ffffcc')
                lbl.grid(row=row_idx + 1, column=col_idx, padx=5)
        if food_results:
            # this 4 is because it's parent has 4 rows -> quite terrible, but I'll live with it for now
            self.add_food_btn.grid(row=4 + len(food_results) + 1, column=0, padx=5, pady=10, sticky='w')
    
    def _render_add_new_food_button(self):
        afi_frame = AddNewFoodItemFrame(self.frame, food_name=self.selected_food_name, callback=self._add_new_food_item)
        # TODO: I guess this should be part of public API
        afi_frame.frame.grid(row=0, column=0, rowspan=5, columnspan=2, sticky='n')
    
    def _add_new_food_item(self, food_item_weight):
        """Connect to db and create a new (eaten) food item"""

        ratio = food_item_weight / self.normative
        # NOTE: quite ugly, should be better when I switch to sqlAlchemy ORM
        food_name, *food_nutrition = self.db.get_food_item_table(self.selected_food_name)[0][1:]
        # TODO: this is tightly coupled with the db schema,
        # meaning if schema changes I need to change this list definition throughout the app
        food_nutrition_column = ['calories', 'fat', 'saturated_fat', 'carbs', 'sugars', 'proteins', 'fiber']
        record = {c: float(n) * ratio for c, n in zip(food_nutrition_column, food_nutrition)}
        record['food_name'] = food_name
        record['food_weight'] = food_item_weight
        self.db.create_new_consumed_food_item(**record)

