from tkinter import Canvas

from .frame_widgets import StoredFoodTablesFrame
from .. utility_widgets import ScrollBarWidget


class StoredFoodTablesCanvas:
    """Canvas widget for rendering StoredFoodTablesFrame and its assocciated widgets"""

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self._initialize_canvas()
        self._initialize_frame()
        self._initialize_scrollbar()

    def _initialize_canvas(self):
        self.canvas = Canvas(self.parent)
        self.canvas.grid(row=0, column=0, sticky='news')
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)

        self.screen_width = self.canvas.winfo_screenwidth()
        self.screen_height = self.canvas.winfo_screenheight()
        self.canvas.configure(width=self.screen_width)
        self.canvas.configure(height=self.screen_height)
        self.canvas.configure(scrollregion=(0, 0, 0, self.screen_height))
        # self.canvas.configure(yscrollincrement=0)

    def _initialize_frame(self):
        frame = StoredFoodTablesFrame(self.canvas, self.db)
        self.frame_id = self.canvas.create_window(0, 0, window=frame.frame, anchor='nw')
        self.canvas.bind('<Configure>', lambda _: self._configure_frame_surface())
    
    def _initialize_scrollbar(self):
        scrolly = ScrollBarWidget(self.canvas)
        scrolly.attach_to_scrollable(self.canvas)
        scrolly.grid(row=0, column=1, sticky='ns')
    
    def _configure_frame_surface(self):
        self.canvas.itemconfigure(self.frame_id, width=self.canvas.winfo_width())
        self.canvas.itemconfigure(self.frame_id, height=self.canvas.winfo_height())

