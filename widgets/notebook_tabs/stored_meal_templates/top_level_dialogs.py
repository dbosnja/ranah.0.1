from tkinter import ttk, Toplevel, PhotoImage


class DeleteDialogTopLevel:
    """Description"""
    def __init__(self, parent, ingredient_name):
        self.parent = parent
        self.ingredient_name = ingredient_name

        self._initialize_dialog_window()

        # its children
        self._create_styles()
        self._create_mutual_button_options()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Trajno brisanje sastojka predloška')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x200+2500+500')
        self.dialog_center.minsize(500, 200)
        self.dialog_center.columnconfigure(0, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())

    def _create_styles(self):
        self.yes_btn_style = ttk.Style()
        self.yes_btn_style.configure('Yes.TButton', font=(25), padding=(0, 5, 0, 5))
        self.yes_btn_style.map('Yes.TButton', background=[('active', '#00994D')])

        self.no_btn_style = ttk.Style()
        self.no_btn_style.configure('No.TButton', font=(25), padding=(0, 5, 0, 5))
        self.no_btn_style.map('No.TButton', background=[('active', '#FF0000')])

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.dialog_center,
            'cursor': 'hand2',
        }

    def _create_widget_vars(self):
        self.title_lbl_var = f'Jeste li sigurni da želite trajno izbrisati sastojak\n`{self.ingredient_name}`?'

    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2,
                                   relief='groove', background='#FFFFCC', justify='center')

        self.yes_btn = ttk.Button(text='Da', style='Yes.TButton', command=self._delete_ingredient, **self.mutual_button_options)
        self.no_btn = ttk.Button(text='Ne', style='No.TButton', command=self.dialog_center.destroy, **self.mutual_button_options)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, sticky='we')

        self.yes_btn.grid(row=1, column=0, pady=(20, 20))
        self.no_btn.grid(row=2, column=0, pady=(0, 20))

    def _delete_ingredient(self):
        self.parent.delete_ingredient(self)


class DialogPickerTopLevel:
    """Description"""
    def __init__(self, parent, ingredient_name):
        self.parent = parent
        self.ingredient_name = ingredient_name

        self._initialize_dialog_window()

        self._create_mutual_style_options()
        self._create_mutual_button_options()

        # its children
        self._create_styles()
        self._create_images()        
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Centar akcija')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x400+2500+326')
        self.dialog_center.minsize(500, 500)
        self.dialog_center.columnconfigure(0, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())
    
    def _create_styles(self):
        self.add_btn_style = ttk.Style()
        self.add_btn_style.configure('Add.TButton', **self.mutual_style_options)
        
        self.update_btn_style = ttk.Style()
        self.update_btn_style.configure('Update.TButton', **self.mutual_style_options)

        self.delete_btn_style = ttk.Style()
        self.delete_btn_style.configure('Delete.TButton', **self.mutual_style_options)

        self.close_btn_style = ttk.Style()
        self.close_btn_style.configure('Close.TButton', **self.mutual_style_options)
    
    def _create_images(self):
        self.add_img = PhotoImage(file='./assets/images/add_icon.png')
        self.update_img = PhotoImage(file='./assets/images/update_icon.png')
        self.delete_img = PhotoImage(file='./assets/images/delete_icon.png')
        self.close_img = PhotoImage(file='./assets/images/close_icon.png')

    def _create_mutual_button_options(self):
        self.mutual_button_options = {
            'master': self.dialog_center,
            'compound': 'left',
            'cursor': 'hand2',
        }

    def _create_mutual_style_options(self):
        self.mutual_style_options = {
            'font': (25),
            'background': '#FFE6F1',
            'space': 15,
            'padding': (0, 5, 0, 5),
        }
    
    def _create_widget_vars(self):
        self.title_lbl_var = f'Odaberite što želite napraviti sa sastojkom\n`{self.ingredient_name}`'
    
    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2, relief='groove', background='#E57C2C', justify='center')
        
        self.add_btn = ttk.Button(text='Dodaj', image=self.add_img, style='Add.TButton',
                                  command=self._create_add_dialog, **self.mutual_button_options)
        self.update_btn = ttk.Button(text='Ažuriraj', image=self.update_img, style='Update.TButton',
                                     command=self._create_update_dialog, **self.mutual_button_options)
        self.delete_btn = ttk.Button(text='Izbriši', image=self.delete_img, style='Delete.TButton',
                                     command=self._create_delete_dialog, **self.mutual_button_options)
        self.close_btn = ttk.Button(text='Zatvori', image=self.close_img, style='Close.TButton',
                                    command=self.dialog_center.destroy, **self.mutual_button_options)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, sticky='we')
        
        self.add_btn.grid(row=1, column=0, pady=(50, 20))
        self.update_btn.grid(row=2, column=0, pady=(0, 20))
        self.delete_btn.grid(row=3, column=0, pady=(0, 20))
        self.close_btn.grid(row=4, column=0, pady=(0, 20))

    def _bind_events(self):
        pass

    def _create_delete_dialog(self):
        DeleteDialogTopLevel(self, self.ingredient_name)

    def _create_add_dialog(self):
        ...
    
    def _create_update_dialog(self):
        ...

    def delete_ingredient(self, delete_picker):
        self.parent.delete_ingredient(self, delete_picker)