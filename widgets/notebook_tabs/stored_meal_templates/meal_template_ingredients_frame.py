from tkinter import ttk

from .template_ingredients_title_frame import TemplateIngredientsTitleFrame
from .search_meal_templates.sort_options_frame import SortOptionsFrame
from ...utility_widgets.leaf_frames import FoodTableResultsFrame
from constants.constants import meal_templates_headers, meal_templates_headers_map


class MealTemplateIngredientsFrame:
    """Frame for rendering details about a meal template's ingredients.

    Frame consists of 3 childrend.

    First one being a simple title, second representing some metadata
    about the list of ingredients and sorting options.

    And the 3rd one rendering the acutal table.
    """
    def __init__(self, parent):
        self.parent = parent

        self._create_styles()
        self._create_table_events()
        
        self.frame = ttk.Frame(parent.canvas, style='MainTitleFrame.TFrame')
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('MainTitleFrame.TFrame', background='#FFD900')

    def _create_table_events(self):
        """Define a mapping between event and their handlers for the rendered table"""

        # self.row_events_pkey = {
        #     '<Button-3>': self.delete_template_row,
        #     '<1>': self.open_dialog_center,
        # }
        # self.row_events = {
        #     '<Button-4>': self.handle_scroll_up,
        #     '<Button-5>': self.handle_scroll_down,
        # }

        self.header_events = {
            '<Button-4>': self.handle_scroll_up,
            '<Button-5>': self.handle_scroll_down,
        }
    
    def _create_widget_vars(self):
        st_idx, end_idx = meal_templates_headers_map['food_id'], meal_templates_headers_map['price'] + 1
        self.header_labels = list(meal_templates_headers.values())[st_idx:end_idx]
    
    def _create_widgets(self):
        self.template_ingredients_title_frame = TemplateIngredientsTitleFrame(self)
        self.sort_options_frame = SortOptionsFrame(self)
        self.template_ingredients_table_frame = FoodTableResultsFrame(self, self.header_labels)
        self.template_ingredients_table_frame.configure_style(style_name='MainTitleFrame.TFrame')
    
    def _grid_widgets(self):
        self.template_ingredients_title_frame.grid(row=0, column=0, sticky='we')
        self.sort_options_frame.grid(row=1, column=0, sticky='we')
        self.template_ingredients_table_frame.grid_frame(row=2, column=0, sticky='we')
        self.template_ingredients_table_frame.render_headers(self.header_events)
    
    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.handle_scroll_up())
        self.frame.bind('<Button-5>', lambda _: self.handle_scroll_down())

    def handle_scroll_up(self):
        self.parent.handle_scroll_up()

    def handle_scroll_down(self):
        self.parent.handle_scroll_down()