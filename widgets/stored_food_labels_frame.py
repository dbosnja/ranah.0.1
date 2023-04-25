from tkinter import ttk, Listbox, StringVar

from .create_food_item_frame import CreateFoodItemFrame
from .leaf_frames import ScrollBarWidget


class StoredFoodLabelsFrame:
    """Frame for rendering/filtering stored food labels/tables"""

    text_constants = CreateFoodItemFrame.text_constants

    def __init__(self, parent, db):
        self.db = db
        self.food_label_names = self.db.all_food_label_names

        # main frame
        self.frame = ttk.Frame(parent, style='StoredLabels.TFrame', borderwidth=5, relief='raised')
        self.frame.grid(row=1, column=0, sticky='nwe', padx=10)
        # enable resizing
        for i in range(9):
            self.frame.columnconfigure(i, weight=1)

        # its children
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

        # style the list-box
        self._style_lbox_items()
    
    def _create_styles(self):
        ttk.Style().configure('StoredLabels.TFrame', background='#ade6e1')
    
    def _create_widget_vars(self):
        self.food_label_names_lboxvar = StringVar(value=self.food_label_names)
        self.search_entry_var = StringVar()
    
    def _create_widgets(self):
        self.food_names_lbox = Listbox(self.frame, height=5, listvariable=self.food_label_names_lboxvar, width=30)
        self.food_names_lbox_scroll_bar = ScrollBarWidget(self.frame)
        self.food_names_lbox_scroll_bar.attach_to_scrollable(self.food_names_lbox)
        
        self.search_btn = ttk.Button(self.frame, text='Pretraži po imenu', width=30)
        self.search_entry = ttk.Entry(self.frame, width=30, textvariable=self.search_entry_var)
        self.refresh_btn = ttk.Button(self.frame, text='Osvježi', width=30)
        
        self.food_number_lbl = ttk.Label(self.frame, text='#', borderwidth=2, relief='raised', padding=8)
        self.food_name_lbl = ttk.Label(self.frame, text=self.text_constants['food_name_lbl'], borderwidth=2, relief='raised', padding=8)
        self.calories_lbl = ttk.Label(self.frame, text=self.text_constants['calory_lbl'], borderwidth=2, relief='raised', padding=8)
        self.fat_lbl = ttk.Label(self.frame, text=self.text_constants['fat_lbl'], borderwidth=2, relief='raised', padding=8)
        self.sat_fat_lbl = ttk.Label(self.frame, text=self.text_constants['sat_fat_lbl'], borderwidth=2, relief='raised', padding=8)
        self.carbs_lbl = ttk.Label(self.frame, text=self.text_constants['carb_lbl'], borderwidth=2, relief='raised', padding=8)
        self.sugar_lbl = ttk.Label(self.frame, text=self.text_constants['sugar_lbl'], borderwidth=2, relief='raised', padding=8)
        self.protein_lbl = ttk.Label(self.frame, text=self.text_constants['protein_lbl'], borderwidth=2, relief='raised', padding=8)
        self.fiber_lbl = ttk.Label(self.frame, text=self.text_constants['fiber_lbl'], borderwidth=2, relief='raised', padding=8)
    
    def _grid_widgets(self):
        self.food_names_lbox.grid(row=0, column=4, pady=5, columnspan=2)
        self.food_names_lbox_scroll_bar.grid(row=0, column=5, sticky='ens', pady=5)
        self.search_entry.grid(row=1, column=4, pady=5, columnspan=2)
        self.search_btn.grid(row=2, column=4, pady=5, columnspan=2)
        self.refresh_btn.grid(row=3, column=4, pady=5, columnspan=2)
        
        self.food_number_lbl.grid(row=4, column=0, padx=5, pady=10)
        self.food_name_lbl.grid(row=4, column=1, padx=5, pady=10)
        self.calories_lbl.grid(row=4, column=2, padx=5, pady=10)
        self.fat_lbl.grid(row=4, column=3, padx=5, pady=10)
        self.sat_fat_lbl.grid(row=4, column=4, padx=5, pady=10)
        self.carbs_lbl.grid(row=4, column=5, padx=5, pady=10)
        self.sugar_lbl.grid(row=4, column=6, padx=5, pady=10)
        self.protein_lbl.grid(row=4, column=7, padx=5, pady=10)
        self.fiber_lbl.grid(row=4, column=8, padx=5, pady=10)
    
    def _bind_events(self):
        self.refresh_btn.configure(command=self._refresh_food_names)
        self.search_btn.configure(command=self._search_by_name)
    
    def _refresh_food_names(self):
        self.food_label_names = self.db.all_food_label_names
        self.food_label_names_lboxvar.set(self.food_label_names)
        self.food_names_lbox.configure(listvariable=self.food_label_names_lboxvar)
    
    def _search_by_name(self):
        search_token = self.search_entry_var.get()
        filtered_names = [name for name in self.food_label_names if search_token.lower() in name.lower()]
        filtered_names_var = StringVar(value=filtered_names)
        self.food_names_lbox.configure(listvariable=filtered_names_var)
    
    def _style_lbox_items(self):
        for i in range(0, len(self.food_label_names), 2):
            self.food_names_lbox.itemconfigure(i, background='#ddd')
