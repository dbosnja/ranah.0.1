from tkinter import ttk

from .search_options_frame import SearchOptionsFrame
from .sort_options_frame import SortOptionsFrame

from .. .. utility_widgets.leaf_frames import FoodTableResultsFrame
from constants.constants import meal_templates_headers, MealTemplatesTableLabels


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
        self.meal_templates = []

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
        """Render templates stats

        The function always evalutes on a non-empty operand.
        It deletes the old values in the table and enables sortin/cleaning
        options.
        """
        self.sort_options_frame.rerender_templates_count(len(template_names))
        self.sort_options_frame.enable_buttons()

        # delete the old results and unmark sorting column(if any)
        self.templates_table_frame.destroy_rows()
        self.templates_table_frame.unmark_column()
        self.meal_templates = []

        # NOTE: this might be better suited on the instance operand
        mt_id = MealTemplatesTableLabels.template_id.value
        mt_name = MealTemplatesTableLabels.name.value
        mt_tally_row = MealTemplatesTableLabels.tally_row.value
        mt_created_on = MealTemplatesTableLabels.created_on.value
        mt_updated_on = MealTemplatesTableLabels.updated_on.value
        # render rows
        for mt in template_names:
            row = self.db.get_meal_template_by_name(mt)
            created, updated = [d.strftime('%d-%m-%Y, %H:%M')
                                for d in (getattr(row, mt_created_on), getattr(row, mt_updated_on))]
            row = [getattr(row, mt_id), getattr(row, mt_name)] \
                  + list(getattr(row, mt_tally_row).values()) \
                  + [created, updated]
            self.meal_templates.append(row)
            # TODO: add events definitions and handlers
            self.templates_table_frame.render_result(row)

