from sqlalchemy import create_engine, URL, select, and_, extract

from .connection_params import DB_URL_PARAMS
from .schema import metadata, nutrition_labels_table, consumed_food_items_table

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
        sel = select(nutrition_labels_table.c.label_name)
        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            return [f_name for (f_name, ) in rp.fetchall()]
    
    def is_food_name_unique(self, food_name):
        # TODO: remove this interface segment, this is application code
        return food_name not in self.all_food_label_names
    
    def get_food_item_table(self, food_name):
        """Retrieve food item table based on its name
        
        The API does also formatting of the fetched data. All floats are rounded to 2 decimals
        and datetime is formatted as `day full-mont-name year HH:MM`
        """
        
        sel = select(nutrition_labels_table)
        sel = sel.where(nutrition_labels_table.c.label_name == food_name)
        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            result = list(rp.first())
        # NOTE: this will look better once I switch to ORM Alchemy mode
        result[2:-2] = [round(float(f), 2) for f in result[2:-2]]
        result[-2] = result[-2].strftime('%d-%m-%Y, %H:%M')
        result[-1] = result[-1].strftime('%d-%m-%Y, %H:%M')
        return result
    
    def create_new_consumed_food_item(self, **values):
        """Create new consumed food item record"""

        ins = consumed_food_items_table.insert().values(**values)
        # TODO: return boolean to the caller?
        with self.engine.connect() as conn:
            conn.execute(ins)
            conn.commit()
    
    def get_consumed_food_on_date(self, date):
        sel = select(consumed_food_items_table)
        sel = sel.where(
            and_(
                extract('YEAR', consumed_food_items_table.c.timestamp) == date.year,
                extract('MONTH', consumed_food_items_table.c.timestamp) == date.month,
                extract('DAY', consumed_food_items_table.c.timestamp) == date.day,
            )
        )
        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            return rp.fetchall()

