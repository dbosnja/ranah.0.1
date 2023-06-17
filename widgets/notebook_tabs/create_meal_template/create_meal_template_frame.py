import re
from datetime import datetime, timedelta

from tkinter import ttk, StringVar, Listbox, messagebox

from ...utility_widgets.leaf_frames import FoodTableResultsFrame, ScrollBarWidget
from constants.constants import consumed_food_headers, consumed_food_map, NORMATIVE, nutrition_table_map
from .top_level_dialogs import DialogPickerTopLevel


class CreateTemplateOptionsFrame:
    """Frame for rendering options of searching and adding new meal template."""
    
    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self.last_pressed_button = datetime.now()
        self.last_pressed_button_interval = timedelta(microseconds=1)

        self._create_mutual_label_options()

        self._create_styles()

        self.frame = ttk.Frame(parent.frame, style='CFoodSearchOptions.TFrame', padding=(200, 20))
        for i in range(5):
            self.frame.columnconfigure(i, weight=1)

        # define validations
        self.food_weight_re = re.compile('^[1-9]\d{,3}$')
        self._validate_food_weight = self.frame.register(self._validate_food_weight_input), '%P'

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
        ttk.Style().configure('CreateTemplateUpperLbl.TLabel', background='#bfff80', **self.mutual_label_options)
        ttk.Style().configure('CreateTemplateBottomLbl.TLabel', background='#E882C8', **self.mutual_label_options)
        ttk.Style().configure('CreateTemplateFoodEntry.TEntry', readonlybackground='white')

        self.add_btn_style = ttk.Style()
        self.add_btn_style.configure('CreateTemplateActiveAddBtn.TButton', font='default 11', padding=10)
        self.add_btn_style.map('CreateTemplateActiveAddBtn.TButton', background=[('active', '#00994D')])

    def _create_widget_vars(self):
        self.search_name_e_var = StringVar()
        self.tally_results_var = StringVar()

        self.food_results_lbox_values = []
        self.food_results_lbox_var = StringVar(value=self.food_results_lbox_values)

        self.food_name_var = StringVar()
        self.food_weight_var = StringVar()

    def _create_widgets(self):
        self.search_name_lbl = ttk.Label(self.frame, text='Pretraži prehrambene artikle', style='CreateTemplateUpperLbl.TLabel')
        self.search_name_e = ttk.Entry(self.frame, textvariable=self.search_name_e_var, font='default 12', width=30)

        self.vertical_separator = ttk.Separator(self.frame, orient='vertical')

        self.tally_results_lbl = ttk.Label(self.frame, textvariable=self.tally_results_var, style='CreateTemplateUpperLbl.TLabel')
        self.food_results_lbox = Listbox(self.frame, listvariable=self.food_results_lbox_var, cursor='hand2', width=40, height=5)
        self.food_results_scrolly = ScrollBarWidget(self.frame)
        self.food_results_scrolly.attach_to_scrollable(self.food_results_lbox)

        self.horizontal_separator = ttk.Separator(self.frame, orient='horizontal')
        self.horizontal_separator.lower()

        self.food_name_lbl = ttk.Label(self.frame, text='Naziv artikla', style='CreateTemplateBottomLbl.TLabel')
        self.food_name_e = ttk.Entry(self.frame, textvariable=self.food_name_var, font='default 12', width=40,
                                     justify='center', state='readonly', style='CreateTemplateFoodEntry.TEntry')

        self.food_weight_lbl = ttk.Label(self.frame, text='Masa artikla', style='CreateTemplateBottomLbl.TLabel')
        self.food_weight_e = ttk.Entry(self.frame, textvariable=self.food_weight_var, font='default 12', width=10,
                                       justify='center', validate='key', validatecommand=self._validate_food_weight)

        self.add_template_btn = ttk.Button(self.frame, text='Dodaj u predložak', state='disabled',
                                           command=self._add_to_template, style='CreateTemplateActiveAddBtn.TButton')

    def _grid_widgets(self):
        self.search_name_lbl.grid(row=0, column=0, columnspan=2, padx=(0, 10), pady=(0, 10))
        self.search_name_e.grid(row=1, column=0, columnspan=2, padx=(0, 10), pady=(0, 30))

        self.vertical_separator.grid(row=0, column=2, rowspan=5, sticky='ns')

        self.tally_results_lbl.grid(row=0, column=3, columnspan=2, padx=(80, 0), pady=(0, 20))
        self.food_results_lbox.grid(row=1, column=3, columnspan=2, padx=(80, 0), pady=(0, 30), sticky='we')
        self.food_results_scrolly.grid(row=1, column=4, sticky='ens', pady=(0, 30))

        self.horizontal_separator.grid(row=2, column=0, columnspan=6, sticky='we')

        self.food_name_lbl.grid(row=3, column=0, columnspan=2, padx=(0, 10), pady=(100, 20))
        self.food_name_e.grid(row=4, column=0, columnspan=2, padx=(0, 10), pady=(0, 50))

        self.food_weight_lbl.grid(row=3, column=3, columnspan=2, padx=(80, 0), pady=(100, 20))
        self.food_weight_e.grid(row=4, column=3, columnspan=2, padx=(80, 0), pady=(0, 50))

        self.add_template_btn.grid(row=5, column=0, columnspan=5, pady=(10, 0))
    
    def _bind_events(self):
        self.food_results_lbox.bind('<<ListboxSelect>>', lambda _: self._set_food_name())
        self.food_weight_e.bind('<KeyRelease>', lambda _: self._handle_food_weight_keyreleased())
        self.frame.bind('<Button-4>', lambda _: self.scroll_up_handler())
        self.frame.bind('<Button-5>', lambda _: self.scroll_down_handler())
        self.search_name_e.bind('<Return>', lambda _: self._search_by_name())
        self.search_name_e.bind('<KeyRelease>', lambda _: self._search_by_name_on_release())

    def _validate_food_weight_input(self, entry_value):
        if entry_value and self.food_weight_re.match(entry_value) is None:
            return False
        return True

    def _set_food_name(self):
        if not self.food_results_lbox.curselection():
            # NOTE: some weird error which I didn't debug yet
            return
        idx, = self.food_results_lbox.curselection()
        self.food_name_var.set(self.food_results_lbox_values[idx])

        # check if necessary conditions are satisifed
        if self.food_weight_var.get():
            self.add_template_btn.state(['!disabled'])
            self.add_template_btn['cursor'] = 'hand2'
        else:
            self.add_template_btn.state(['disabled'])
            self.add_template_btn['cursor'] = ''

    def _handle_food_weight_keyreleased(self):
        # check if necessary conditions are satisifed
        if self.food_weight_var.get() and self.food_name_var.get():
            self.add_template_btn.state(['!disabled'])
            self.add_template_btn['cursor'] = 'hand2'
        else:
            self.add_template_btn.state(['disabled'])
            self.add_template_btn['cursor'] = ''

    def _add_to_template(self):
        food_name = self.food_name_var.get()
        food_weight = int(self.food_weight_var.get())
        self.parent.add_to_template(food_name, food_weight)

    def _sort_results(self):
        pass
        # sort_option = self.selected_sort_option_var.get()
        # if sort_option:
        #     sort_direction = self.sort_option_direction_var.get()
        #     rev = True if sort_direction == 'desc' else False
        #     self.parent.sort_results(sort_option, rev)

    def _search_by_name(self):
        food_name = self.search_name_e_var.get().strip()
        if not food_name:
            self.update_food_label_names(self.all_food_names, parent_call=False)
        food_name = food_name.lower()
        food_names = [fn for fn in self.all_food_names if food_name in fn.lower()]
        self.update_food_label_names(food_names, parent_call=False)

    def _search_by_name_on_release(self):
        press_time = datetime.now()
        if press_time - self.last_pressed_button < self.last_pressed_button_interval:
            self.last_pressed_button = press_time
            return
        self.last_pressed_button = press_time
        self._search_by_name()

    def _update_tally_cnt(self):
        cnt = len(self.food_results_lbox_values)
        cnt_s = str(cnt).zfill(2)
        text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        self.tally_results_var.set(f'{cnt} {text}')

    def _color_listbox_foods(self):
        for i in range(len(self.food_results_lbox_values)):
            clr = 'white' if i % 2 == 0 else '#f7d4ec'
            self.food_results_lbox.itemconfigure(i, background=clr)

    def grid_frame(self, row, column, sticky):
        self.frame.grid(row=row, column=column, sticky=sticky, padx=(300), pady=(0, 20))
    
    def configure_style(self, style_name):
        self.frame.configure(style=style_name)
    
    def set_scroll_up_handler(self, callback):
        self.scroll_up_handler = callback
    
    def set_scroll_down_handler(self, callback):
        self.scroll_down_handler = callback

    def update_food_label_names(self, food_names, parent_call=True):
        # TODO: make this work properly; ie. justify the text by center
        # self.food_results_lbox_values = [x.rjust((60 - len(x)) // 2) for x in food_names]

        # `self.all_food_names` is only changed by parent frame, it is a superset for `self.food_results_lbox_values`
        if parent_call:
            self.all_food_names = food_names
            # clear all entry values
            for v in (self.search_name_e_var, self.food_name_var, self.food_weight_var):
                v.set('')
        self.food_results_lbox_values = food_names
        self.food_results_lbox_var.set(self.food_results_lbox_values)
        self._update_tally_cnt()
        self._color_listbox_foods()


class TemplateActionsFrame:
    """Frame for rendering action options of a new meal template."""

    def __init__(self, parent):
        self.parent = parent

        self.frame = ttk.Frame(parent.frame, style='CreateTemplate.TFrame')

        self._create_mutual_button_options()
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.frame,
            'state': 'disabled',
            'style': 'CreateTemplateActiveAddBtn.TButton',
        }

    def _create_styles(self):
        ...

    def _create_widget_vars(self):
        ...

    def _create_widgets(self):
        self.save_template_btn = ttk.Button(text='Trajno pohrani predložak', command=lambda: ..., **self.mutual_button_options)
        self.clean_template_btn = ttk.Button(text='Očisti predložak', command=self.parent.clean_template, **self.mutual_button_options)

    def _grid_widgets(self):
        self.save_template_btn.grid(row=0, column=0, padx=(10, 20))
        self.clean_template_btn.grid(row=0, column=1)

    def _bind_events(self):
        ...

    def grid_frame(self, row, column, sticky):
        self.frame.grid(row=row, column=column, sticky=sticky, padx=0, pady=(0, 10))

    def enable_buttons(self):
        self.save_template_btn.state(['!disabled'])
        self.save_template_btn['cursor'] = 'hand2'
        self.clean_template_btn.state(['!disabled'])
        self.clean_template_btn['cursor'] = 'hand2'

    def disable_buttons(self):
        self.save_template_btn.state(['disabled'])
        self.save_template_btn['cursor'] = ''
        self.clean_template_btn.state(['disabled'])
        self.clean_template_btn['cursor'] = ''


class CreateMealTemplateFrame:
    """Frame representing UI and its logic for creating a new meal template."""

    def __init__(self, parent, db):
        self.db = db
        self.parent = parent
        self.template_foods = []
        self.tally_row = None

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

    def _create_widgets(self):
        self.topic_lbl = ttk.Label(self.frame, text=self.topic_lbl_text, style='CreateTemplateTopic.TLabel')
        
        self.create_meal_options_frame = CreateTemplateOptionsFrame(self, self.db)
        self.create_meal_options_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.create_meal_options_frame.set_scroll_down_handler(self.parent.handle_scroll_down)

        self.template_action_frame = TemplateActionsFrame(self)

        # define table headers without `consumed` timestamp
        table_headers = list(consumed_food_headers.values())[:consumed_food_map['created_on']]
        self.template_food_table_frame = FoodTableResultsFrame(self, table_headers)
        self.template_food_table_frame.configure_style('CreateTemplate.TFrame')
        self.template_food_table_frame.set_row_callback(self._open_update_center)
        self.template_food_table_frame.set_scroll_up_handler(self.parent.handle_scroll_up)
        self.template_food_table_frame.set_scroll_down_handler(self.parent.handle_scroll_down)

    def _grid_widgets(self):
        self.topic_lbl.grid(row=0, column=0, sticky='we', padx=(15, 30), pady=(50, 30))
        self.create_meal_options_frame.grid_frame(row=1, column=0, sticky='we')
        self.template_action_frame.grid_frame(row=2, column=0, sticky='w')
        self.template_food_table_frame.grid_frame(row=3, column=0, sticky='we')

    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.parent.handle_scroll_up())
        self.frame.bind('<Button-5>', lambda _: self.parent.handle_scroll_down())

    def add_to_template(self, food_name, food_weight):
        """Add rescaled food item to the template and render it.

        If food name already present in the template, raise an error.
        """
        name_id = consumed_food_map['food_name']
        # two same names can't co exist in a template -> I'm too lazy to merge them together
        if food_name in {f[name_id] for f in self.template_foods}:
            messagebox.showerror(title='Duplicirano ime artikla',
                                 message=f'`{food_name}` već postoji u predlošku!')
            return

        # enable `save template` button
        if not self.template_foods:
            self.template_action_frame.enable_buttons()

        # scale and update internal state
        scaled_row = self._rescale_food_values(food_name, food_weight)
        self.tally_row = self._calculate_tally_row(scaled_row)
        scaled_row = [len(self.template_foods) + 1, food_name] + scaled_row
        self.template_foods.append(scaled_row)

        # rendering
        self.template_food_table_frame.destroy_tally_row()
        self.template_food_table_frame.render_result(scaled_row)
        self.template_food_table_frame.render_tally_row(self.tally_row)

    def _rescale_food_values(self, food_name, food_weight):
        scale_factor = round(food_weight / NORMATIVE, 2)

        # fetch the food table and scale the corresponding columns
        food_table = self.db.get_food_item_table(food_name)
        food_table = food_table[nutrition_table_map['calories']:nutrition_table_map['price'] + 1]
        food_table = [round(x * scale_factor, 2) for x in food_table]
        # cast to int wherever it makes sense to
        food_table = [int(x) if int(x) == x else x for x in food_table]

        return [food_weight] + food_table

    def _calculate_tally_row(self, new_row):
        if self.tally_row is None:
            return ['\u2211', 'Ukupno'] + new_row
        else:
            tr = self.tally_row[consumed_food_map['food_weight']:consumed_food_map['price'] + 1]
            tr = [round(tr_d + nr_d, 2) for tr_d, nr_d in zip(tr, new_row)]
            # cast to int wherever it makes sense to
            tr = [int(x) if int(x) == x else x for x in tr]
            return ['\u2211', 'Ukupno'] + tr

    def clean_template(self):
        """Delete all data from the template"""

        self.template_food_table_frame.destroy_rows()
        self.template_food_table_frame.destroy_tally_row()
        self.template_foods = []
        self.tally_row = None

        self.template_action_frame.disable_buttons()

    def search_foods(self, start_time, end_time, food_name):
        """Search food by start time and optionally by end time and food name

        After filtering is done, update the total number of results, delete old
        and render new results.
        """
        pass
        # self.consumed_foods = self.db.get_consumed_food_on_date(start_time, end_time)
        # if food_name:
        #     food_name = food_name.lower()
        #     self.consumed_foods = [f for f in self.consumed_foods if food_name in f[1].lower()]

        # # update the number of results label
        # cnt = len(self.consumed_foods)
        # cnt_s = str(cnt).zfill(2)
        # text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        # self.consumed_food_tally_lbl_var.set(f'{cnt} {text}')

        # self.tally_row = self._calculate_tally_row(start_time, end_time)
        # # uncolor the sorting column since it was present for the old results
        # self.template_food_table_frame.unmark_column()
        # # Clear all rendered rows
        # self.template_food_table_frame.destroy_rows()
        # # re-render them with the updated list of food tables
        # self.template_food_table_frame.render_results(self.consumed_foods)
        # # render the tally row
        # self.template_food_table_frame.render_tally_row(self.tally_row)

        # # since there are 2 search operation, save the last one used by a user
        # self.last_search_operation = self.create_meal_options_frame._search_foods

    def _calculate_tally_row1(self, start_time, end_time):
        """Return the sum of all rows or None if no rows present"""
        pass
        
        # if not self.consumed_foods:
        #     return None
        # tally_time = f"{f'{start_time.day}'.zfill(2)}-{f'{start_time.month}'.zfill(2)}-{start_time.year}"
        # if end_time:
        #     tally_time = tally_time + '  <-->  ' + f"{f'{end_time.day}'.zfill(2)}-{f'{end_time.month}'.zfill(2)}-{end_time.year}"
        # sorting_idx = list(consumed_food_map.values())[2:-1]
        # tally_row = [sum([row[i] for row in self.consumed_foods]) for i in sorting_idx]
        # tally_row = [int(i) if int(i) == round(i, 2) else round(i, 2) for i in tally_row]
        # tally_row  = ['\u2211', 'Ukupno'] + tally_row + [tally_time]
        # return tally_row

    def sort_results(self, sort_option, rev):
        """Sort current results by `sort_option` and reverse the results if `rev=True`"""

        # Find the corresponding index from the centralized back-patching defintion
        pass
        
        # for k, v in consumed_food_headers.items():
        #     if v == sort_option:
        #         idx = consumed_food_map[k]
        #         break
        # self.template_food_table_frame.mark_column(idx)
        # if idx == consumed_food_map['food_name']:
        #     # sort by name works based on ASCII -> compare with case insensitivity
        #     self.consumed_foods.sort(key=lambda row: row[idx].lower(), reverse=rev)
        # elif idx == consumed_food_map['created_on']:
        #     # sort by datetime instances instead of strings representing datetime stamp
        #     self.consumed_foods.sort(key=lambda row: datetime.strptime(row[idx], '%d-%m-%Y, %H:%M'), reverse=rev)
        # else:
        #     self.consumed_foods.sort(key=lambda row: row[idx], reverse=rev)
        # # Clear all rendered rows
        # self.template_food_table_frame.destroy_rows()
        # # re-render them with the sorted list of food tables
        # self.template_food_table_frame.render_results(self.consumed_foods)
        # # render the tally row
        # self.template_food_table_frame.render_tally_row(self.tally_row)

    def search_by_name(self, food_name):
        """Search all consumed foods based only on the given name

        The filtering is based ond the `in` operator and case sensitivity is ignored.
        """
        pass
        # consumed_food_names = self.db.get_all_consumed_food_names()
        # # if food_name is empty return all results, otherwise do the filtering
        # if food_name:
        #     food_name = food_name.lower()
        #     consumed_food_names = [fn for fn in consumed_food_names if food_name in fn.lower()]
        # self.consumed_foods = [fr
        #                        for fn in consumed_food_names
        #                        for fr in self.db.get_consumed_foods_by_name(fn)]

        # # update the number of results label
        # cnt = len(self.consumed_foods)
        # cnt_s = str(cnt).zfill(2)
        # text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        # self.consumed_food_tally_lbl_var.set(f'{cnt} {text}')

        # # calculate earliest and latest timestamps
        # min_t, max_t = self._get_edge_timestamps()

        # self.tally_row = self._calculate_tally_row(min_t, max_t)
        # # uncolor the sorting column since it was present for the old results
        # self.template_food_table_frame.unmark_column()
        # # Clear all rendered rows
        # self.template_food_table_frame.destroy_rows()
        # # re-render them with the updated list of food tables
        # self.template_food_table_frame.render_results(self.consumed_foods)
        # # render the tally row
        # self.template_food_table_frame.render_tally_row(self.tally_row)

        # # since there are 2 search operation, save the last one used by a user
        # self.last_search_operation = self.create_meal_options_frame._search_by_name

    def _get_edge_timestamps(self):
        """Return earliest and latest from consumed food results

        # NOTE: not the best design, but I'll live with it -> I had to adhere to `_calculate_tally_row` API
        If timestamps is empty return dummy values(datetime.now()).
        If earliest and latest timestamps are the same return only one and None
        Otherwise return both of them.
        """
        pass
        # time_idx = consumed_food_map['created_on']
        # timestamps = [cf[time_idx] for cf in self.consumed_foods]
        # if not timestamps:
        #     return datetime.now(), datetime.now()
        # min_t, max_t = min(timestamps), max(timestamps)
        # start_time = datetime.strptime(min_t, '%d-%m-%Y, %H:%M')
        # end_time = datetime.strptime(max_t, '%d-%m-%Y, %H:%M')
        # if start_time == end_time:
        #     return start_time, None
        # return start_time, end_time

    def _open_update_center(self, p_key):
        pass
        # Fetch the complete table row since consumed food name is not globally unique
        # consumed_food_row = self.db.get_consumed_food_by_primary_key(p_key)
        # DialogPickerTopLevel(self, self.db, consumed_food_row)

    def update_food_label_names(self):
        self.all_food_names = self.db.all_food_label_names
        self.create_meal_options_frame.update_food_label_names(self.all_food_names)
