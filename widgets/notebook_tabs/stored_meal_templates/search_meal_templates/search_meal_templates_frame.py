from tkinter import ttk

from .search_options_frame import SearchOptionsFrame
from .sort_options_frame import SortOptionsFrame

from .. .. utility_widgets.leaf_frames import FoodTableResultsFrame
from constants.constants import meal_templates_headers


class SearchMealTemplatesFrame:
    """Main Frame for searchin, sorting and rendering meal templates.
    
    Frame has 3 Frame children.
    
    First Frame is in charge of representing UI and logic for searching all
    stored meal templates.

    Second Frame is in charge of sorting options.

    Third Frame handles rendering of meal templates in a table-like diplay.
    """

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self._create_styles()

        self.frame = ttk.Frame(parent.canvas, style='SearchMealTemplates.TFrame')
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('SearchMealTemplates.TFrame', background='#FFD900')
        # ttk.Style().configure('SearchMealTemplates.TFrame', background='black')
    
    def _create_widget_vars(self):
        ...
    
    def _create_widgets(self):
        self.search_options_frame = SearchOptionsFrame(self)
        self.sort_options_frame = SortOptionsFrame(self)

        self.templates_table_frame = FoodTableResultsFrame(self, meal_templates_headers.values())
        self.templates_table_frame.set_scroll_up_handler(self.handle_scroll_up)
        self.templates_table_frame.set_scroll_down_handler(self.handle_scroll_down)
    
    def _grid_widgets(self):
        self.search_options_frame.grid(row=0, column=0, sticky='we')
        self.sort_options_frame.grid(row=1, column=0, sticky='we')
        self.templates_table_frame.grid_frame(row=2, column=0, sticky='we')
    
    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.handle_scroll_up())
        self.frame.bind('<Button-5>', lambda _: self.handle_scroll_down())

    def set_meal_template_names(self):
        self.search_options_frame.set_meal_template_names(self.db.all_meal_templates_names)

    def handle_scroll_up(self):
        self.parent.handle_scroll_up()

    def handle_scroll_down(self):
        self.parent.handle_scroll_down()

    def render_templates(self, template_names):
        self.sort_options_frame.rerender_templates_count(len(template_names))
        self.sort_options_frame.enable_buttons()
        print(template_names)

