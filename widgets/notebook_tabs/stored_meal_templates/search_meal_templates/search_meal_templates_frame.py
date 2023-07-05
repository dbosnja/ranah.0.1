from datetime import datetime
from tkinter import ttk, messagebox

from .search_options_frame import SearchOptionsFrame
from .sort_options_frame import SortOptionsFrame

from .. .. utility_widgets.leaf_frames import FoodTableResultsFrame
from constants.constants import (meal_templates_headers,
                                 MealTemplatesTableLabels,
                                 meal_templates_headers_map,
                                 MealTemplatesTableColumnsOrder,
                                 consumed_food_map,
                                 )
from .top_level_dialogs import DialogPickerTopLevel


class SearchMealTemplatesFrame:
    """Main Frame for searchin, sorting and rendering meal templates.
    
    Frame has 3 Frame children.
    
    First Frame is in charge of representing UI and logic for searching all
    stored meal templates.

    Second Frame is in charge of sorting options.

    Third Frame handles rendering of meal templates in a table-like diplay.
    """

    NORMATIVE = 100

    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.meal_templates = []

        self._create_styles()
        self._create_table_events()

        self.frame = ttk.Frame(parent.canvas, style='SearchMealTemplates.TFrame')
        self.frame.columnconfigure(0, weight=1)

        self._create_widget_vars()
        self._create_widgets()
        self._grid_widgets()
        self._bind_events()

    def _create_styles(self):
        ttk.Style().configure('SearchMealTemplates.TFrame', background='#FFD900')

    def _create_widget_vars(self):
        ...

    def _create_widgets(self):
        self.search_options_frame = SearchOptionsFrame(self)

        st_idx = meal_templates_headers_map['food_name']
        sort_options = list(meal_templates_headers.values())[st_idx:]
        self.sort_options_frame = SortOptionsFrame(self, sort_options)

        self.templates_table_frame = FoodTableResultsFrame(self, meal_templates_headers.values())
        self.templates_table_frame.configure_style('SearchMealTemplates.TFrame')

    def _grid_widgets(self):
        self.search_options_frame.grid(row=0, column=0, sticky='we')
        self.sort_options_frame.grid(row=1, column=0, sticky='we')
        self.templates_table_frame.grid_frame(row=2, column=0, sticky='we')
        self.templates_table_frame.render_headers(self.header_events)

    def _bind_events(self):
        self.frame.bind('<Button-4>', lambda _: self.handle_scroll_up())
        self.frame.bind('<Button-5>', lambda _: self.handle_scroll_down())

    def _create_table_events(self):
        """Define a mapping between event and their handlers for the rendered table"""

        self.row_events_pkey = {
            '<Button-3>': self.delete_template_row,
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

    def _add_consumed_food(self, ratio, food_values, consumed_datetime, columns):
        whole = 1.0
        values = {col: food_values[col] for col in columns}
        if ratio != whole:
            # scale the values
            for col in columns:
                values[col] = round(food_values[col] * ratio, 2)
        values['created_on'] = consumed_datetime
        values['food_name'] = food_values['food_name']
        self.db.create_new_consumed_food_item(**values)

    def set_meal_template_names(self):
        self.search_options_frame.set_meal_template_names(self.db.all_meal_templates_names)

    def handle_scroll_up(self):
        self.parent.handle_scroll_up()

    def handle_scroll_down(self):
        self.parent.handle_scroll_down()

    def render_templates(self, template_names):
        """Render templates stats

        The function always evalutes on a non-empty operand.
        It deletes the old values in the table and enables sorting/cleaning
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
            self.templates_table_frame.render_result(row, self.row_events, self.row_events_pkey)

    def clean_table(self):
        """Clean all rows from the table"""

        self.sort_options_frame.rerender_templates_count(0)
        self.sort_options_frame.disable_buttons()
        self.templates_table_frame.unmark_column()
        self.meal_templates = []
        self.templates_table_frame.destroy_rows()

    def sort_table(self, key, reverse):
        """Sort rows from the table based on key"""

        for k, v in meal_templates_headers.items():
            if v == key:
                idx = meal_templates_headers_map[k]
        self.templates_table_frame.mark_column(idx)

        if idx == meal_templates_headers_map['food_name']:
            # sort by name works based on ASCII -> compare with case insensitivity
            self.meal_templates.sort(key=lambda row: row[idx].lower(), reverse=reverse)
        elif idx in (meal_templates_headers_map['created_on'], meal_templates_headers_map['updated_on']):
            # sort by datetime instances instead of strings representing datetime stamp
            self.meal_templates.sort(key=lambda row: datetime.strptime(row[idx], '%d-%m-%Y, %H:%M'), reverse=reverse)
        else:
            self.meal_templates.sort(key=lambda row: row[idx], reverse=reverse)

        self.templates_table_frame.destroy_rows()
        for row in self.meal_templates:
            self.templates_table_frame.render_result(row, self.row_events, self.row_events_pkey)

    def delete_template_row(self, p_key):
        """Delete a row from the table with element `p_key`"""

        mt_template_id = MealTemplatesTableColumnsOrder.template_id.value
        # update the rows count
        meal_templates_left = len(self.meal_templates) - 1
        self.sort_options_frame.rerender_templates_count(meal_templates_left)
        if not meal_templates_left:
            self.sort_options_frame.disable_buttons()

        # delete appropriate row and re-render the rest
        for i, row in enumerate(self.meal_templates):
            if row[mt_template_id] == p_key:
                del_idx = i
                break
        rows_to_rerender = self.meal_templates[del_idx + 1:]
        for row in self.meal_templates[del_idx:]:
            prim_key = row[mt_template_id]
            self.templates_table_frame.destroy_row(prim_key)
        for row in rows_to_rerender:
            self.templates_table_frame.render_result(row, self.row_events, self.row_events_pkey)
        self.meal_templates = self.meal_templates[:del_idx] + rows_to_rerender

    def open_dialog_center(self, p_key):
        """Open dialog center for a template row"""

        self.selected_p_key = p_key
        self.selected_mt = self.db.get_meal_template_by_primary_key(p_key)
        self.selected_mt_name = getattr(self.selected_mt, MealTemplatesTableLabels.name.value)
        DialogPickerTopLevel(self, self.selected_mt_name)

    def delete_template_permanently(self, top_dialog, delete_dialog):
        self.db.delete_meal_template_by_primary_key(self.selected_p_key)
        self.clean_table()
        self.set_meal_template_names()
        delete_dialog.dialog_center.destroy()
        top_dialog.dialog_center.destroy()
        messagebox.showinfo(title='Predložak trajno izbrisan',
                            message=f'`{self.selected_mt_name}` uspješno izbrisan.')


    def add_template_as_consumed(self, top_dialog, add_dialog, user_input):
        con_year = user_input['year']
        con_month = user_input['month']
        con_day = user_input['day']
        con_hour = user_input['hour']
        con_minute = user_input['minute']
        consumed_datetime = f'{con_day}-{con_month}-{con_year}, {con_hour}:{con_minute}'
        try:
            consumed_datetime = datetime.strptime(consumed_datetime, '%d-%m-%Y, %H:%M')
        except ValueError:
            messagebox.showerror(title='Ilegalan datum',
                                 message=f'Datum `{consumed_datetime}` ne postoji!',
                                 parent=add_dialog.dialog_center)
            return
        tmplt_percentage = int(user_input['tmplt_percentage'])
        ratio = tmplt_percentage / self.NORMATIVE
        st_idx, end_idx = consumed_food_map['food_weight'], consumed_food_map['price'] + 1
        columns = list(consumed_food_map.keys())[st_idx:end_idx]
        tmplt_content = getattr(self.selected_mt, MealTemplatesTableLabels.content.value)
        for food_values in tmplt_content.values():
            self._add_consumed_food(ratio, food_values, consumed_datetime, columns)
        add_dialog.dialog_center.destroy()
        top_dialog.dialog_center.destroy()
        messagebox.showinfo(title='Predložak iskonzumiran',
                            message=f'Predložak `{self.selected_mt_name}` dodan kao konzumiran')

