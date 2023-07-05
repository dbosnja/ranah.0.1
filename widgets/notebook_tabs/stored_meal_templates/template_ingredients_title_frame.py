from tkinter import ttk


class TemplateIngredientsTitleFrame:
    """Frame for rendering title of the meal template ingredients frame."""

    def __init__(self, parent):
        self.parent = parent

        self._create_styles()
        
        self.frame = ttk.Frame(parent.frame, style='MainTitleFrame.TFrame', padding=(0, 20, 0, 0))
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('MainTitleFrame.TFrame', background='#FFD900')
    
    def _create_widget_vars(self):
        self.title_lbl_var = 'Pregled sastojaka predloška'
    
    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.frame, text=self.title_lbl_var, background='#FFD900', anchor='center', font='Purisa 17')
    
    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0)
    
    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.handle_scroll_up())
        self.frame.bind('<Button-5>', lambda _: self.handle_scroll_down())

    def grid(self, row, column, sticky='we'):
        self.frame.grid(row=row, column=column, sticky=sticky)

    def handle_scroll_up(self):
        self.parent.handle_scroll_up()

    def handle_scroll_down(self):
        self.parent.handle_scroll_down()

