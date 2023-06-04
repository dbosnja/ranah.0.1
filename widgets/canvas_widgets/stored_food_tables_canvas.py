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
        self._bind_events()

    def _initialize_canvas(self):
        self.canvas = Canvas(self.parent)
        self.canvas.grid(row=0, column=0, sticky='news')
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)

        self.screen_width = self.canvas.winfo_screenwidth()
        self.screen_height = self.canvas.winfo_screenheight()
        self.canvas.configure(width=self.screen_width)
        self.canvas.configure(height=self.screen_height)
        self.canvas.configure(yscrollincrement=3)

    def _initialize_frame(self):
        frame = StoredFoodTablesFrame(self.canvas, self.db)
        self.frame_id = self.canvas.create_window(0, 0, window=frame.frame, anchor='nw')
        self.canvas.bind('<Configure>', lambda _: self._configure_frame_surface())
    
    def _initialize_scrollbar(self):
        scrolly = ScrollBarWidget(self.canvas)
        scrolly.attach_to_scrollable(self.canvas)
        scrolly.grid(row=0, column=1, sticky='ns')
        scrolly
    
    def _bind_events(self):
        self.canvas.bind_all('<Button-4>', lambda _: self.canvas.yview_scroll(-5, "units"))
        self.canvas.bind_all('<Button-5>', lambda _: self.canvas.yview_scroll(5, "units"))
        # no idea why it's working with - 2; one thing's clear though
        # dimensions information are known only after the geometry manager renders all requested widgets
        self.canvas.bind_all('<Map>', lambda _: self.canvas.configure(scrollregion=(0, 0, 0, self.canvas.winfo_height() - 2)))
    
    def _configure_frame_surface(self):
        self.canvas.itemconfigure(self.frame_id, width=self.canvas.winfo_width())
        self.canvas.itemconfigure(self.frame_id, height=self.screen_height)

