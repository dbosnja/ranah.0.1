from tkinter import ttk, StringVar, Listbox, font

from .. .. utility_widgets.leaf_frames import ScrollBarWidget


class SearchOptionsFrame:
    """Frame which is in charge of searching through meal templates with UI and reactive logic."""

    def __init__(self, parent):
        self.parent = parent
        self.all_meal_template_names = []

        self.frame = ttk.Frame(parent.frame, style='SearchMealTemplates.TFrame', padding=(0, 20, 0, 0))
        # enable resizing
        for col in range(3):
            self.frame.columnconfigure(col, weight=1)

        self._create_mutual_label_options()
        self._create_mutual_entry_options()
        self._create_mutual_button_options()

        self._create_fonts()
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

    def _create_fonts(self):
        self.lbox_items_font = font.Font(family='Chilanka', size=15)

    def _create_styles(self):
        ttk.Style().configure('SearchMealLabels.TLabel', background='#BFBFBF')
    
    def _create_widget_vars(self):
        self.search_e_var = StringVar()
        self.tally_cnt_var = StringVar()
        self.tmplt_results_lbox_values = []
        self.tmplt_results_lbox_var = StringVar(value=self.tmplt_results_lbox_values)
        self.selected_tmplt_name_var = StringVar()
    
    def _create_widgets(self):
        self.search_lbl = ttk.Label(text='Pretraži predložak', **self.mutual_label_options)
        self.search_e = ttk.Entry(textvariable=self.search_e_var, **self.mutual_entry_options)
        self.tally_cnt_lbl = ttk.Label(textvariable=self.tally_cnt_var, **self.mutual_label_options)
        self.tmplt_results_lbox = Listbox(self.frame, listvariable=self.tmplt_results_lbox_var, cursor='hand2', height=5)
        self.tmplt_results_lbox.configure(font=self.lbox_items_font)
        self.tmplt_lbox_scrolly = ScrollBarWidget(self.frame)
        self.tmplt_lbox_scrolly.attach_to_scrollable(self.tmplt_results_lbox)
        self.selected_tmplt_name_e = ttk.Entry(textvariable=self.selected_tmplt_name_var, state='readonly', **self.mutual_entry_options)

        self.render_ingredients_btn = ttk.Button(text='Pregledaj sastojke predloška', state='disabled',
                                                 command=self._render_ingredients, **self.mutual_button_options)
        self.render_template_btn = ttk.Button(text='Pregledaj predloške', cursor='hand2',
                                              command=self._render_templates, **self.mutual_button_options)

    def _grid_widgets(self):
        self.search_lbl.grid(row=0, column=1, pady=(0, 10))
        self.search_e.grid(row=1, column=1, pady=(0, 10), sticky='ew')
        self.tally_cnt_lbl.grid(row=2, column=1, pady=(0, 10))
        self.tmplt_results_lbox.grid(row=3, column=1, pady=(0, 10), sticky='ew')
        self.tmplt_lbox_scrolly.grid(row=3, column=2, sticky='wns', pady=(0, 10))
        self.selected_tmplt_name_e.grid(row=4, column=1, sticky='ew', pady=(20, 0))

        self.render_ingredients_btn.grid(row=4, column=0, sticky='e', padx=(0, 20), pady=(20, 0))
        self.render_template_btn.grid(row=4, column=2, sticky='w', padx=(20, 0), pady=(20, 0))

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

    def _create_mutual_entry_options(self):
        self.mutual_entry_options = {
            'master': self.frame,
            'width': 30,
            'font': 'default 15',
            'justify': 'center',
        }

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.frame,
            'style': 'CreateTemplateActiveAddBtn.TButton',
        }
    
    def _bind_events(self):
        self.tmplt_results_lbox.bind('<<ListboxSelect>>', lambda _: self._set_selected_template_name())
        self.search_e.bind('<KeyRelease>', lambda _: self._filter_template_names())
        self.frame.bind('<Button-4>', self.mouse_wheel_event_handler)
        self.frame.bind('<Button-5>', self.mouse_wheel_event_handler)

    def _filter_template_names(self):
        name = self.search_e_var.get().strip()
        if not name:
            self.tmplt_results_lbox_values = [n for n in self.all_meal_template_names]
        else:
            name = name.lower()
            self.tmplt_results_lbox_values = [n for n in self.all_meal_template_names if name in n.lower()]
        self.tmplt_results_lbox_var.set(self.tmplt_results_lbox_values)

        if self.tmplt_results_lbox_values:
            self.enable_render_template_btn()
        else:
            self.disable_render_template_btn()

        self._rerender_templates_count()
        self._recolor_lbox_values()

    def _rerender_template_names(self):
        self.tmplt_results_lbox_values = [n for n in self.all_meal_template_names]
        self.tmplt_results_lbox_var.set(value=self.tmplt_results_lbox_values)

        self._rerender_templates_count()
        self._recolor_lbox_values()

        # clean entry values
        self.search_e_var.set('')
        self.selected_tmplt_name_var.set('')
        self.disable_render_ingredients_btn()
        if self.tmplt_results_lbox_values:
            self.enable_render_template_btn()
        else:
            self.disable_render_template_btn()
    
    def _rerender_templates_count(self):
        cnt = len(self.tmplt_results_lbox_values)
        cnt_s = str(cnt).zfill(2)
        text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        self.tally_cnt_var.set(f'{cnt} {text}')

    def _recolor_lbox_values(self):
        for i in range(len(self.tmplt_results_lbox_values)):
            clr = 'white' if i % 2 == 0 else '#f7d4ec'
            self.tmplt_results_lbox.itemconfigure(i, background=clr)

    def _set_selected_template_name(self):
        if not self.tmplt_results_lbox.curselection():
            # NOTE: some weird error which I didn't debug yet
            return
        idx, = self.tmplt_results_lbox.curselection()
        self.selected_tmplt_name_var.set(self.tmplt_results_lbox_values[idx])
        self.enable_render_ingredients_btn()

    def _render_ingredients(self):
        template_name = self.selected_tmplt_name_var.get()
        self.parent.render_ingredients(template_name)

    def _render_templates(self):
        template_names = self.tmplt_results_lbox_values
        self.parent.render_templates(template_names)

    def grid(self, row, column, sticky='we'):
        self.frame.grid(row=row, column=column, sticky=sticky)

    def set_meal_template_names(self, tmplt_names):
        self.all_meal_template_names = tmplt_names
        self._rerender_template_names()

    def enable_render_ingredients_btn(self):
        self.render_ingredients_btn['state'] = ''
        self.render_ingredients_btn['cursor'] = 'hand2'

    def disable_render_ingredients_btn(self):
        self.render_ingredients_btn['state'] = 'disabled'
        self.render_ingredients_btn['cursor'] = ''

    def enable_render_template_btn(self):
        self.render_template_btn['state'] = ''
        self.render_template_btn['cursor'] = 'hand2'

    def disable_render_template_btn(self):
        self.render_template_btn['state'] = 'disabled'
        self.render_template_btn['cursor'] = ''

    def mouse_wheel_event_handler(self, event):
        self.parent.mouse_wheel_event_handler(event)

