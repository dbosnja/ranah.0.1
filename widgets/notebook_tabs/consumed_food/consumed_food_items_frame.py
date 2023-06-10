import datetime

from tkinter import ttk, StringVar

from ...utility_widgets.leaf_frames import FoodTableResultsFrame 
from constants.constants import consumed_food_headers


class ConsumedFoodSearchOptionsFrame:
    """Frame for rendering options of searching and sorting for consumed food tab."""
    
    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self._create_styles()

        self.frame = ttk.Frame(parent.frame, style='ConsumedFoodSearchOptions.TFrame')

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('ConsumedFoodSearchOptions.TFrame', background='#F0DBDB')
        ttk.Style().configure('ConsumedFoodTopicLabel.TLabel', anchor='center', borderwidth=2, relief='ridge', padding=6, font='default 12')

    def _create_widget_vars(self):
        self.time_segment_from_day_var = StringVar()
        self.time_segment_from_month_var = StringVar()
        self.time_segment_from_year_var = StringVar()
        self.time_segment_to_day_var = StringVar()
        self.time_segment_to_month_var = StringVar()
        self.time_segment_to_year_var = StringVar()
        self.search_name_e_var = StringVar()

        self.selected_sort_option_var = StringVar()
        self.sort_option_direction_var = StringVar()

    def _create_widgets(self):
        self.search_options_topic_lbl = ttk.Label(self.frame, text='Opcije pretraživanja', style='ConsumedFoodTopicLabel.TLabel')
        self.search_name_lbl = ttk.Label(self.frame, text='Naziv konzumiranog artikla')
        self.search_name_e = ttk.Entry(self.frame, textvariable=self.search_name_e_var)
        
        self.time_segment_lbl = ttk.Label(self.frame, text='Vremenski raspon konzumiranja')
        self.time_segment_from_lbl = ttk.Label(self.frame, text='Od')
        self.time_segment_to_lbl = ttk.Label(self.frame, text='Do')
        self.time_segment_from_day_c = ttk.Combobox(self.frame, values=list(range(1, 32)), height=5, textvariable=self.time_segment_from_day_var, state='readonly', width=5)
        self.time_segment_from_month_c = ttk.Combobox(self.frame, values=list(range(1, 13)), height=5, textvariable=self.time_segment_from_month_var, state='readonly', width=5)
        self.time_segment_from_year_c = ttk.Combobox(self.frame, values=list(range(2023, 2026)), height=5, textvariable=self.time_segment_from_year_var, state='readonly', width=5)
        self.time_segment_to_day_c = ttk.Combobox(self.frame, values=list(range(1, 32)), height=5, textvariable=self.time_segment_to_day_var, state='readonly', width=5)
        self.time_segment_to_month_c = ttk.Combobox(self.frame, values=list(range(1, 13)), height=5, textvariable=self.time_segment_to_month_var, state='readonly', width=5)
        self.time_segment_to_year_c = ttk.Combobox(self.frame, values=list(range(2023, 2026)), height=5, textvariable=self.time_segment_to_year_var, state='readonly', width=5)
        self.search_btn = ttk.Button(self.frame, text='Pretraži', command=self.parent._search_foods, cursor='hand2')

        self.sort_options_topic_lbl = ttk.Label(self.frame, text='Opcije sortiranja', style='ConsumedFoodTopicLabel.TLabel')
        self.sort_options_cbox = ttk.Combobox(self.frame, values=list(consumed_food_headers.values())[1:], state='readonly',
                                              textvariable=self.selected_sort_option_var)
        self.ascending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Uzlazno', variable=self.sort_option_direction_var, value='asc')
        self.descending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Silazno', variable=self.sort_option_direction_var, value='desc')
        self.sort_btn = ttk.Button(self.frame, text='Sortiraj', cursor='hand2')

    def _grid_widgets(self):
        self.search_options_topic_lbl.grid(row=0, column=0, columnspan=6, pady=(10, 20))
        self.search_name_lbl.grid(row=1, column=0, columnspan=3)
        self.search_name_e.grid(row=1, column=3, columnspan=3)
        
        self.time_segment_lbl.grid(row=2, column=0, columnspan=6)
        self.time_segment_from_lbl.grid(row=3, column=0, columnspan=3)
        self.time_segment_to_lbl.grid(row=3, column=3, columnspan=3)
        self.time_segment_from_day_c.grid(row=4, column=0)
        self.time_segment_from_month_c.grid(row=4, column=1)
        self.time_segment_from_year_c.grid(row=4, column=2)
        self.time_segment_to_day_c.grid(row=4, column=3)
        self.time_segment_to_month_c.grid(row=4, column=4)
        self.time_segment_to_year_c.grid(row=4, column=5)
        self.search_btn.grid(row=5, column=0, columnspan=6)

        self.sort_options_topic_lbl.grid(row=6, column=0, columnspan=6, pady=(10, 20))
        self.sort_options_cbox.grid(row=7, column=0, columnspan=3)
        self.ascending_sort_option_rbtn.grid(row=7, column=3, columnspan=2)
        self.descending_sort_option_rbtn.grid(row=7, column=5, columnspan=2)
        self.sort_btn.grid(row=8, column=0, columnspan=7)
    
    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.scroll_up_handler())
        self.frame.bind('<Button-5>', lambda _: self.scroll_down_handler())
    
    def _search_foods(self):
        self.consumed_foods = self.db.get_consumed_food_on_date(datetime.datetime.strptime('01-06-23', '%d-%m-%y'))

    def grid_frame(self, row, column, sticky):
        self.frame.grid(row=row, column=column, sticky=sticky)
    
    def configure_style(self, style_name):
        self.frame.configure(style=style_name)
    
    def set_scroll_up_handler(self, callback):
        self.scroll_up_handler = callback
    
    def set_scroll_down_handler(self, callback):
        self.scroll_down_handler = callback


class ConsumedFoodItemsFrame:
    """Frame representing UI for searching consumed food at some point in time"""

    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self._create_styles()

        self.frame = ttk.Frame(parent.canvas, style='ConsumedFoodItems.TFrame')
        self.frame.grid(row=0, column=0, sticky='news')
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('ConsumedFoodItems.TFrame', background='#F0DBDB')
        ttk.Style().configure('ConsumedFoodTopic.TLabel', anchor='center', font='Helvetica 15', padding=20)

    def _create_widget_vars(self):
        self.topic_lbl_text = 'Pretraži konzumiranu hranu'

    def _create_widgets(self):
        self.topic_lbl = ttk.Label(self.frame, text=self.topic_lbl_text, style='ConsumedFoodTopic.TLabel')
        
        self.consumed_food_search_options_frame = ConsumedFoodSearchOptionsFrame(self, self.db)
        self.consumed_food_search_options_frame.configure_style('ConsumedFoodItems.TFrame')
        self.consumed_food_search_options_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.consumed_food_search_options_frame.set_scroll_down_handler(self.parent.handle_scroll_down)
        
        self.consumed_food_table_frame = FoodTableResultsFrame(self, consumed_food_headers.values())
        self.consumed_food_table_frame.configure_style('ConsumedFoodItems.TFrame')
        self.consumed_food_table_frame.set_row_callback(lambda _: ...)
        self.consumed_food_table_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.consumed_food_table_frame.set_scroll_down_handler(self.parent.handle_scroll_down)

    def _grid_widgets(self):
        self.topic_lbl.grid(row=0, column=0, sticky='we', padx=(15, 30), pady=(50, 30))
        self.consumed_food_search_options_frame.grid_frame(row=1, column=0, sticky='we')
        self.consumed_food_table_frame.grid_frame(row=2, column=0, sticky='we')
    
    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.parent.handle_scroll_up())
        self.frame.bind('<Button-5>', lambda _: self.parent.handle_scroll_down())
    
    def _search_foods(self):
        self.consumed_foods = self.db.get_consumed_food_on_date(datetime.datetime.strptime('01-06-23', '%d-%m-%y'))
        self.consumed_food_table_frame.destroy_rows()
        self.consumed_food_table_frame.render_results(self.consumed_foods)

