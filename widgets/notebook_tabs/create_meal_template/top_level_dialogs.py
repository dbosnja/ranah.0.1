from tkinter import ttk, Toplevel, messagebox, StringVar


class SaveTemplateCenterTopLevel:
    """Description"""

    def __init__(self, parent, save_callback):
        self.parent = parent
        self.save_callback = save_callback

        self._initialize_dialog_window()

        self._create_mutual_button_options()
        self._create_mutual_label_options()
        self._create_mutual_entry_options()

        # its children
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Trajno pohrani predložak objeda')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x200+2600+400')
        self.dialog_center.minsize(600, 200)
        for col in range(2):
            self.dialog_center.columnconfigure(col, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())

    def _create_styles(self):
        self.save_btn_style = ttk.Style()
        self.save_btn_style.configure('SaveMealTemplate.TButton', font=(25), padding=(0, 5, 0, 5))
        self.save_btn_style.map('SaveMealTemplate.TButton', background=[('active', '#00994D')])

        self.cancel_btn_style = ttk.Style()
        self.cancel_btn_style.configure('CancelMealTemplate.TButton', font=(25), padding=(0, 5, 0, 5))
        self.cancel_btn_style.map('CancelMealTemplate.TButton', background=[('active', '#FF0000')])

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.dialog_center,
            'cursor': 'hand2',
        }

    def _create_mutual_label_options(self):
        self.mutual_label_options = {
            'master': self.dialog_center,
            'anchor': 'center',
            'borderwidth': 2,
            'relief': 'groove',
            'padding': 10,
            'font': 'default 15',
            'justify': 'center',
        }

    def _create_mutual_entry_options(self):
        self.mutual_entry_options = {
            'master': self.dialog_center,
            'width': 30,
            'font': 'normal 17',
            'justify': 'center',
        }

    def _create_widget_vars(self):
        self.title_lbl_var = 'Unesite naziv za budući predložak objeda'
        self.template_name_e_var = StringVar()

    def _create_widgets(self):
        self.title_lbl = ttk.Label(text=self.title_lbl_var, background='#FFFFCC', **self.mutual_label_options)

        self.template_name_e = ttk.Entry(textvariable=self.template_name_e_var, **self.mutual_entry_options)

        self.create_template_btn = ttk.Button(self.dialog_center, text='Spremi', command=self.save_callback,
                                              style='SaveMealTemplate.TButton', state='disabled')
        self.cancel_btn = ttk.Button(text='Odustani', command=self.dialog_center.destroy, style='CancelMealTemplate.TButton', **self.mutual_button_options)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, columnspan=2, sticky='we')
        self.template_name_e.grid(row=1, column=0, columnspan=2, sticky='we', pady=(10, 5))
        self.create_template_btn.grid(row=2, column=0, sticky='e', padx=(0, 10), pady=(30, 0))
        self.cancel_btn.grid(row=2, column=1, sticky='w', padx=(10, 0), pady=(30, 0))

    def _bind_events(self):
        self.template_name_e.bind('<KeyRelease>', lambda _: self._handle_template_name())

    def _handle_template_name(self):
        if self.template_name_e_var.get():
            self.create_template_btn['state'] = 'active'
            self.create_template_btn['cursor'] = 'hand2'
        else:
            self.create_template_btn['state'] = 'disabled'
            self.create_template_btn['cursor'] = ''

