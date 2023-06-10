from tkinter import Canvas

from .consumed_food_items_frame import ConsumedFoodItemsFrame
from ... utility_widgets.leaf_frames import ScrollBarWidget


class ConsumedFoodItemsCanvas:
    """Canvas holding a Frame and a scroll-bar widget.
    
    The Frame is in the 0th column and consists of a couple of sub-frames
    holding widgets and logic needed to implement the corresponding UI

    Scroll-bar widget is contained in the 1st column and is vertically scrollable
    if canvas itself ever becomes higher than the Notebook, ie the root window.
    """

    CANVAS_ID = 3

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self._initialize_canvas()
        self._initialize_frame()
        self._initialize_scrollbar()
        self._bind_events()
    
    def _initialize_canvas(self):
        self.canvas = Canvas(self.parent, background='#f0dbdb')
        # enable resizing
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.configure(scrollregion=(0, 0, 0, 2000))
        self.canvas.configure(yscrollincrement=5)
    
    def _initialize_frame(self):
        self.frame = ConsumedFoodItemsFrame(self, self.db)
        self.frame_id = self.canvas.create_window(0, 0, window=self.frame.frame, anchor='nw')

    def _initialize_scrollbar(self):
        scrolly = ScrollBarWidget(self.canvas)
        scrolly.attach_to_scrollable(self.canvas)
        scrolly.grid(row=0, column=1, sticky='ns')
    
    def _handle_scroll_up(self, event):
        # breakpoint()
        # if any(f'canvas{self.CANVAS_ID}' in tag for tag in event.widget.bindtags()):
        #     self.canvas.yview_scroll(-5, "units")
        self.canvas.yview_scroll(-5, "units")
    
    def _handle_scroll_down(self, event):
        # if any(f'canvas{self.CANVAS_ID}' in tag for tag in event.widget.bindtags()):
        #     self.canvas.yview_scroll(5, "units")
        self.canvas.yview_scroll(5, "units")
    
    def _bind_events(self):
        self.canvas.bind('<Map>', lambda _: self.canvas.itemconfigure(self.frame_id, width=self.canvas.winfo_width()))
        self.canvas.bind('<Button-4>', lambda event: self._handle_scroll_up(event))
        self.canvas.bind('<Button-5>', lambda event: self._handle_scroll_down(event))
        pass
    
    def _handle_resize(self):
        print(f'table size from canvas: {self.frame.consumed_food_table_frame.frame.winfo_height()}')
        self.canvas.itemconfigure(self.frame_id, width=self.canvas.winfo_width())
        self.canvas.itemconfigure(self.frame_id, height=2000)
        print(f'frame size: {self.frame.frame.winfo_height()}')
