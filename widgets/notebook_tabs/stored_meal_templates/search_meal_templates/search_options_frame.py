from tkinter import ttk, StringVar, Listbox

from .. .. utility_widgets.leaf_frames import ScrollBarWidget


class SearchOptionsFrame:
    """Description"""

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db  # NOTE: not sure if this one needs the database operand

        self.frame = ttk.Frame(parent.frame, style='SearchMealTemplates.TFrame', padding=(0, 20, 0, 0))
        # enable resizing - TODO: or more
        for col in range(3):
            self.frame.columnconfigure(col, weight=1)

        self._create_mutual_label_options()
        self._create_mutual_entry_options()
        self._create_mutual_button_options()

        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

    def _create_styles(self):
        ttk.Style().configure('SearchMealLabels.TLabel', background='#BFBFBF')
    
    def _create_widget_vars(self):
        self.search_e_var = StringVar()
        self.tally_cnt_var = StringVar(value='n rezultata')
        self.tmplt_results_lbox_values = []
        self.tmplt_results_lbox_var = StringVar(value=self.tmplt_results_lbox_values)
        self.selected_tmplt_name_var = StringVar()
    
    def _create_widgets(self):
        self.search_lbl = ttk.Label(text='Pretraži predložak', **self.mutual_label_options)
        self.search_e = ttk.Entry(textvariable=self.search_e_var, **self.mutual_entry_options)
        self.tally_cnt_lbl = ttk.Label(textvariable=self.tally_cnt_var, **self.mutual_label_options)
        self.tmplt_results_lbox = Listbox(self.frame, listvariable=self.tmplt_results_lbox_var, cursor='hand2')
        self.tmplt_lbox_scrolly = ScrollBarWidget(self.frame)
        self.tmplt_lbox_scrolly.attach_to_scrollable(self.tmplt_results_lbox)
        self.selected_tmplt_name_e = ttk.Entry(textvariable=self.selected_tmplt_name_var, state='readonly', **self.mutual_entry_options)

        self.render_ingredients_btn = ttk.Button(text='Pregledaj sastojke predloška', state='disabled', **self.mutual_button_options)
        self.render_template_btn = ttk.Button(text='Pregledaj predložak', cursor='hand2', **self.mutual_button_options)

    def _grid_widgets(self):
        self.search_lbl.grid(row=0, column=1, pady=(0, 10))
        self.search_e.grid(row=1, column=1, pady=(0, 10))
        self.tally_cnt_lbl.grid(row=2, column=1, pady=(0, 10))
        self.tmplt_results_lbox.grid(row=3, column=1, pady=(0, 10))
        self.tmplt_lbox_scrolly.grid(row=3, column=1, sticky='ens', pady=(0, 10))
        self.selected_tmplt_name_e.grid(row=4, column=1)

        self.render_ingredients_btn.grid(row=4, column=0)
        self.render_template_btn.grid(row=4, column=2)

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
        }

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.frame,
            'style': 'CreateTemplateActiveAddBtn.TButton',
        }
    
    def _bind_events(self):
        ...
    
    def grid(self, row, column, sticky='we'):
        self.frame.grid(row=row, column=column, sticky=sticky)
