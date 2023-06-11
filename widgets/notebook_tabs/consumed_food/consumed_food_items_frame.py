import datetime

from tkinter import ttk, StringVar

from ...utility_widgets.leaf_frames import FoodTableResultsFrame 
from constants.constants import consumed_food_headers, consumed_food_map


class ConsumedFoodSearchOptionsFrame:
    """Frame for rendering options of searching and sorting for consumed foods tab."""
    
    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self._create_styles()

        self.frame = ttk.Frame(parent.frame, style='CFoodSearchOptions.TFrame', padding=(40, 30))

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
        ttk.Style().configure('CFoodSearchOptions.TFrame', background='#F8FCE8', borderwidth=3, relief='ridge')
        ttk.Style().configure('CFoodTopic.TLabel', anchor='center', borderwidth=2, relief='ridge', background='#BFBFBF', font='default 12')
        ttk.Style().configure('CFoodText.TLabel', anchor='center', padding=2, font='default 12', background='#F8FCE8')
        ttk.Style().configure('CFoodSearch.TButton', anchor='center', padding=5, font='default 11')
        ttk.Style().configure('CFoodRadio.TRadiobutton', anchor='center', padding=5, font='default 10', background='#BFBFBF')

    def _create_widget_vars(self):
        today = datetime.datetime.now()

        self.search_name_e_var = StringVar()

        self.time_from_day_var = StringVar()
        self.time_from_day_var.set(today.day)
        self.time_from_month_var = StringVar()
        self.time_from_month_var.set(today.month)
        self.time_from_year_var = StringVar()
        self.time_from_year_var.set(today.year)

        self.time_to_day_var = StringVar()
        self.time_to_month_var = StringVar()
        self.time_to_year_var = StringVar()

        self.selected_sort_option_var = StringVar()
        self.sort_option_direction_var = StringVar()

    def _create_widgets(self):
        self.search_options_topic_lbl = ttk.Label(self.frame, text='Opcije pretraživanja', style='CFoodTopic.TLabel', padding=6)
        self.search_name_lbl = ttk.Label(self.frame, text='Naziv konzumiranog artikla', style='CFoodText.TLabel')
        self.search_name_e = ttk.Entry(self.frame, textvariable=self.search_name_e_var, font='default 12')
        
        self.time_lbl = ttk.Label(self.frame, text='Vremenski raspon konzumiranja', style='CFoodText.TLabel')
        self.time_from_lbl = ttk.Label(self.frame, text='Od', style='CFoodText.TLabel')
        self.time_to_lbl = ttk.Label(self.frame, text='Do', style='CFoodText.TLabel')
        self.time_from_day_c = ttk.Combobox(values=list(range(1, 32)), textvariable=self.time_from_day_var,
                                            **self.mutual_cbox_options, cursor='hand2')
        self.time_from_month_c = ttk.Combobox(values=list(range(1, 13)), textvariable=self.time_from_month_var,
                                              **self.mutual_cbox_options, cursor='hand2')
        self.time_from_year_c = ttk.Combobox(values=list(range(2023, 2026)), textvariable=self.time_from_year_var,
                                             **self.mutual_cbox_options, cursor='hand2')
        self.time_to_day_c = ttk.Combobox(values=[''] + list(range(1, 32)), textvariable=self.time_to_day_var,
                                          **self.mutual_cbox_options, cursor='hand2')
        self.time_to_month_c = ttk.Combobox(values=[''] + list(range(1, 13)), textvariable=self.time_to_month_var,
                                            **self.mutual_cbox_options, cursor='hand2')
        self.time_to_year_c = ttk.Combobox(values=[''] + list(range(2023, 2026)), textvariable=self.time_to_year_var,
                                           **self.mutual_cbox_options, cursor='hand2')
        self.search_btn = ttk.Button(self.frame, text='Pretraži', command=self._search_foods, style='CFoodSearch.TButton', cursor='hand2')

        self.vertical_separator = ttk.Separator(self.frame, orient='vertical')
        self.sort_options_topic_lbl = ttk.Label(self.frame, text='Opcije sortiranja', style='CFoodTopic.TLabel', padding=6)
        self.sort_options_cbox = ttk.Combobox(self.frame, values=list(consumed_food_headers.values())[1:], state='readonly',
                                              textvariable=self.selected_sort_option_var, cursor='hand2')
        self.ascending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Uzlazno',
                                                          variable=self.sort_option_direction_var, value='asc',
                                                          style='CFoodRadio.TRadiobutton', cursor='hand2')
        self.descending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Silazno',
                                                           variable=self.sort_option_direction_var, value='desc',
                                                           style='CFoodRadio.TRadiobutton', cursor='hand2')
        self.sort_btn = ttk.Button(self.frame, text='Sortiraj', style='CFoodSearch.TButton', cursor='hand2', command=self._sort_results)

    def _grid_widgets(self):
        self.search_options_topic_lbl.grid(row=0, column=0, columnspan=6, pady=(0, 30))
        self.search_name_lbl.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        self.search_name_e.grid(row=1, column=3, columnspan=3, pady=(0, 10))
        
        self.time_lbl.grid(row=2, column=0, columnspan=6, pady=(5, 10))
        self.time_from_lbl.grid(row=3, column=0, columnspan=3, pady=(0, 5))
        self.time_to_lbl.grid(row=3, column=3, columnspan=3, pady=(0, 5))
        self.time_from_day_c.grid(row=4, column=0)
        self.time_from_month_c.grid(row=4, column=1)
        self.time_from_year_c.grid(row=4, column=2, padx=(0, 20))
        self.time_to_day_c.grid(row=4, column=3)
        self.time_to_month_c.grid(row=4, column=4)
        self.time_to_year_c.grid(row=4, column=5)
        self.search_btn.grid(row=5, column=0, columnspan=6, pady=(30, 0))

        self.vertical_separator.grid(row=0, column=6, rowspan=6, sticky='ns', padx=(60, 0))
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
        from_d, from_m, from_y = [v.get()
                                  for v in (self.time_from_day_var,
                                            self.time_from_month_var,
                                            self.time_from_year_var)]
        start_time = datetime.datetime.strptime(f'{from_d}-{from_m}-{from_y}', '%d-%m-%Y')
        to_d, to_m, to_y = [v.get()
                            for v in (self.time_to_day_var,
                                      self.time_to_month_var,
                                      self.time_to_year_var)]
        if not any(x for x in (to_d, to_m, to_y)):
            end_time = None
        else:
            # NOTE: subject to change in Future
            to_d = to_d or '1'
            to_m = to_m or '1'
            to_y = to_y or start_time.year + 1
            end_time = datetime.datetime.strptime(f'{to_d}-{to_m}-{to_y}', '%d-%m-%Y')
            # make changes visible to the user
            self.time_to_day_var.set(to_d)
            self.time_to_month_var.set(to_m)
            self.time_to_year_var.set(to_y)
        food_name = self.search_name_e_var.get().strip()
        self.consumed_foods = self.parent.search_foods(start_time, end_time, food_name)

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

        self.consumed_food_tally_lbl_var = StringVar()
        self.consumed_food_tally_lbl_var.set('0 rezultata')

    def _create_widgets(self):
        self.topic_lbl = ttk.Label(self.frame, text=self.topic_lbl_text, style='ConsumedFoodTopic.TLabel')
        
        self.consumed_food_search_options_frame = ConsumedFoodSearchOptionsFrame(self, self.db)
        self.consumed_food_search_options_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.consumed_food_search_options_frame.set_scroll_down_handler(self.parent.handle_scroll_down)

        self.food_tables_tally_lbl = ttk.Label(self.frame, borderwidth=2, relief='ridge', textvariable=self.consumed_food_tally_lbl_var, padding=5)

        self.consumed_food_table_frame = FoodTableResultsFrame(self, consumed_food_headers.values())
        self.consumed_food_table_frame.configure_style('ConsumedFoodItems.TFrame')
        self.consumed_food_table_frame.set_row_callback(lambda _: ...)
        self.consumed_food_table_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.consumed_food_table_frame.set_scroll_down_handler(self.parent.handle_scroll_down)

    def _grid_widgets(self):
        self.topic_lbl.grid(row=0, column=0, sticky='we', padx=(15, 30), pady=(50, 30))
        self.consumed_food_search_options_frame.grid_frame(row=1, column=0, sticky='w')
        self.food_tables_tally_lbl.grid(row=2, column=0, sticky='w', padx=(5, 0), pady=(30, 10))
        self.consumed_food_table_frame.grid_frame(row=3, column=0, sticky='we')

    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.parent.handle_scroll_up())
        self.frame.bind('<Button-5>', lambda _: self.parent.handle_scroll_down())

    def search_foods(self, start_time, end_time, food_name):
        """Search food by start time and optionally by end time and food name

        After filtering is done, update the total number of results, delete old
        and render new results.
        """
        self.consumed_foods = self.db.get_consumed_food_on_date(start_time, end_time)
        if food_name:
            food_name = food_name.lower()
            self.consumed_foods = [f for f in self.consumed_foods if food_name in f[1].lower()]

        # update the number of results label
        cnt = len(self.consumed_foods)
        cnt_s = str(cnt).zfill(2)
        text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        self.consumed_food_tally_lbl_var.set(f'{cnt} {text}')

        self.tally_row = self._calculate_tally_row(start_time, end_time)

        # Clear all rendered rows
        self.consumed_food_table_frame.destroy_rows()
        # re-render them with the updated list of food tables
        self.consumed_food_table_frame.render_results(self.consumed_foods)
        # render the tally row
        self.consumed_food_table_frame.render_tally_row(self.tally_row)

    def _calculate_tally_row(self, start_time, end_time):
        """Return the sum of all rows or None if no rows present"""
        if not self.consumed_foods:
            return None
        tally_time = f"{f'{start_time.day}'.zfill(2)}-{f'{start_time.month}'.zfill(2)}-{start_time.year}"
        if end_time:
            tally_time = tally_time + '  <-->  ' + f"{f'{end_time.day}'.zfill(2)}-{f'{end_time.month}'.zfill(2)}-{end_time.year}"
        sorting_idx = list(consumed_food_map.values())[2:-1]
        tally_row = [sum([row[i] for row in self.consumed_foods]) for i in sorting_idx]
        tally_row = [int(i) if int(i) == round(i, 2) else round(i, 2) for i in tally_row]
        tally_row  = ['\u2211', 'Ukupno'] + tally_row + [tally_time]
        return tally_row

    def sort_results(self, sort_option, rev):
        """Sort current results by `sort_option` and reverse the results if `rev=True`"""

        # Find the corresponding index from the centralized back-patching defintion
        for k, v in consumed_food_headers.items():
            if v == sort_option:
                idx = consumed_food_map[k]
                break
        if idx == 1:
            # sort by name works based on ASCII -> compare with case insensitivity
            self.consumed_foods.sort(key=lambda row: row[idx].lower(), reverse=rev)
        else:
            self.consumed_foods.sort(key=lambda row: row[idx], reverse=rev)
        # Clear all rendered rows
        self.consumed_food_table_frame.destroy_rows()
        # re-render them with the sorted list of food tables
        self.consumed_food_table_frame.render_results(self.consumed_foods)
        # render the tally row
        self.consumed_food_table_frame.render_tally_row(self.tally_row)

