from tkinter import ttk


class SuccessfulLabelCreationFrame:
    """Leaf Frame
    
    Shows info when a new food label table was successfully created.
    """

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent, padding=(10), borderwidth=2, relief='ridge', style='Success.TFrame')
        
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _create_styles(self):
        ttk.Style().configure('Success.TFrame', background='#8d9f66')
    
    def _create_widget_vars(self):
        self.ok_text = 'Ok'
        self.message_text = 'Uspješno kreirana nova nutritivna tablica u Ranahu.'
    
    def _create_widgets(self):
        self.ok_button = ttk.Button(self.frame, text=self.ok_text, command=self._remove_widgets)
        self.message_lbl = ttk.Label(self.frame, text=self.message_text)
    
    def _grid_widgets(self):
        self.message_lbl.grid(row=0, column=0, pady=15, padx=5)
        self.ok_button.grid(row=1, column=0, pady=15, padx=5)
    
    def _remove_widgets(self):
        """Remove this frame from its parent mapping"""
        self.frame.grid_forget()


# NOTE: root is not scrollable, either way I'll leave this type present
class ScrollBarWidget:
    """Scroll bar type"""

    def __init__(self, parent, orient='vertical'):
        """Create new scroll-bar and hook it to the parent in appropriate orientation"""
        
        self.scroll_bar = ttk.Scrollbar(parent, orient=orient)
        if orient == 'horizontal':
            parent.configure(xscrollcommand=self.scroll_bar.set)
            command = parent.xview
        else:
            parent.configure(yscrollcommand=self.scroll_bar.set)
            command = parent.yview
        self.scroll_bar.configure(command=command)
        self._grid()
    
    def _grid(self):
        self.scroll_bar.grid(row=0, column=1, sticky='ns')
