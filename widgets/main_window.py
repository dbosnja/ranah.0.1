from .main_notebook import MainNotebook


class MainWindow:
    """Top-level Tk Frame, a.k.a. root
    
    This main window is in control of all other present widgets.
    It is mainly concerned with configuring the root widget(ranah app)
    and initializing its direct child, which is the ranah notebook.

    The children of ranah notebook are Canvas widgets which hold frames
    for each tab in the notebook, simulating a single page application.
    """

    # TODO: handle <Escape> event better -> separate between dev and prod mode
    # dev mode -> Escape quits the app; prod mode -> pop-up asks are you sure

    ROOT_TITLE = 'ranah.2.0'
    
    def __init__(self, root, db):
        self.db = db
        self._initialize_the_root(root)
        MainNotebook(self.root, self.db)
    
    def _initialize_the_root(self, root):
        self.root = root
        self.root.title(self.ROOT_TITLE)
        self.root.geometry(f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}')
        # convenience
        self.root.bind('<Escape>', lambda _: self.root.destroy())
        # enable resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        # hardcoded values -> defined with trial and error method
        self.root.minsize(width=1500, height=700)
    
    def mainloop(self):
        self.root.mainloop()

