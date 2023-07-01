from sqlalchemy import create_engine, URL, select, and_, extract, delete, update, column

from .connection_params import DB_URL_PARAMS
from .schema import metadata, nutrition_labels_table, consumed_food_items_table, meal_templates_table, MealTemplatesTableLabels

class Database:
    """Database Interface
    
    This type provides database initialization and methods for common work with
    a database(CRUD operators)
    """
    def __init__(self, conn_string=None):
        self.engine = self._create_engine(conn_string)
        self.metadata = metadata
        self._persist_schema()
    
    def _create_engine(self, conn_string=None):
        if conn_string is not None:
            return create_engine(conn_string)
        db_url = URL.create(
            drivername=DB_URL_PARAMS['drivername'],
            username=DB_URL_PARAMS['username'],
            password=DB_URL_PARAMS['password'],
            host=DB_URL_PARAMS['host'],
            database=DB_URL_PARAMS['database'],
            port=DB_URL_PARAMS['port']
        )
        return create_engine(db_url)

    def _persist_schema(self):
        self.metadata.create_all(self.engine)
    
    def _format_food_table_row(self, row, two_dates=True):
        # NOTE: this will look better once I switch to ORM Alchemy mode
        # row[2:float_id] -> ignore primary_key and label_name dimensions
        # if a value is actually int, then always return int(instead of float)
        float_id = -2 if two_dates else -1
        tmp_row = row[2:float_id]
        for i, f in enumerate(tmp_row):
            rnd_f = round(float(f), 2)
            tmp_row[i] = rnd_f if rnd_f != int(rnd_f) else int(rnd_f)
        row[2:float_id] = tmp_row
        row[-1] = row[-1].strftime('%d-%m-%Y, %H:%M')
        if two_dates:
            row[-2] = row[-2].strftime('%d-%m-%Y, %H:%M')
        return row
    
    def insert_new_food_item_record(self, **values):
        """Insert a new nutrition table record of a food item"""

        ins = nutrition_labels_table.insert().values(**values)
        with self.engine.connect() as conn:
            # TODO: handle exceptions, e.g. Integrity Error -> this could be a complex topic
            # TODO: return the result to the caller, e.g. True/False
            conn.execute(ins)
            conn.commit()
    
    @property
    def all_food_label_names(self):
        # fetch all vectors' name dimension

        food_name_c = column('label_name')
        sel_stmt = select(food_name_c).select_from(nutrition_labels_table)
        with self.engine.connect() as conn:
            rp = conn.execute(sel_stmt)
        return [fn.label_name for fn in rp]

    @property
    def all_food_label_tables(self):
        """Return all results from the food nutrition table

        The method does an immediate formatting.
        Rationale: I'm not expecting to be using 5 digits after floating point
        anywhere or miliseconds in timestamps in Ranah.
        """
        sel = select(nutrition_labels_table)
        with self.engine.connect() as conn:
            rp = conn.execute(sel)

        return [self._format_food_table_row(list(r)) for r in rp]

    def is_food_name_unique(self, food_name):
        # TODO: remove this interface segment, this is application code
        return food_name not in self.all_food_label_names

    def get_food_item_table(self, food_name):
        """Retrieve one food item table based on its name

        The API does also formatting of the fetched data. All floats are rounded to 2 decimals
        and datetime is formatted as `day full-month-name year HH:MM`
        """
        
        sel = select(nutrition_labels_table)
        sel = sel.where(nutrition_labels_table.c.label_name == food_name)
        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            result = list(rp.first())
        
        return self._format_food_table_row(result)

    def get_food_item_table_by_primary_key(self, p_key):
        """Retrieve one food item table based on its primary_key

        The API does also formatting of the fetched data. All floats are rounded to 2 decimals
        and datetime is formatted as `day full-month-name year HH:MM`
        """
        sel = select(nutrition_labels_table)
        sel = sel.where(nutrition_labels_table.c.label_id == p_key)
        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            result = list(rp.first())

        return self._format_food_table_row(result)

    def delete_food_table(self, food_table_name):
        """Delete row with the name `food_table_name`.

        The operation is unambiguous since the name of a food table is globally unique.
        """
        del_stmt = delete(nutrition_labels_table)\
                   .where(nutrition_labels_table.c.label_name == food_table_name)
        with self.engine.connect() as conn:
            conn.execute(del_stmt)
            conn.commit()

    def update_food_item_table(self, **values):
        """Update one food item table."""

        update_stmt = update(nutrition_labels_table)\
                  .where(nutrition_labels_table.c.label_name == values['label_name'])\
                  .values(values)
        with self.engine.connect() as conn:
            conn.execute(update_stmt)
            conn.commit()

    def create_new_consumed_food_item(self, **values):
        """Create new consumed food item record"""

        ins = consumed_food_items_table.insert().values(**values)
        # TODO: return boolean to the caller?
        with self.engine.connect() as conn:
            conn.execute(ins)
            conn.commit()
    
    def get_consumed_food_on_date(self, start_time, end_time):
        """Fetch all food consumed on `start_time`.

        If `end_time` is defined then fetch all food consumed within the time segment.
        """
        sel = select(consumed_food_items_table)
        if end_time is None:
            sel = sel.where(
                and_(
                    extract('YEAR', consumed_food_items_table.c.created_on) == start_time.year,
                    extract('MONTH', consumed_food_items_table.c.created_on) == start_time.month,
                    extract('DAY', consumed_food_items_table.c.created_on) == start_time.day,
                )
            )
        else:
            sel = sel.where(
                consumed_food_items_table.c.created_on.between(start_time, end_time)
            )

        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            return [self._format_food_table_row(list(row), False) for row in rp.fetchall()]

    def get_consumed_food_by_primary_key(self, p_key):
        """Retrieve consumed food item based on its primary_key"""

        sel = select(consumed_food_items_table)
        sel = sel.where(consumed_food_items_table.c.food_id == p_key)
        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            result = list(rp.first())

        return self._format_food_table_row(result, False)

    def delete_consumed_food_by_primary_key(self, p_key):
        """Delete consumed food with primary key `p_key`."""

        del_stmt = delete(consumed_food_items_table)
        del_stmt = del_stmt.where(consumed_food_items_table.c.food_id == p_key)
        with self.engine.connect() as conn:
            conn.execute(del_stmt)
            conn.commit()

    def update_consumed_food_item(self, p_key, **values):
        """Update one consumed food item based on its primary key"""

        update_stmt = update(consumed_food_items_table)
        update_stmt = update_stmt.where(consumed_food_items_table.c.food_id == p_key)
        update_stmt = update_stmt.values(values)
        with self.engine.connect() as conn:
            conn.execute(update_stmt)
            conn.commit()

    def get_all_consumed_food_names(self):
        """Return a set of all consumed food names"""

        food_name_c = column('food_name')
        sel_stmt = select(food_name_c).select_from(consumed_food_items_table)
        with self.engine.connect() as conn:
            rp = conn.execute(sel_stmt)
        food_names = {fn.food_name for fn in rp}
        return food_names

    def get_consumed_foods_by_name(self, food_name):
        """Return all vectors with name `food_name`"""

        sel_stmt = select(consumed_food_items_table)
        sel_stmt = sel_stmt.where(consumed_food_items_table.c.food_name == food_name)
        with self.engine.connect() as conn:
            rp = conn.execute(sel_stmt)
            return [self._format_food_table_row(list(r), False) for r in rp]


    def create_new_meal_template(self, **values):
        """Create new vector in meal templates space"""

        ins_stmt = meal_templates_table.insert().values(**values)
        with self.engine.connect() as conn:
            conn.execute(ins_stmt)
            conn.commit()

    @property
    def all_meal_templates_names(self):
        """Fetch all first dimensions among all vectors in meal-templates space"""

        template_name = MealTemplatesTableLabels.name.value
        name_c = column(template_name)
        sel_stmt = select(name_c).select_from(meal_templates_table)

        with self.engine.connect() as conn:
            rp = conn.execute(sel_stmt)
            return [getattr(row, template_name) for row in rp]

    def get_meal_template_by_name(self, tmplt_name):
        """Return one meal template with name `tmplt_name`"""

        col_name = MealTemplatesTableLabels.name.value
        sel_stmt = select(meal_templates_table)
        sel_stmt = sel_stmt.where(getattr(meal_templates_table.c, col_name) == tmplt_name)
        with self.engine.connect() as conn:
            rp = conn.execute(sel_stmt)
            return rp.first()
