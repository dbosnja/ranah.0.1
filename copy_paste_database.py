# NOTE: tread lightly with this script; it can modify a complete database

from sqlalchemy import URL, create_engine, select, Table, MetaData, Column, Integer, String, Numeric

from database.schema import nutrition_labels_table


metadata2 = MetaData()


nutrition_labels_table2 = Table(
    'nutrition_facts_labels',
    metadata2,
    Column('label_id', Integer, primary_key=True),
    Column('label_name', String, unique=True, index=True),
    Column('calories', Numeric(10, 5), default=0),
    Column('fat', Numeric(10, 5), default=0),
    Column('saturated_fat', Numeric(10, 5), default=0),
    Column('carbs', Numeric(10, 5), default=0),
    Column('sugars', Numeric(10, 5), default=0),
    Column('proteins', Numeric(10, 5), default=0),
    Column('fiber', Numeric(10, 5), default=0),
)


DB_URL_PARAMS1 = {
    'drivername': 'postgresql+psycopg2',
    'username': 'ranah',
    'password': 'ranah',
    'host': 'localhost',
    'database': 'ranah_01',
    'port': 5432
}

DB_URL_PARAMS2 = {
    'drivername': 'postgresql+psycopg2',
    'username': 'ranah2',
    'password': 'ranah2',
    'host': 'localhost2',
    'database': 'ranah_022',
    'port': 54322
}

class Database:
    def __init__(self, db_url_params, nutrition_labels_table):
        self.nutrition_labels_table = nutrition_labels_table
        self.engine = self._create_engine(db_url_params)
    
    def _create_engine(self, DB_URL_PARAMS=None):
        db_url = URL.create(
            drivername=DB_URL_PARAMS['drivername'],
            username=DB_URL_PARAMS['username'],
            password=DB_URL_PARAMS['password'],
            host=DB_URL_PARAMS['host'],
            database=DB_URL_PARAMS['database'],
            port=DB_URL_PARAMS['port']
        )
        return create_engine(db_url)

    def all_food_label_names(self):
        sel = select(self.nutrition_labels_table.c.label_name)
        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            return [f_name for (f_name, ) in rp.fetchall()]
    
    def insert_new_food_item_record(self, **values):
        ins = self.nutrition_labels_table.insert().values(**values)
        with self.engine.connect() as conn:
            conn.execute(ins)
            conn.commit()
    
    def get_food_item_table(self, food_name):
        sel = select(self.nutrition_labels_table)
        sel = sel.where(self.nutrition_labels_table.c.label_name == food_name)
        with self.engine.connect() as conn:
            rp = conn.execute(sel)
            result = list(rp.first())
            return result[1:]
    
db1 = Database(DB_URL_PARAMS1, nutrition_labels_table2)
db2 = Database(DB_URL_PARAMS2, nutrition_labels_table)

for food_name in db1.all_food_label_names():
    row = db1.get_food_item_table(food_name)
    values = {
        'label_name': row[0],
        'calories': row[1],
        'fat': row[2],
        'saturated_fat': row[3],
        'carbs': row[4],
        'sugars': row[5],
        'proteins': row[6],
        'fiber': row[7],
        'price': 0,
    }
    db2.insert_new_food_item_record(**values)

input()

