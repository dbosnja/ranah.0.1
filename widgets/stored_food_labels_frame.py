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
        self.frame.columnconfigure(0, weight=1)

        # its children
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        
        # TODO: this should be handled in the frame's own namespace
        self._create_result_frame()
        self._create_results_frame_children()
        self._grid_results_frame_children()
        
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
    
    def _grid_widgets(self):
        self.food_names_lbox.grid(row=0, column=0, pady=5, columnspan=2, sticky='we')
        self.food_names_lbox_scroll_bar.grid(row=0, column=1, sticky='ns', pady=5)
        self.search_entry.grid(row=1, column=0, pady=5, columnspan=2)
        self.search_btn.grid(row=2, column=0, pady=5, columnspan=2)
        self.refresh_btn.grid(row=3, column=0, pady=5, columnspan=2)
    
    def _bind_events(self):
        self.refresh_btn.configure(command=self._refresh_food_names)
        self.search_btn.configure(command=self._search_by_name)
        self.food_names_lbox.bind('<Double-1>', self._get_record_from_doubleclick)
    
    def _create_result_frame(self):
        # frame holding searched results
        # TODO: this frame should a separate type, easily pluggable to self.frame
        self.results_frame = ttk.Frame(self.frame, style='StoredLabels.TFrame')
        # enable resizing
        for i in range(9):
            self.results_frame.columnconfigure(i, weight=1)
        self.results_frame.grid(row=4, column=0, sticky='we')
    
    def _create_results_frame_children(self):
        self.food_number_lbl = ttk.Label(self.results_frame, text='#', borderwidth=2, relief='raised', padding=8, anchor='center')
        self.food_name_lbl = ttk.Label(self.results_frame, text=self.text_constants['food_name_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.calories_lbl = ttk.Label(self.results_frame, text=self.text_constants['calory_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.fat_lbl = ttk.Label(self.results_frame, text=self.text_constants['fat_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.sat_fat_lbl = ttk.Label(self.results_frame, text=self.text_constants['sat_fat_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.carbs_lbl = ttk.Label(self.results_frame, text=self.text_constants['carb_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.sugar_lbl = ttk.Label(self.results_frame, text=self.text_constants['sugar_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.protein_lbl = ttk.Label(self.results_frame, text=self.text_constants['protein_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
        self.fiber_lbl = ttk.Label(self.results_frame, text=self.text_constants['fiber_lbl'], borderwidth=2, relief='raised', padding=8, anchor='center')
    
    def _grid_results_frame_children(self):
        self.food_number_lbl.grid(row=0, column=0, padx=5, pady=10, sticky='we')
        self.food_name_lbl.grid(row=0, column=1, padx=5, pady=10, sticky='we')
        self.calories_lbl.grid(row=0, column=2, padx=5, pady=10, sticky='we')
        self.fat_lbl.grid(row=0, column=3, padx=5, pady=10, sticky='we')
        self.sat_fat_lbl.grid(row=0, column=4, padx=5, pady=10, sticky='we')
        self.carbs_lbl.grid(row=0, column=5, padx=5, pady=10, sticky='we')
        self.sugar_lbl.grid(row=0, column=6, padx=5, pady=10, sticky='we')
        self.protein_lbl.grid(row=0, column=7, padx=5, pady=10, sticky='we')
        self.fiber_lbl.grid(row=0, column=8, padx=5, pady=10, sticky='we')

    
    def _refresh_food_names(self):
        self.food_label_names = self.db.all_food_label_names
        self.food_label_names_lboxvar.set(self.food_label_names)
        self.food_names_lbox.configure(listvariable=self.food_label_names_lboxvar)
        self.search_entry_var.set('')
        
        self.results_frame.grid_forget()
        self._create_result_frame()
        self._create_results_frame_children()
        self._grid_results_frame_children()
    
    def _search_by_name(self):
        search_token = self.search_entry_var.get()
        self.filtered_names = [name for name in self.food_label_names if search_token.lower() in name.lower()]
        self.filtered_names_var = StringVar(value=self.filtered_names)
        self.food_names_lbox.configure(listvariable=self.filtered_names_var)
    
    def _get_record_from_doubleclick(self, event):
        # Currently only one item box can be selected
        food_idx = self.food_names_lbox.curselection()[0]
        try:
            # first try to find it among filtered names
            food_name = self.filtered_names[food_idx]
        except AttributeError:
            # otherwise it has to be using the main names array
            food_name = self.food_label_names[food_idx]
        self._render_searched_result(self.db.get_food_item_table(food_name))
    
    def _style_lbox_items(self):
        for i in range(0, len(self.food_label_names), 2):
            self.food_names_lbox.itemconfigure(i, background='#fff3e6')

    def _render_searched_result(self, food_results):
        # first clear all rendered results(if any)
        self.results_frame.grid_forget()
        # re-render the table headers
        self._create_result_frame()
        self._create_results_frame_children()
        self._grid_results_frame_children()

        # Expected to be a 1-element list, could change in future
        for row_idx, food_table_record in enumerate(food_results):
            food_table_record = list(food_table_record[1:])
            for col_idx, val in enumerate([row_idx + 1] + food_table_record):
                try:
                    val = round(float(val), 2)
                except ValueError:
                    # only for name column
                    ...
                lbl = ttk.Label(self.results_frame, text=val, borderwidth=2, relief='raised', padding=8, anchor='center', background='#ffffcc')
                lbl.grid(row= 4 + row_idx + 1, column=col_idx, padx=5)