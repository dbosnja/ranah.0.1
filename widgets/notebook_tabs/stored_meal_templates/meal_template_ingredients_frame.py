from tkinter import ttk

from .template_ingredients_title_frame import TemplateIngredientsTitleFrame
from .search_meal_templates.sort_options_frame import SortOptionsFrame
from ...utility_widgets.leaf_frames import FoodTableResultsFrame
from constants.constants import meal_templates_headers, meal_templates_headers_map, MealTemplatesTableLabels


class MealTemplateIngredientsFrame:
    """Frame for rendering details about a meal template's ingredients.

    Frame consists of 3 childrend.

    First one being a simple title, second representing some metadata
    about the list of ingredients and sorting options.

    And the 3rd one rendering the acutal table.
    """
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db

        self._create_styles()
        self._create_table_events()
        
        self.frame = ttk.Frame(parent.canvas, style='IngredientFrame.TFrame')
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()
    
    def _create_styles(self):
        ttk.Style().configure('IngredientFrame.TFrame', background='#5F27F1')

    def _create_table_events(self):
        """Define a mapping between event and their handlers for the rendered table"""

        # self.row_events_pkey = {
        #     '<Button-3>': self.delete_template_row,
        #     '<1>': self.open_dialog_center,
        # }
        self.row_events = {
            '<Button-4>': self.handle_scroll_up,
            '<Button-5>': self.handle_scroll_down,
        }

        self.header_events = {
            '<Button-4>': self.handle_scroll_up,
            '<Button-5>': self.handle_scroll_down,
        }
    
    def _create_widget_vars(self):
        st_idx, end_idx = meal_templates_headers_map['food_id'], meal_templates_headers_map['price'] + 1
        self.header_labels = list(meal_templates_headers.values())[st_idx:end_idx]
    
    def _create_widgets(self):
        self.template_ingredients_title_frame = TemplateIngredientsTitleFrame(self)

        st_idx, end_idx = meal_templates_headers_map['food_name'], meal_templates_headers_map['price'] + 1
        sort_options = list(meal_templates_headers.values())[st_idx:end_idx]
        padding = (10, 40, 0, 10)
        self.sort_options_frame = SortOptionsFrame(self, sort_options, padding)

        self.template_ingredients_table_frame = FoodTableResultsFrame(self, self.header_labels)
        self.template_ingredients_table_frame.configure_style(style_name='IngredientFrame.TFrame')
    
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

    def render_ingredients(self, tmplt_name):
        mt = self.db.get_meal_template_by_name(tmplt_name)
        mt_content = MealTemplatesTableLabels.content.value
        mt_tally_row = MealTemplatesTableLabels.tally_row.value
        self.template_ingredients = [[i] + [ig for ig in ing_map.values()]
                                     for i, ing_map in enumerate(getattr(mt, mt_content).values())]
        self.tally_row = ['\u2211', 'Ukupno'] + [i for i in getattr(mt, mt_tally_row).values()]

        # update title, enable buttons and calculate tally count
        self.template_ingredients_title_frame.render_full_title(tmplt_name)
        self.sort_options_frame.enable_buttons()
        self.sort_options_frame.rerender_templates_count(len(self.template_ingredients))

        # destroy old rows
        self.template_ingredients_table_frame.destroy_rows()
        self.template_ingredients_table_frame.destroy_tally_row()
        self.template_ingredients_table_frame.unmark_column()

        # render rows
        for ingredient in self.template_ingredients:
            self.template_ingredients_table_frame.render_result(ingredient, self.row_events)
        self.template_ingredients_table_frame.render_tally_row(self.tally_row, self.header_events)

    def get_height(self):
        return sum(getattr(fr, 'winfo_height')()
                   for fr in (
                    self.template_ingredients_title_frame.frame,
                    self.sort_options_frame.frame,
                    self.template_ingredients_table_frame.frame))

    def clean_table(self):
        self.template_ingredients_title_frame.render_prefix_title()
        self.sort_options_frame.rerender_templates_count(0)
        self.sort_options_frame.disable_buttons()

        self.template_ingredients = []
        self.tally_row = None

        self.template_ingredients_table_frame.unmark_column()
        self.template_ingredients_table_frame.destroy_rows()
        self.template_ingredients_table_frame.destroy_tally_row()

