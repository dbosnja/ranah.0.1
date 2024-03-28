from tkinter import Canvas

from .search_meal_templates_frame import SearchMealTemplatesFrame
from .. .. utility_widgets.leaf_frames import ScrollBarWidget


class SearchMealTemplatesCanvas:
    """Canvas for searching stored meal templates in Ranah.

    Canvas is holding one Frame which handles all UI and logic needed.

    Its 2nd child is a scrollbar widget.
    Scroll-bar widget is contained in the 1st column and is vertically scrollable.
    """

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self._initialize_styles()

        self._initialize_canvas()
        
        self._initialize_search_meal_templates_frame()
        self._initialize_scrollbar()
        self._bind_events()
    
    def _initialize_styles(self):
        ...
    
    def _initialize_canvas(self):
        self.canvas = Canvas(self.parent.canvas, background='#FFD900')
        # NOTE: For some reason the following line seems to be redundant
        self.canvas.grid(row=1, column=0, sticky='news')
        # enable resizing
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.configure(yscrollincrement=5)
    
    def _initialize_search_meal_templates_frame(self):
        self.search_meal_templates_frame = SearchMealTemplatesFrame(self, self.db)
        self.search_meal_templates_frame_id = self.canvas.create_window(0, 0,
                                                                        window=self.search_meal_templates_frame.frame, anchor='nw')

    def _initialize_scrollbar(self):
        scrolly = ScrollBarWidget(self.canvas)
        scrolly.attach_to_scrollable(self.canvas)
        scrolly.grid(row=0, column=1, sticky='ns')

    def _bind_events(self):
        # whenever canvas itself is configured, make sure the width of the child frame is the same as canvas'
        # the reason why i need to do that is because the canvas now behaves as a geometry manager(create_window method)
        # also, when the table size changes, the canvas size does not, i guess this is important for future reading
        self.canvas.bind('<Configure>', lambda _: self.canvas.itemconfigure(self.search_meal_templates_frame_id, width=self.canvas.winfo_width()))
        self.canvas.bind('<Button-4>', self.mouse_wheel_event_handler)
        self.canvas.bind('<Button-5>', self.mouse_wheel_event_handler)
        # for Windows and Macintosh machines
        self.canvas.bind('<MouseWheel>', self.mouse_wheel_event_handler)

    def mouse_wheel_event_handler(self, event):
        # handle mouse-wheel events for all platforms
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-5, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(5, "units")

    def handle_resizing(self):
        """Handle resizing of the scrollregion whenever the size of the table changes

        NOTE: This whole thing with scrollregion is a bit weirdish. Whenever the table size exceeds
        the window size, everything works as expected, but there were some problems with scrollregion
        when the table size was small, ie the canvas height was larger than the frame height
        """
        if self.search_meal_templates_frame.frame.winfo_height() > self.canvas.winfo_height():
            s_region = self.canvas.bbox('all')
            # add some extra space at the bottom, s_region is a tuple!
            s_region = s_region[:3] + (s_region[-1] + 50,)
        else:
            # for some reason works well with -2 translation
            s_region = (0, 0, 0, self.canvas.winfo_height() - 2)
        self.canvas.configure(scrollregion=s_region)

    def set_meal_template_names(self):
        self.search_meal_templates_frame.set_meal_template_names()

    def render_ingredients(self, tmplt_name):
        self.parent.render_ingredients(tmplt_name)

    def clean_table_on_delete(self, template_name):
        self.parent.clean_table_on_delete(template_name)

