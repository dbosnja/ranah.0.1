from sqlalchemy import MetaData, Table, Column, Integer, String, Numeric


metadata = MetaData()

test_table = Table(
    'test',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(), unique=True)
)

# TODO: all numeric values should default to 0.0
# TODO: index the name column
nutrition_labels_table = Table(
    'nutrition_facts_labels',
    metadata,
    Column('label_id', Integer, primary_key=True),
    Column('label_name', String, unique=True),
    Column('calories', Numeric(10, 5)),
    Column('fat', Numeric(10, 5)),
    Column('saturated_fat', Numeric(10, 5)),
    Column('carbs', Numeric(10, 5)),
    Column('sugars', Numeric(10, 5)),
    Column('proteins', Numeric(10, 5)),
    Column('fiber', Numeric(10, 5)),
)