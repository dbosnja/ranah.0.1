from tkinter import Canvas

from .main_title_frame import MainTitleFrame
from .search_meal_templates.search_meal_templates_canvas import SearchMealTemplatesCanvas
from .meal_template_ingredients_frame import MealTemplateIngredientsFrame
from ...utility_widgets.leaf_frames import ScrollBarWidget


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
        self._initialize_search_templates_canvas()
        self._initialize_ingredients_frame()
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
        self.canvas.configure(yscrollincrement=5)
    
    def _initialize_title_frame(self):
        self.main_title_frame = MainTitleFrame(self)
        self.main_title_frame_id = self.canvas.create_window(50, 20, window=self.main_title_frame.frame, anchor='nw')

    def _initialize_search_templates_canvas(self):
        self.search_templates_canvas = SearchMealTemplatesCanvas(self, self.db)
        self.search_templates_canvas_id = self.canvas.create_window(50, 150, window=self.search_templates_canvas.canvas, anchor='nw')

    def _initialize_ingredients_frame(self):
        self.meal_ingredients_frame = MealTemplateIngredientsFrame(self, self.db)
        self.meal_ingredients_frame_id = self.canvas.create_window(50, 750, window=self.meal_ingredients_frame.frame, anchor='nw')

    def _initialize_scrollbar(self):
        scrolly = ScrollBarWidget(self.canvas)
        scrolly.attach_to_scrollable(self.canvas)
        scrolly.grid(row=0, column=1, sticky='ns')

    def _bind_events(self):
        # whenever canvas itself is configured, make sure the width of the child frame is the same as canvas'
        # the reason why i need to do that is because the canvas now behaves as a geometry manager(create_window method)
        # also, when the table size changes, the canvas size does not, i guess this is important for future reading
        self.canvas.bind('<Configure>', lambda _: self._configure_canvas())
        self.canvas.bind('<Button-4>', self.mouse_wheel_event_handler)
        self.canvas.bind('<Button-5>', self.mouse_wheel_event_handler)

    def _configure_canvas(self):
        self.canvas.itemconfigure(self.main_title_frame_id, width=self.canvas.winfo_width() - 120)

        self.canvas.itemconfigure(self.search_templates_canvas_id, width=self.canvas.winfo_width() - 120)
        self.canvas.itemconfigure(self.search_templates_canvas_id, height=550)

        self.canvas.itemconfigure(self.meal_ingredients_frame_id, width=self.canvas.winfo_width() - 120)
        self.canvas.itemconfigure(self.meal_ingredients_frame_id, height=self.meal_ingredients_frame.get_height())

    def mouse_wheel_event_handler(self, event):
        # handle mouse-wheel events for all platforms
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-5, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(5, "units")

    def handle_resizing(self):
        """Handle resizing of the scrollregion whenever the size of the table changes"""

        self.canvas.itemconfigure(self.meal_ingredients_frame_id, height=self.meal_ingredients_frame.get_height())
        tally_height = sum(getattr(fr, 'winfo_height')()
                            for fr in (self.main_title_frame.frame, self.search_templates_canvas.canvas))
        tally_height += self.meal_ingredients_frame.get_height()
        # add the margins in-between the frames/Canvas
        tally_height += 112
        if tally_height > self.canvas.winfo_height():
            s_region = self.canvas.bbox('all')
            # add some extra space at the bottom and acknowledge canvas' "padding" on left, top
            # s_region is a tuple!
            s_region = (0, 0) + s_region[2:3] + (s_region[-1] + 50,)
        else:
            # for some reason works well with -2 translation
            s_region = (0, 0, 0, self.canvas.winfo_height() - 2)
        self.canvas.configure(scrollregion=s_region)

    def set_meal_template_names(self):
        self.search_templates_canvas.set_meal_template_names()

    def render_ingredients(self, tmplt_name):
        self.meal_ingredients_frame.render_ingredients(tmplt_name)

    def clean_table_on_delete(self, template_name):
        self.meal_ingredients_frame.clean_table_on_delete(template_name)

