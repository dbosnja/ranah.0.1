from sqlalchemy import create_engine, URL

from connection_params import URL_PARAMS

class Database:
    """Database Interface
    
    This type provides database initialization and methods for common work with
    a database
    """
    def __init__(self):
        self.create_engine()
        self.connection = self.engine.connect()
    
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
