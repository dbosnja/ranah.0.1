from tkinter import ttk, StringVar


class TemplateIngredientsTitleFrame:
    """Frame for rendering title of the meal template ingredients frame."""

    def __init__(self, parent):
        self.parent = parent
        self.prefix_title = 'Pregled sastojaka predloška'

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
        self.title_lbl_var = StringVar(value=self.prefix_title)
    
    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.frame, textvariable=self.title_lbl_var, background='#FFD900', anchor='center', font='Purisa 17')
    
    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0)
    
    def _bind_events(self):
        self.frame.bind('<Button-4>', self.mouse_wheel_event_handler)
        self.frame.bind('<Button-5>', self.mouse_wheel_event_handler)
        self.title_lbl.bind('<Button-4>', self.mouse_wheel_event_handler)
        self.title_lbl.bind('<Button-5>', self.mouse_wheel_event_handler)

    def grid(self, row, column, sticky='we'):
        self.frame.grid(row=row, column=column, sticky=sticky)

    def mouse_wheel_event_handler(self, event):
        self.parent.mouse_wheel_event_handler(event)

    def render_prefix_title(self):
        self.title_lbl_var.set(self.prefix_title)

    def render_full_title(self, template_name):
        self.title_lbl_var.set(f'{self.prefix_title} {template_name}')

