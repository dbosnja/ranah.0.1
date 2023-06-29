from tkinter import ttk


class MainTitleFrame:
    """Frame for rendering the title of stored-meal-canvas

    Yes, it's not a generic one(thought of it too late) and it's tightly coupled
    (at least in its idea)
    """
    def __init__(self, parent):
        self.parent = parent

        self._create_styles()
        
        self.frame = ttk.Frame(parent.canvas, style='MainTitleFrame.TFrame', padding=(0, 25))
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('MainTitleFrame.TFrame', background='#ffd900')
    
    def _create_widget_vars(self):
        self.title_label_text = 'Pregledaj sve predloške objedâ'
    
    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.frame, text=self.title_label_text, background='#ffd900', font='Helvetica 25')
    
    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0)
    
    def _bind_events(self):
        ...