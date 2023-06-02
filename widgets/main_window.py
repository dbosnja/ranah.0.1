from .main_notebook import MainNotebook


class MainWindow:
    """Top-level Tk Frame, a.k.a. root
    
    This main window is in control of all other present widgets.
    It is mainly concerned with configuring the root widget(ranah app)
    and initializing its direct child, which is the ranah notebook.

    The children of ranah notebook are Canvas widgets which hold frames
    for each tab in the notebook, simulating a single page application.
    """

    ROOT_TITLE = 'ranah.2.0.'
    ROOT_DIMENSION = '900x800+2500+150'
    
    def __init__(self, root, db):
        self.db = db
        self._initialize_the_root(root)
        MainNotebook(self.root, self.db)
    
    def _initialize_the_root(self, root):
        self.root = root
        self.root.title(self.ROOT_TITLE)
        self.root.geometry(self.ROOT_DIMENSION)
        # convenience
        self.root.bind('<Escape>', lambda _: self.root.quit())
        # enable resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def mainloop(self):
        self.root.mainloop()
