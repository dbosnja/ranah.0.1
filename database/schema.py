from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, Numeric, DateTime


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
    Column('fiber', Numeric(10, 5), default=0),
    Column('proteins', Numeric(10, 5), default=0),
    Column('price', Numeric(10, 5), nullable=False),
    Column('created_on', DateTime, default=datetime.now),
    Column('updated_on', DateTime, default=datetime.now, onupdate=datetime.now),
)


consumed_food_items_table = Table(
    'consumed_food_items',
    metadata,
    Column('food_id', Integer, primary_key=True),
    Column('food_name', String, nullable=False),
    Column('food_weight', Numeric(10, 5), nullable=False),
    Column('calories', Numeric(10, 5), nullable=False),
    Column('fat', Numeric(10, 5), nullable=False),
    Column('saturated_fat', Numeric(10, 5), nullable=False),
    Column('carbs', Numeric(10, 5), nullable=False),
    Column('sugars', Numeric(10, 5), nullable=False),
    Column('fiber', Numeric(10, 5), nullable=False),
    Column('proteins', Numeric(10, 5), nullable=False),
    Column('price', Numeric(10, 5), nullable=False),
    Column('created_on', DateTime, default=datetime.now, nullable=False),
)

