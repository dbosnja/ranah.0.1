from tkinter import ttk, StringVar

from constants.constants import meal_templates_headers, meal_templates_headers_map


class SortOptionsFrame:
    """Frame which is in charge of sorting options for selected meal templates."""
    
    def __init__(self, parent):
        self.parent = parent

        self.frame = ttk.Frame(parent.frame, style='SearchMealTemplates.TFrame', padding=(10, 70, 0, 10))

        self._create_mutual_label_options()
        # self._create_mutual_entry_options()
        self._create_mutual_button_options()

        self._create_fonts()
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

    def _create_fonts(self):
        ...

    def _create_styles(self):
        ...

    def _create_widget_vars(self):
        self.tally_cnt_var = StringVar(value='0 rezultata')
        self.selected_sort_option_var = StringVar()
        
        st_idx = meal_templates_headers_map['food_name']
        self.sort_options_var = list(meal_templates_headers.values())[st_idx:]
        
        self.sort_option_direction_var = StringVar(value='asc')

    def _create_widgets(self):
        self.tally_cnt_lbl = ttk.Label(textvariable=self.tally_cnt_var, **self.mutual_label_options)
        self.clean_table_btn = ttk.Button(text='Očisti tablicu', command=self._clean_table, **self.mutual_button_options)
        self.sort_options_lbl = ttk.Label(text='Opcije sortiranja:', **self.mutual_label_options)
        self.sort_options_cbox = ttk.Combobox(self.frame, state='readonly', height=5, cursor='hand2',
                                              textvariable=self.selected_sort_option_var, values=self.sort_options_var)
        
        self.ascending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Uzlazno',
                                                          variable=self.sort_option_direction_var, value='asc', cursor='hand2')
        self.descending_sort_option_rbtn = ttk.Radiobutton(self.frame, text='Silazno',
                                                           variable=self.sort_option_direction_var, value='desc', cursor='hand2')
        
        self.sort_btn = ttk.Button(text='Sortiraj', command=self._sort_results, **self.mutual_button_options)

    def _grid_widgets(self):
        self.tally_cnt_lbl.grid(row=0, column=0, sticky='w', padx=(0, 20))
        self.clean_table_btn.grid(row=0, column=1, sticky='w', padx=(0, 100))
        self.sort_options_lbl.grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.sort_options_cbox.grid(row=0, column=3, sticky='w', padx=(0, 10))
        self.ascending_sort_option_rbtn.grid(row=0, column=4, sticky='w', padx=(0, 10))
        self.descending_sort_option_rbtn.grid(row=0, column=5, sticky='w', padx=(0, 20))
        self.sort_btn.grid(row=0, column=6, sticky='w')

    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.parent.handle_scroll_up())
        self.frame.bind('<Button-5>', lambda _: self.parent.handle_scroll_down())

    def _create_mutual_label_options(self):
        self.mutual_label_options = {
            'master': self.frame,
            'borderwidth': 2,
            'relief': 'ridge',
            'anchor': 'center',
            'padding': (10, 10, 10, 6),
            'font': '"URW Gothic" 12',
            'style': 'SearchMealLabels.TLabel',
        }

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.frame,
            'style': 'CreateTemplateActiveAddBtn.TButton',
            'state': 'disabled',
        }

    def _sort_results(self):
        sort_option = self.selected_sort_option_var.get()
        if sort_option:
            sort_direction = self.sort_option_direction_var.get()
            rev = True if sort_direction == 'desc' else False
            self.parent.sort_table(sort_option, rev)

    def _clean_table(self):
        self.parent.clean_table()

    def grid(self, row, column, sticky='we'):
        self.frame.grid(row=row, column=column, sticky=sticky)

    def enable_buttons(self):
        self.clean_table_btn['state'] = ''
        self.clean_table_btn['cursor'] = 'hand2'

        self.sort_btn['state'] = ''
        self.sort_btn['cursor'] = 'hand2'

    def disable_buttons(self):
        self.clean_table_btn['state'] = 'disabled'
        self.clean_table_btn['cursor'] = ''

        self.sort_btn['state'] = 'disabled'
        self.sort_btn['cursor'] = ''

    def rerender_templates_count(self, tmplt_cnt):
        cnt_s = str(tmplt_cnt).zfill(2)
        text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        self.tally_cnt_var.set(f'{tmplt_cnt} {text}')