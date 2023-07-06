from tkinter import ttk, messagebox

from .template_ingredients_title_frame import TemplateIngredientsTitleFrame
from .search_meal_templates.sort_options_frame import SortOptionsFrame
from ...utility_widgets.leaf_frames import FoodTableResultsFrame
from constants.constants import meal_templates_headers, meal_templates_headers_map, MealTemplatesTableLabels
from .top_level_dialogs import DialogPickerTopLevel


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

        self.row_events_pkey = {
            '<1>': self.open_dialog_center,
        }
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

    def _update_tally_row(self, row, addition=True):
        start_id, end_id = meal_templates_headers_map['food_weight'], meal_templates_headers_map['price'] + 1
        if addition:
            row = [round(tr_d + r_d, 2) for tr_d, r_d in zip(self.tally_row[start_id:end_id], row[start_id:end_id])]
        else:
            row = [round(tr_d - r_d, 2) for tr_d, r_d in zip(self.tally_row[start_id:end_id], row[start_id:end_id])]
        # cast to int wherever it makes sense to
        row = [int(x) if int(x) == x else x for x in row]

        return ['\u2211', 'Ukupno'] + row

    def handle_scroll_up(self):
        self.parent.handle_scroll_up()

    def handle_scroll_down(self):
        self.parent.handle_scroll_down()

    def render_ingredients(self, tmplt_name):
        self.meal_template_name = tmplt_name
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
            self.template_ingredients_table_frame.render_result(ingredient, self.row_events, self.row_events_pkey)
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

    def clean_table_on_delete(self, template_name):
        """Clean whole table if current template name matches `template_name`

        This is important to check, since user can delete a meal template after
        its ingredients list was rendered. In this case a full clean of table has to
        be done since the template does not exist anymore.
        """
        mtn = getattr(self, 'meal_template_name', None)
        if mtn is not None and mtn == template_name:
            self.clean_table()

    def sort_table(self, key, reverse):
        for k, v in meal_templates_headers.items():
            if v == key:
                idx = meal_templates_headers_map[k]
                break
        self.template_ingredients_table_frame.mark_column(idx)

        if idx == meal_templates_headers_map['food_name']:
            # sort by name works based on ASCII -> compare with case insensitivity
            self.template_ingredients.sort(key=lambda row: row[idx].lower(), reverse=reverse)
        else:
            self.template_ingredients.sort(key=lambda row: row[idx], reverse=reverse)
        # since `p_key` here is actually position of an element in the list
        # I have to make sure to update it after every sort
        self.template_ingredients = [[i] + row[1:] for i, row in enumerate(self.template_ingredients)]

        self.template_ingredients_table_frame.destroy_rows()
        self.template_ingredients_table_frame.destroy_tally_row()
        for row in self.template_ingredients:
            self.template_ingredients_table_frame.render_result(row, self.row_events, self.row_events_pkey)
        self.template_ingredients_table_frame.render_tally_row(self.tally_row, self.header_events)

    def open_dialog_center(self, p_key):
        self.p_key = p_key
        self.ingredient_name = self.template_ingredients[p_key][meal_templates_headers_map['food_name']]
        DialogPickerTopLevel(self, self.ingredient_name)

    def delete_ingredient(self, dialog_picker, delete_picker):
        if len(self.template_ingredients) == 1:
            messagebox.showerror(title='Nedozvoljeno brisanje',
                                 message='Ne mogu izbrisati zadnji sastojak u predlošku',
                                 parent=delete_picker.dialog_center)
            return

        # calculate updated values and update the DB model
        mt = self.db.get_meal_template_by_name(self.meal_template_name)
        mt_content = MealTemplatesTableLabels.content.value
        mt_tally_row = MealTemplatesTableLabels.tally_row.value
        new_content = {ingredient: ing_map
                       for ingredient, ing_map in getattr(mt, mt_content).items()
                       if ingredient != self.ingredient_name}
        self.tally_row = self._update_tally_row(self.template_ingredients[self.p_key], addition=False)
        st_idx, end_idx = meal_templates_headers_map['food_weight'], meal_templates_headers_map['price'] + 1
        columns = list(meal_templates_headers_map.keys())[st_idx:end_idx]
        new_tally_row = {c: self.tally_row[meal_templates_headers_map[c]] for c in columns}
        new_values = {
            mt_content: new_content,
            mt_tally_row: new_tally_row,
        }
        self.db.update_meal_template_by_name(self.meal_template_name, **new_values)

        # make sure to update `p_key` for each row after the deletion row
        rows_to_rerender = [[row[0] - 1] + row[1:] for row in self.template_ingredients[self.p_key + 1:]]
        for row in self.template_ingredients[self.p_key:]:
            self.template_ingredients_table_frame.destroy_row(row[0])
        self.template_ingredients_table_frame.destroy_tally_row()
        for row in rows_to_rerender:
            self.template_ingredients_table_frame.render_result(row, self.row_events, self.row_events_pkey)
        self.template_ingredients_table_frame.render_tally_row(self.tally_row, self.header_events)
        self.template_ingredients = self.template_ingredients[:self.p_key] + rows_to_rerender

        self.sort_options_frame.rerender_templates_count(len(self.template_ingredients))
        dialog_picker.dialog_center.destroy()
        delete_picker.dialog_center.destroy()

        messagebox.showinfo(title='Sastojak trajno izbrisan',
                            message=f'Uspješno izbrisan `{self.ingredient_name}` sastojak')

