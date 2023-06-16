import datetime

from tkinter import ttk, StringVar, Listbox

from ...utility_widgets.leaf_frames import FoodTableResultsFrame, ScrollBarWidget
from constants.constants import consumed_food_headers, consumed_food_map
from .top_level_dialogs import DialogPickerTopLevel


class CreateTemplateOptionsFrame:
    """Frame for rendering options of searching and adding new meal template."""
    
    def __init__(self, parent, db):
        self.db = db
        self.parent = parent

        self._create_mutual_label_options()

        self._create_styles()

        self.frame = ttk.Frame(parent.frame, style='CFoodSearchOptions.TFrame', padding=(200, 50))
        for i in range(5):
            self.frame.columnconfigure(i, weight=1)

        self._create_mutual_combobox_options()
        self._create_mutual_button_options()

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

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.frame,
            'style': 'CFoodSearch.TButton',
            'cursor': 'hand2',
        }

    def _create_mutual_label_options(self):
        self.mutual_label_options = {
            'borderwidth': 2,
            'relief': 'ridge',
            'anchor': 'center',
            'padding': 8,
            'font': 'default 11',
        }

    def _create_styles(self):
        ttk.Style().configure('CFoodSearchOptions.TFrame', background='#F8FCE8', borderwidth=3, relief='ridge')
        ttk.Style().configure('CFoodTopic.TLabel', anchor='center', borderwidth=2, relief='ridge', background='#BFBFBF', font='default 12')
        ttk.Style().configure('CFoodText.TLabel', anchor='center', padding=2, font='default 12', background='#F8FCE8')
        ttk.Style().configure('CFoodSearch.TButton', anchor='center', padding=5, font='default 11')
        ttk.Style().configure('CFoodRadio.TRadiobutton', anchor='center', padding=5, font='default 10', background='#BFBFBF')
        ttk.Style().configure('CreateTemplateSearchLbl.TLabel', background='#bfff80', **self.mutual_label_options)

    def _create_widget_vars(self):
        self.search_name_e_var = StringVar()
        self.tally_results_var = StringVar()

        self.food_results_lbox_values = []
        self.food_results_lbox_var = StringVar(value=self.food_results_lbox_values)

        self.food_name_var = StringVar()
        self.food_weight_var = StringVar()

    def _create_widgets(self):
        self.search_name_lbl = ttk.Label(self.frame, text='Pretraži artikle', style='CreateTemplateSearchLbl.TLabel')
        self.search_name_e = ttk.Entry(self.frame, textvariable=self.search_name_e_var, font='default 12', width=30)

        self.vertical_separator = ttk.Separator(self.frame, orient='vertical')

        self.tally_results_lbl = ttk.Label(self.frame, textvariable=self.tally_results_var, style='CreateTemplateSearchLbl.TLabel')
        self.food_results_lbox = Listbox(self.frame, listvariable=self.food_results_lbox_var, cursor='hand2', width=40, height=5)
        self.food_results_scrolly = ScrollBarWidget(self.frame)
        self.food_results_scrolly.attach_to_scrollable(self.food_results_lbox)

        self.horizontal_separator = ttk.Separator(self.frame, orient='horizontal')

        self.food_name_lbl = ttk.Label(self.frame, text='Naziv artikla', style='CFoodText.TLabel')
        self.food_name_e = ttk.Entry(self.frame, textvariable=self.food_name_var, font='default 12', width=40, justify='center', state='readonly')

        self.food_weight_lbl = ttk.Label(self.frame, text='Masa artikla', style='CFoodText.TLabel')
        self.food_weight_e = ttk.Entry(self.frame, textvariable=self.food_weight_var, font='default 12')

        self.add_template_btn = ttk.Button(self.frame, text='Dodaj u predložak', cursor='hand2')

    def _grid_widgets(self):
        self.search_name_lbl.grid(row=0, column=0, columnspan=2, padx=(0, 10), pady=(0, 10))
        self.search_name_e.grid(row=1, column=0, columnspan=2, padx=(0, 10), pady=(0, 30))

        self.vertical_separator.grid(row=0, column=2, rowspan=5, sticky='ns')

        self.tally_results_lbl.grid(row=0, column=3, columnspan=2, padx=(80, 0), pady=(0, 20))
        self.food_results_lbox.grid(row=1, column=3, columnspan=2, padx=(80, 0), pady=(0, 30), sticky='we')
        self.food_results_scrolly.scroll_bar.grid(row=1, column=4, sticky='ens', pady=(0, 30))
        # self.food_results_scrolly.grid(row=1, column=5, columnspan=1)

        self.horizontal_separator.grid(row=2, column=0, columnspan=6, sticky='we')

        self.food_name_lbl.grid(row=3, column=0, columnspan=2, padx=(0, 10), pady=(100, 10))
        self.food_name_e.grid(row=4, column=0, columnspan=2, padx=(0, 10), pady=(0, 50))

        self.food_weight_lbl.grid(row=3, column=3, columnspan=2, padx=(10, 0), pady=(100, 10))
        self.food_weight_e.grid(row=4, column=3, columnspan=2, padx=(10, 0), pady=(0, 50))

        self.add_template_btn.grid(row=5, column=0, columnspan=5, pady=(50, 0))
    
    def _bind_events(self):
        self.food_results_lbox.bind('<<ListboxSelect>>', lambda _: self._set_food_name())
        # self.frame.bind('<Button-4>', lambda _: self.scroll_up_handler())
        # self.frame.bind('<Button-5>', lambda _: self.scroll_down_handler())
        # self.search_name_e.bind('<Return>', lambda _: self._search_by_name())

    def _set_food_name(self):
        if not self.food_results_lbox.curselection():
            # NOTE: some weird error which I didn't debug yet
            return
        idx, = self.food_results_lbox.curselection()
        self.food_name_var.set(self.food_results_lbox_values[idx])
    
    def _search_foods(self):
        pass
        # from_d, from_m, from_y = [v.get()
        #                           for v in (self.time_from_day_var,
        #                                     self.time_from_month_var,
        #                                     self.time_from_year_var)]
        # start_time = datetime.datetime.strptime(f'{from_d}-{from_m}-{from_y}', '%d-%m-%Y')
        # to_d, to_m, to_y = [v.get()
        #                     for v in (self.time_to_day_var,
        #                               self.time_to_month_var,
        #                               self.time_to_year_var)]
        # if not any(x for x in (to_d, to_m, to_y)):
        #     end_time = None
        # else:
        #     # NOTE: subject to change in Future
        #     to_d = to_d or '1'
        #     to_m = to_m or '1'
        #     to_y = to_y or start_time.year + 1
        #     end_time = datetime.datetime.strptime(f'{to_d}-{to_m}-{to_y}', '%d-%m-%Y')
        #     # make changes visible to the user
        #     self.time_to_day_var.set(to_d)
        #     self.time_to_month_var.set(to_m)
        #     self.time_to_year_var.set(to_y)
        # food_name = self.search_name_e_var.get().strip()
        # self.parent.search_foods(start_time, end_time, food_name)

    def _sort_results(self):
        pass
        # sort_option = self.selected_sort_option_var.get()
        # if sort_option:
        #     sort_direction = self.sort_option_direction_var.get()
        #     rev = True if sort_direction == 'desc' else False
        #     self.parent.sort_results(sort_option, rev)

    def _search_by_name(self):
        pass
        # c_food_name = self.search_name_e_var.get().strip()
        # self.parent.search_by_name(c_food_name)

    def _update_tally_cnt(self):
        cnt = len(self.food_results_lbox_values)
        cnt_s = str(cnt).zfill(2)
        text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        self.tally_results_var.set(f'{cnt} {text}')

    def _color_listbox_foods(self):
        for i in range(len(self.food_results_lbox_values)):
            clr = 'white' if i % 2 == 0 else '#E6E6E6'
            self.food_results_lbox.itemconfigure(i, background=clr)

    def grid_frame(self, row, column, sticky):
        self.frame.grid(row=row, column=column, sticky=sticky, padx=(300), pady=(0, 20))
    
    def configure_style(self, style_name):
        self.frame.configure(style=style_name)
    
    def set_scroll_up_handler(self, callback):
        self.scroll_up_handler = callback
    
    def set_scroll_down_handler(self, callback):
        self.scroll_down_handler = callback

    def update_food_label_names(self, food_names):
        # TODO: make this work properly; ie. justify the text by center
        # self.food_results_lbox_values = [x.rjust((120 - len(x)) // 2) for x in food_names]
        self.food_results_lbox_values = food_names
        self.food_results_lbox_var.set(self.food_results_lbox_values)
        self._update_tally_cnt()
        self._color_listbox_foods()


class CreateMealTemplateFrame:
    """Frame representing UI and its logic for creating a new meal template."""

    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        # self.all_food_names = self.get_all_food_label_names()

        self._create_styles()

        self.frame = ttk.Frame(parent.canvas, style='CreateTemplate.TFrame')
        self.frame.grid(row=0, column=0, sticky='news')
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

    def _create_styles(self):
        ttk.Style().configure('CreateTemplate.TFrame', background='#BAB9B9')
        ttk.Style().configure('CreateTemplateTopic.TLabel', anchor='center', font='Helvetica 15', padding=20)

    def _create_widget_vars(self):
        self.topic_lbl_text = 'Kreiraj novi predložak objeda'

        # self.consumed_food_tally_lbl_var = StringVar(value='0 rezultata')

    def _create_widgets(self):
        self.topic_lbl = ttk.Label(self.frame, text=self.topic_lbl_text, style='CreateTemplateTopic.TLabel')
        
        self.create_meal_options_frame = CreateTemplateOptionsFrame(self, self.db)
        self.create_meal_options_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.create_meal_options_frame.set_scroll_down_handler(self.parent.handle_scroll_down)

        self.save_template_btn = ttk.Button(self.frame, text='Trajno pohrani predložak', command=lambda: ..., cursor='hand2')

        self.consumed_food_table_frame = FoodTableResultsFrame(self, consumed_food_headers.values())
        self.consumed_food_table_frame.configure_style('CreateTemplate.TFrame')
        self.consumed_food_table_frame.set_row_callback(self._open_update_center)
        self.consumed_food_table_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.consumed_food_table_frame.set_scroll_down_handler(self.parent.handle_scroll_down)

    def _grid_widgets(self):
        self.topic_lbl.grid(row=0, column=0, sticky='we', padx=(15, 30), pady=(50, 30))
        self.create_meal_options_frame.grid_frame(row=1, column=0, sticky='we')
        self.save_template_btn.grid(row=2, column=0, pady=(0, 30))
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
        # uncolor the sorting column since it was present for the old results
        self.consumed_food_table_frame.unmark_column()
        # Clear all rendered rows
        self.consumed_food_table_frame.destroy_rows()
        # re-render them with the updated list of food tables
        self.consumed_food_table_frame.render_results(self.consumed_foods)
        # render the tally row
        self.consumed_food_table_frame.render_tally_row(self.tally_row)

        # since there are 2 search operation, save the last one used by a user
        self.last_search_operation = self.create_meal_options_frame._search_foods

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
        self.consumed_food_table_frame.mark_column(idx)
        if idx == consumed_food_map['food_name']:
            # sort by name works based on ASCII -> compare with case insensitivity
            self.consumed_foods.sort(key=lambda row: row[idx].lower(), reverse=rev)
        elif idx == consumed_food_map['created_on']:
            # sort by datetime instances instead of strings representing datetime stamp
            self.consumed_foods.sort(key=lambda row: datetime.datetime.strptime(row[idx], '%d-%m-%Y, %H:%M'), reverse=rev)
        else:
            self.consumed_foods.sort(key=lambda row: row[idx], reverse=rev)
        # Clear all rendered rows
        self.consumed_food_table_frame.destroy_rows()
        # re-render them with the sorted list of food tables
        self.consumed_food_table_frame.render_results(self.consumed_foods)
        # render the tally row
        self.consumed_food_table_frame.render_tally_row(self.tally_row)

    def search_by_name(self, food_name):
        """Search all consumed foods based only on the given name

        The filtering is based ond the `in` operator and case sensitivity is ignored.
        """
        consumed_food_names = self.db.get_all_consumed_food_names()
        # if food_name is empty return all results, otherwise do the filtering
        if food_name:
            food_name = food_name.lower()
            consumed_food_names = [fn for fn in consumed_food_names if food_name in fn.lower()]
        self.consumed_foods = [fr
                               for fn in consumed_food_names
                               for fr in self.db.get_consumed_foods_by_name(fn)]

        # update the number of results label
        cnt = len(self.consumed_foods)
        cnt_s = str(cnt).zfill(2)
        text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        self.consumed_food_tally_lbl_var.set(f'{cnt} {text}')

        # calculate earliest and latest timestamps
        min_t, max_t = self._get_edge_timestamps()

        self.tally_row = self._calculate_tally_row(min_t, max_t)
        # uncolor the sorting column since it was present for the old results
        self.consumed_food_table_frame.unmark_column()
        # Clear all rendered rows
        self.consumed_food_table_frame.destroy_rows()
        # re-render them with the updated list of food tables
        self.consumed_food_table_frame.render_results(self.consumed_foods)
        # render the tally row
        self.consumed_food_table_frame.render_tally_row(self.tally_row)

        # since there are 2 search operation, save the last one used by a user
        self.last_search_operation = self.create_meal_options_frame._search_by_name

    def _get_edge_timestamps(self):
        """Return earliest and latest from consumed food results

        # NOTE: not the best design, but I'll live with it -> I had to adhere to `_calculate_tally_row` API
        If timestamps is empty return dummy values(datetime.now()).
        If earliest and latest timestamps are the same return only one and None
        Otherwise return both of them.
        """
        time_idx = consumed_food_map['created_on']
        timestamps = [cf[time_idx] for cf in self.consumed_foods]
        if not timestamps:
            return datetime.datetime.now(), datetime.datetime.now()
        min_t, max_t = min(timestamps), max(timestamps)
        start_time = datetime.datetime.strptime(min_t, '%d-%m-%Y, %H:%M')
        end_time = datetime.datetime.strptime(max_t, '%d-%m-%Y, %H:%M')
        if start_time == end_time:
            return start_time, None
        return start_time, end_time

    def _open_update_center(self, p_key):
        pass
        # Fetch the complete table row since consumed food name is not globally unique
        # consumed_food_row = self.db.get_consumed_food_by_primary_key(p_key)
        # DialogPickerTopLevel(self, self.db, consumed_food_row)

    def update_food_label_names(self):
        self.all_food_names = self.db.all_food_label_names
        self.create_meal_options_frame.update_food_label_names(self.all_food_names)

