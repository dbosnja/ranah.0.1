from tkinter import ttk, DoubleVar, StringVar


class CreateFoodItemFrame:
    def __init__(self, parent, db):
        self.db = db
        self._create_styles()
        # main frame the `self` is composed of
        self.frame = ttk.Frame(parent, style='Main.TFrame', borderwidth=5, relief='raised')
        # create its children widgets
        self._create_widgets()
        self.frame.grid(column=0, row=0, sticky='wen', padx=10, pady=10)
        self.frame.columnconfigure(0, weight=1, minsize=50)
        self.frame.columnconfigure(1, weight=1, minsize=50)

    def _create_styles(self):
        ttk.Style().configure('Main.TFrame', background='#CCFFCC')

    def _create_widgets(self):
        topic_lbl = ttk.Label(self.frame, text='Nutritivne vrijednosti na 100 grama', anchor='center')
        topic_lbl.grid(row=0, column=0, pady=20, columnspan=2)

        calory_lbl = ttk.Label(self.frame, text='Kalorije', anchor='center', borderwidth=2, relief='groove', padding=(5))
        calory_lbl.grid(row=1, column=0)

        self.calory_var = DoubleVar()
        ttk.Entry(self.frame, textvariable=self.calory_var).grid(row=1, column=1, pady=10)

        fat_lbl = ttk.Label(self.frame, text='Masti', anchor='center', borderwidth=2, relief='groove', padding=(5))
        fat_lbl.grid(row=2, column=0)
        self.fat_var = DoubleVar()
        ttk.Entry(self.frame, textvariable=self.fat_var).grid(row=2, column=1, pady=10)

        saturated_fat_lbl = ttk.Label(self.frame, text='Zasićene masti', anchor='center', borderwidth=2, relief='groove', padding=(5))
        saturated_fat_lbl.grid(row=3, column=0)
        self.saturated_fat_var = DoubleVar()
        ttk.Entry(self.frame, textvariable=self.saturated_fat_var).grid(row=3, column=1, pady=10)

        carbs_lbl = ttk.Label(self.frame, text='Ugljikohidrati', anchor='center', borderwidth=2, relief='groove', padding=(5))
        carbs_lbl.grid(row=4, column=0)
        self.carbs_var = DoubleVar()
        ttk.Entry(self.frame, textvariable=self.carbs_var).grid(row=4, column=1, pady=10)

        sugar_lbl = ttk.Label(self.frame, text='Šećeri', anchor='center', borderwidth=2, relief='groove', padding=(5))
        sugar_lbl.grid(row=5, column=0)
        self.sugar_var = DoubleVar()
        ttk.Entry(self.frame, textvariable=self.sugar_var).grid(row=5, column=1, pady=10)

        proteins_lbl = ttk.Label(self.frame, text='Bjelančevine', anchor='center', borderwidth=2, relief='groove', padding=(5))
        proteins_lbl.grid(row=6, column=0)
        self.proteins_var = DoubleVar()
        ttk.Entry(self.frame, textvariable=self.proteins_var).grid(row=6, column=1, pady=10)

        fiber_lbl = ttk.Label(self.frame, text='Vlakna', anchor='center', borderwidth=2, relief='groove', padding=(5))
        fiber_lbl.grid(row=7, column=0)
        self.fiber_var = DoubleVar()
        ttk.Entry(self.frame, textvariable=self.fiber_var).grid(row=7, column=1, pady=10)

        food_name_lbl = ttk.Label(self.frame, text='Ime', anchor='center', borderwidth=2, relief='groove', padding=(5))
        food_name_lbl.grid(row=8, column=0)
        self.food_name_var = StringVar()
        ttk.Entry(self.frame, textvariable=self.food_name_var).grid(row=8, column=1, pady=10)

        create_btn = ttk.Button(self.frame, text='Kreiraj')
        create_btn.grid(row=9, column=1, pady=10)
