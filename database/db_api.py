from sqlalchemy import create_engine, URL

from .connection_params import URL_PARAMS
from .schema import metadata

class Database:
    """Database Interface
    
    This type provides database initialization and methods for common work with
    a database(CRUD operators)
    """
    def __init__(self):
        self._create_engine()
        self.connection = self.engine.connect()
        self.metadata = metadata
        self._persist_schema()
    
    def _create_engine(self):
        db_url = URL.create(
            drivername=URL_PARAMS['drivername'],
            username=URL_PARAMS['username'],
            password=URL_PARAMS['password'],
            host=URL_PARAMS['host'],
            database=URL_PARAMS['database'],
            port=URL_PARAMS['port']
        )
        self.engine = create_engine(db_url)

    def _persist_schema(self):
        self.metadata.create_all(self.engine)
    
    def insert_new_food_item_record(self, *, table_name='food_items', **values):
        """Insert a new nutrition table record of a food item"""
        ...
    
    def get_food_item_records(self, limit=10):
        """Retrieve `limit` food item records"""
        ...