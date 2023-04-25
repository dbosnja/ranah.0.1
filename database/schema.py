from sqlalchemy import MetaData, Table, Column, Integer, String, Numeric


metadata = MetaData()


nutrition_labels_table = Table(
    'nutrition_facts_labels',
    metadata,
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

# TODO: add meals table