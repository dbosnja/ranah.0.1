from sqlalchemy import create_engine, URL, select

from .connection_params import DB_URL_PARAMS
from .schema import metadata, nutrition_labels_table

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
        
        with self.engine.connect() as conn:
            # TODO: handle exceptions, e.g. Integrity Error -> this could be a complex topic
            # TODO: return the result to the caller, e.g. True/False
            ins = nutrition_labels_table.insert().values(**values)
            conn.execute(ins)
            conn.commit()
    
    def is_food_name_unique(self, food_name):
        sel = select(nutrition_labels_table.c.label_name)
        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            return food_name not in set(f_name for (f_name, ) in rp.fetchall())
    
    def get_food_item_records(self, limit=10):
        """Retrieve `limit` food item records"""
        ...