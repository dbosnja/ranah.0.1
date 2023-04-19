from sqlalchemy import create_engine, URL

from .connection_params import URL_PARAMS
from .schema import metadata

class Database:
    """Database Interface
    
    This type provides database initialization and methods for common work with
    a database
    """
    def __init__(self):
        self.create_engine()
        self.connection = self.engine.connect()
        self.metadata = metadata
        self.persist_schema()
    
    def create_engine(self):
        db_url = URL.create(
            drivername=URL_PARAMS['drivername'],
            username=URL_PARAMS['username'],
            password=URL_PARAMS['password'],
            host=URL_PARAMS['host'],
            database=URL_PARAMS['database'],
            port=URL_PARAMS['port']
        )
        self.engine = create_engine(db_url)

    def persist_schema(self):
        self.metadata.create_all(self.engine)