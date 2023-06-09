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
        self.canvas = Canvas(self.parent, background='#ADE6E1')
        self.canvas.grid(row=0, column=0, sticky='news')
        # enable resizing
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)

        self.screen_width = self.canvas.winfo_screenwidth()
        self.screen_height = self.canvas.winfo_screenheight()
        self.canvas.configure(yscrollincrement=5)

    def _initialize_frame(self):
        self.frame = StoredFoodTablesFrame(self, self.db)
        self.frame_id = self.canvas.create_window(0, 0, window=self.frame.frame, anchor='nw')    
    
    def _initialize_scrollbar(self):
        scrolly = ScrollBarWidget(self.canvas)
        scrolly.attach_to_scrollable(self.canvas)
        scrolly.grid(row=0, column=1, sticky='ns')
    
    def _bind_events(self):
        self.canvas.bind_all('<Configure>', lambda _: self._configure_frame_surface())
        # TODO: add arrow-up/down also for scrolling -> can't do at the moment since combobox is also handling these types of events
        self.canvas.bind_all('<Button-4>', lambda _: self.canvas.yview_scroll(-5, "units"))
        self.canvas.bind_all('<Button-5>', lambda _: self.canvas.yview_scroll(5, "units"))
        self.canvas.bind_all('<Map>', lambda _: self._adjust_height())
    
    def _configure_frame_surface(self):
        # NOTE: not really sure why this event solves this task of resizing, but it does
        self.canvas.itemconfigure(self.frame_id, width=self.canvas.winfo_width())
        if len(self.frame.food_tables) <= 25:
            self.canvas.itemconfigure(self.frame_id, height=self.canvas.winfo_height())
        else:
            delta = len(self.frame.food_tables) - 25
            self.new_frame_height = self.screen_height + delta * 32
            self.canvas.itemconfigure(self.frame_id, height=self.new_frame_height)
    
    def _adjust_height(self):
        """Adjust height of canvas if number of rendered results is greater than 25"""
        # TODO: remove 25 and base the logic on the screen height and number of results
        if len(self.frame.food_tables) <= 25:
            # no need for resizing, keep the defaults
            self.canvas.configure(height=self.screen_height)
            self.canvas.configure(scrollregion=(0, 0, 0, self.canvas.winfo_height() - 2))
        else:
            delta = len(self.frame.food_tables) - 25
            self.new_canvas_height = self.screen_height + delta * 32
            self.canvas.configure(height=self.new_canvas_height)
            self.canvas.configure(scrollregion=(0, 0, 0, self.new_canvas_height))

