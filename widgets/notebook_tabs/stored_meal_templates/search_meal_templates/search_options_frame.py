from tkinter import ttk, StringVar, Listbox

from .. .. utility_widgets.leaf_frames import ScrollBarWidget


class SearchOptionsFrame:
    """Description"""

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db  # NOTE: not sure if this one needs the database operand

        self.frame = ttk.Frame(parent.frame, style='SearchMealTemplates.TFrame')
        # enable resizing - TODO: or more
        for col in range(3):
            self.frame.columnconfigure(col, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_widget_vars(self):
        self.search_e_var = StringVar()
        self.tally_cnt_var = StringVar(value='n rezultata')
        self.tmplt_results_lbox_values = []
        self.tmplt_results_lbox_var = StringVar(value=self.tmplt_results_lbox_values)
        self.selected_tmplt_name_var = StringVar()
    
    def _create_widgets(self):
        self.search_lbl = ttk.Label(self.frame, text='Pretraži predložak', anchor='center')
        self.search_e = ttk.Entry(self.frame)
        self.tally_cnt_lbl = ttk.Label(self.frame, textvariable=self.tally_cnt_var, anchor='center')
        self.tmplt_results_lbox = Listbox(self.frame, listvariable=self.tmplt_results_lbox_var, cursor='hand2')
        self.tmplt_lbox_scrolly = ScrollBarWidget(self.frame)
        self.tmplt_lbox_scrolly.attach_to_scrollable(self.tmplt_results_lbox)
        self.selected_tmplt_name_e = ttk.Entry(self.frame, textvariable=self.selected_tmplt_name_var, state='readonly')

        self.render_ingredients_lbl = ttk.Label(self.frame, text='Pregledaj sastojke predloška', anchor='center')
        self.render_template_lbl = ttk.Label(self.frame, text='Pregledaj predložak', anchor='center')
    
    def _grid_widgets(self):
        self.search_lbl.grid(row=0, column=1)
        self.search_e.grid(row=1, column=1)
        self.tally_cnt_lbl.grid(row=2, column=1)
        self.tmplt_results_lbox.grid(row=3, column=1)
        self.tmplt_lbox_scrolly.grid(row=3, column=1, sticky='ens')
        self.selected_tmplt_name_e.grid(row=4, column=1)

        self.render_ingredients_lbl.grid(row=4, column=0)
        self.render_template_lbl.grid(row=5, column=2)
    
    def _bind_events(self):
        ...
    
    def grid(self, row, column, sticky='we'):
        self.frame.grid(row=row, column=column, sticky=sticky)
