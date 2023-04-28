from .create_food_label_frame import CreateFoodLabelFrame
from .stored_food_labels_frame import StoredFoodLabelsFrame
from .consumed_food_items_frame import ConsumedFoodItemsFrame


ROOT_TITLE = 'ranah.0.1.'
ROOT_DIMENSION = '900x800+2500+150'


class MainWindow:
    """Top-level Tk Frame, a.k.a. root
    
    This main window is in control of all other present widgets.
    It is mainly concerned with configuring the root widget(ranah app)
    and initializing its direct children frames
    """
    child_frames = (
            CreateFoodLabelFrame,
            StoredFoodLabelsFrame,
            ConsumedFoodItemsFrame,
        )
    
    def __init__(self, root, db):
        self._initialize_the_root(root)
        self.db = db
        self._attach_child_frames()
    
    def _initialize_the_root(self, root):
        self.root = root
        self.root.title(ROOT_TITLE)
        self.root.geometry(ROOT_DIMENSION)
        # convenience
        self.root.bind('<Escape>', lambda _: self.root.quit())
        # enable resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

    def _attach_child_frames(self):
        # Do I need the instances of the children frames?
        for ch_f in self.child_frames:
            ch_f(self.root, self.db)
    
    def mainloop(self):
        self.root.mainloop()

