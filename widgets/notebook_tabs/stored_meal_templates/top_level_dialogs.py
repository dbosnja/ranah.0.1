import re

from tkinter import ttk, Toplevel, PhotoImage, StringVar, Listbox, font

from ...utility_widgets.leaf_frames import ScrollBarWidget


class AddIngredientFrame:
    """Frame for rendering the UI needed to add a new ingredient to the meal template"""

    def __init__(self, parent, all_food_names):
        self.parent = parent
        self.all_food_names = all_food_names

        self._create_fonts()
        self._create_styles()

        self.frame = ttk.Frame(parent.dialog_center, style='MainFrame.TFrame', padding=(40, 20, 40, 0))
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self._create_mutual_entry_options()
        self._create_mutual_label_options()

        self._define_regex()
        self._define_validations()

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

        self._render_templates_count()
        self._color_lbox_values()

    def _create_fonts(self):
        self.buttons_font = font.Font(family='Chilanka', size=16)

    def _create_styles(self):
        self.add_btn_style = ttk.Style()
        self.add_btn_style.configure('AddIngredientButton.TButton', font=self.buttons_font, padding=(0, 8, 0, 1))
        self.add_btn_style.map('AddIngredientButton.TButton', background=[('active', '#00994D')])

        self.cancel_btn_style = ttk.Style()
        self.cancel_btn_style.configure('CancelAddIngredientButton.TButton', font=self.buttons_font, padding=(0, 8, 0, 1))
        self.cancel_btn_style.map('CancelAddIngredientButton.TButton', background=[('active', '#FF0000')])

        ttk.Style().configure('MainFrame.TFrame', background='#E3E3E3')

    def _create_widget_vars(self):
        self.search_food_name_entry_var = StringVar()
        self.food_names_tally_cnt = StringVar()
        self.food_names_lbox_values = self.all_food_names
        self.food_names_lbox_var = StringVar(value=self.food_names_lbox_values)
        self.selected_food_name_var = StringVar()
        self.ingredient_weight_e_var = StringVar()

    def _create_widgets(self):
        self.search_food_name_e = ttk.Entry(textvariable=self.search_food_name_entry_var, **self.mutual_entry_options)
        self.search_food_name_e.focus()
        self.food_names_tally_cnt_lbl = ttk.Label(textvariable=self.food_names_tally_cnt, width=10, **self.mutual_label_options)
        self.food_names_lbox = Listbox(self.frame, listvariable=self.food_names_lbox_var, height=7, cursor='hand2')
        self.foods_lbox_scrolly = ScrollBarWidget(self.frame)
        self.foods_lbox_scrolly.attach_to_scrollable(self.food_names_lbox)
        self.selected_food_name_e = ttk.Entry(textvariable=self.selected_food_name_var, state='readonly', **self.mutual_entry_options)
        self.ingredient_weight_lbl = ttk.Label(text='Masa novog sastojka je', **self.mutual_label_options)
        self.ingredient_weight_e = ttk.Entry(textvariable=self.ingredient_weight_e_var, validate='key',
                                             validatecommand=self._validate_food_weight, **self.mutual_entry_options)
        self.add_btn = ttk.Button(self.frame, text='Dodaj', command=self._add_ingredient,
                                  state='disabled', style='AddIngredientButton.TButton')
        self.cancel_btn = ttk.Button(self.frame, text='Odustani', command=self._cancel,
                                     style='CancelAddIngredientButton.TButton', cursor='hand2')

    def _grid_widgets(self):
        self.search_food_name_e.grid(row=0, column=0, columnspan=3, sticky='we', pady=(0, 10))
        self.food_names_tally_cnt_lbl.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky='w')
        self.food_names_lbox.grid(row=2, column=0, columnspan=2, sticky='we', pady=(0, 10))
        self.foods_lbox_scrolly.grid(row=2, column=2, sticky='nse', pady=(0, 10))
        self.selected_food_name_e.grid(row=3, column=0, columnspan=3, sticky='we', pady=(0, 10))
        self.ingredient_weight_lbl.grid(row=4, column=0, columnspan=3, sticky='we', pady=(0, 10))
        self.ingredient_weight_e.grid(row=5, column=0, columnspan=3, pady=(0, 30))
        self.add_btn.grid(row=6, column=0, sticky='e', padx=(0, 10))
        self.cancel_btn.grid(row=6, column=1, sticky='w', padx=(10, 0))

    def _bind_events(self):
        self.food_names_lbox.bind('<<ListboxSelect>>', lambda _: self._set_selected_food_name())
        self.search_food_name_e.bind('<KeyRelease>', lambda _: self._filter_template_names())
        self.ingredient_weight_e.bind('<KeyRelease>', lambda _: self._handle_ingredient_weight_entry())

    def _create_mutual_entry_options(self):
        self.mutual_entry_options = {
            'master': self.frame,
            'width': 10,
            'font': 'normal 17',
            'justify': 'center',
        }

    def _create_mutual_label_options(self):
        self.mutual_label_options = {
            'master': self.frame,
            'anchor': 'center',
            'borderwidth': 2,
            'relief': 'groove',
            'padding': 5,
            'font': '15',
            'background': '#FFFFCC',
        }

    def _render_templates_count(self):
        cnt = len(self.food_names_lbox_values)
        cnt_s = str(cnt).zfill(2)
        text = 'rezultat' if cnt_s[-1] == '1' and cnt_s[-2] != '1' else 'rezultata'
        self.food_names_tally_cnt.set(f'{cnt} {text}')

    def _color_lbox_values(self):
        for i in range(len(self.food_names_lbox_values)):
            clr = 'white' if i % 2 == 0 else '#f7d4ec'
            self.food_names_lbox.itemconfigure(i, background=clr)

    def _filter_template_names(self):
        name = self.search_food_name_entry_var.get().strip()
        if not name:
            self.food_names_lbox_values = [n for n in self.all_food_names]
        else:
            name = name.lower()
            self.food_names_lbox_values = [n for n in self.all_food_names if name in n.lower()]
        self.food_names_lbox_var.set(self.food_names_lbox_values)

        self._render_templates_count()
        self._color_lbox_values()

    def _define_regex(self):
        self.food_weight_re = re.compile('^[1-9]{1}[0-9]{0,3}$')

    def _define_validations(self):
        self._validate_food_weight = self.frame.register(self._validate_food_weight_input), '%P'

    def _validate_food_weight_input(self, entry_value):
        if entry_value and self.food_weight_re.match(entry_value) is None:
                return False
        return True

    def _set_selected_food_name(self):
        if not self.food_names_lbox.curselection():
            return
        idx, = self.food_names_lbox.curselection()
        self.selected_food_name_var.set(self.food_names_lbox_values[idx])

        if self.ingredient_weight_e_var.get():
            self._enable_add_button()
        else:
            self._disable_add_button()

    def _handle_ingredient_weight_entry(self):
        if self.ingredient_weight_e_var.get() and self.selected_food_name_var.get():
            self._enable_add_button()
        else:
            self._disable_add_button()

    def _enable_add_button(self):
        self.add_btn['state'] = ''
        self.add_btn['cursor'] = 'hand2'

    def _disable_add_button(self):
        self.add_btn['state'] = 'disabled'
        self.add_btn['cursor'] = ''

    def _cancel(self):
        self.parent.destroy_dialog()

    def _add_ingredient(self):
        ingredient_name = self.selected_food_name_var.get()
        ingredient_weight = int(self.ingredient_weight_e_var.get())
        self.parent.add_ingredient(ingredient_name, ingredient_weight)

    def grid(self, row, column, sticky):
        self.frame.grid(row=row, column=column, sticky=sticky)


class AddDialogTopLevel:
    """Description"""

    def __init__(self, parent, template_name, all_food_names):
        self.parent = parent
        self.template_name = template_name
        self.all_food_names = all_food_names

        self._initialize_dialog_window()

        # its children
        self._create_styles()
        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()

    def _initialize_dialog_window(self):
        self.dialog_center = Toplevel()
        self.dialog_center.title('Dodaj novi sastojak u predložak')
        # Hardcoded values, but I'll live with it
        self.dialog_center.geometry(f'600x600+2500+300')
        self.dialog_center.minsize(600, 600)
        self.dialog_center.columnconfigure(0, weight=1)
        self.dialog_center.rowconfigure(1, weight=1)
        self.dialog_center.bind('<Escape>', lambda _: self.dialog_center.destroy())

    def _create_styles(self):
        ...

    def _create_widget_vars(self):
        self.title_lbl_var = f'Unesite naziv novog sastojka predloška\n`{self.template_name}`\ni njegovu masu u predlošku'

    def _create_widgets(self):
        self.title_lbl = ttk.Label(self.dialog_center, text=self.title_lbl_var,
                                   padding=10, font='15', anchor='center', borderwidth=2,
                                   relief='groove', background='#FFFFCC', justify='center')
        self.add_ingredient_frame = AddIngredientFrame(self, self.all_food_names)

    def _grid_widgets(self):
        self.title_lbl.grid(row=0, column=0, sticky='we')
        self.add_ingredient_frame.grid(row=1, column=0, sticky='news')

    def destroy_dialog(self):
        self.dialog_center.destroy()

    def add_ingredient(self, ingredient_name, ingredient_weight):
        self.parent.add_ingredient(self, ingredient_name, ingredient_weight)


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
        self.parent.open_add_dialog(self)
    
    def _create_update_dialog(self):
        ...

    def delete_ingredient(self, delete_picker):
        self.parent.delete_ingredient(self, delete_picker)

    def add_ingredient(self, add_picker, ingredient_name, ingredient_weight):
        self.parent.add_ingredient(self, add_picker, ingredient_name, ingredient_weight)

