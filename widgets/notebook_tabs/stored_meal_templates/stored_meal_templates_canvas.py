from tkinter import Canvas

from .main_title_frame import MainTitleFrame
# from ...utility_widgets.leaf_frames import ScrollBarWidget


class StoredMealTemplatesCanvas:
    """Canvas for rendering stored meal templates in Ranah.

    Canvas is holding a trivial Frame which simply renders the Canvas' title.

    Its next child is a Canvas(!) which is responsible for searching all
    of the stored meal templates and options for sortin/adding/deleting them.

    The next child is a Frame which simply renders the ingredients list
    of a selected meal template. It also provides option for
    sorting/updating/deleting an ingredient from the meal.

    All abovementioned children are contained in the Canvas' 0th column.

    Its last child is a scrollbar widget.
    Scroll-bar widget is contained in the 1st column and is vertically scrollable
    if canvas itself ever becomes higher than the Notebook, ie the root window.
    """

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self._initialize_styles()

        self._initialize_canvas()
        
        self._initialize_title_frame()
        self._initialize_scrollbar()
        self._bind_events()
    
    def _initialize_styles(self):
        ...
    
    def _initialize_canvas(self):
        self.canvas = Canvas(self.parent, background='#5F27F1')
        # NOTE: For some reason the following line seems to be redundant
        self.canvas.grid(row=0, column=0, sticky='news')
        # enable resizing
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        # self.canvas.configure(yscrollincrement=5)
    
    def _initialize_title_frame(self):
        self.main_title_frame = MainTitleFrame(self)
        self.main_title_frame_id = self.canvas.create_window(50, 60, window=self.main_title_frame.frame, anchor='w')

    def _initialize_scrollbar(self):
        ...

    def _bind_events(self):
        # whenever canvas itself is configured, make sure the width of the child frame is the same as canvas'
        # the reason why i need to do that is because the canvas now behaves as a geometry manager(create_window method)
        # also, when the table size changes, the canvas size does not, i guess this is important for future reading
        self.canvas.bind('<Configure>', lambda _: self.canvas.itemconfigure(self.main_title_frame_id, width=self.canvas.winfo_width() - 100))
        # self.canvas.bind('<Button-4>', lambda _: self.handle_scroll_up())
        # self.canvas.bind('<Button-5>', lambda _: self.handle_scroll_down())

    def handle_scroll_up(self):
        self.canvas.yview_scroll(-5, "units")

    def handle_scroll_down(self):
        self.canvas.yview_scroll(5, "units")

    def handle_resizing(self):
        """Handle resizing of the scrollregion whenever the size of the table changes

        NOTE: This whole thing with scrollregion is a bit weirdish. Whenever the table size exceeds
        the window size, everything works as expected, but there were some problems with scrollregion
        when the table size was small, ie the canvas height was larger than the frame height
        """
        if self.frame.frame.winfo_height() > self.canvas.winfo_height():
            s_region = self.canvas.bbox('all')
            # add some extra space at the bottom, s_region is a tuple!
            s_region = s_region[:3] + (s_region[-1] + 50,)
        else:
            # for some reason works well with -2 translation
            s_region = (0, 0, 0, self.canvas.winfo_height() - 2)
        self.canvas.configure(scrollregion=s_region)

