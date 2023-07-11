from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, Numeric, DateTime, PickleType

from constants.constants import (MealTemplatesTableLabels,
                                 NUTRITION_LABELS_NUMERIC_DEFAULT,
                                 DB_SCHEMA_NUMERIC_PRECISION,
                                 DB_SCHEMA_NUMERIC_SCALE)


metadata = MetaData()


DEFAULT_NUMERIC_TYPE = Numeric(DB_SCHEMA_NUMERIC_PRECISION, DB_SCHEMA_NUMERIC_SCALE)


nutrition_labels_table = Table(
    'nutrition_facts_labels',
    metadata,
    Column('label_id', Integer, primary_key=True),
    Column('label_name', String, unique=True, index=True),
    Column('calories', DEFAULT_NUMERIC_TYPE, default=NUTRITION_LABELS_NUMERIC_DEFAULT),
    Column('fat', DEFAULT_NUMERIC_TYPE, default=NUTRITION_LABELS_NUMERIC_DEFAULT),
    Column('saturated_fat', DEFAULT_NUMERIC_TYPE, default=NUTRITION_LABELS_NUMERIC_DEFAULT),
    Column('carbs', DEFAULT_NUMERIC_TYPE, default=NUTRITION_LABELS_NUMERIC_DEFAULT),
    Column('sugars', DEFAULT_NUMERIC_TYPE, default=NUTRITION_LABELS_NUMERIC_DEFAULT),
    Column('fiber', DEFAULT_NUMERIC_TYPE, default=NUTRITION_LABELS_NUMERIC_DEFAULT),
    Column('proteins', DEFAULT_NUMERIC_TYPE, default=NUTRITION_LABELS_NUMERIC_DEFAULT),
    Column('price', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('created_on', DateTime, default=datetime.now),
    Column('updated_on', DateTime, default=datetime.now, onupdate=datetime.now),
)


consumed_food_items_table = Table(
    'consumed_food_items',
    metadata,
    Column('food_id', Integer, primary_key=True),
    Column('food_name', String, nullable=False),
    Column('food_weight', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('calories', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('fat', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('saturated_fat', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('carbs', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('sugars', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('fiber', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('proteins', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('price', DEFAULT_NUMERIC_TYPE, nullable=False),
    Column('created_on', DateTime, default=datetime.now, nullable=False),
)


meal_templates_table = Table(
    MealTemplatesTableLabels.table_name.value,
    metadata,
    Column(MealTemplatesTableLabels.template_id.value, Integer, primary_key=True),
    Column(MealTemplatesTableLabels.name.value, String, nullable=False, unique=True),
    Column(MealTemplatesTableLabels.content.value, PickleType, nullable=False),
    Column(MealTemplatesTableLabels.tally_row.value, PickleType, nullable=False),
    Column(MealTemplatesTableLabels.created_on.value, DateTime, default=datetime.now),
    Column(MealTemplatesTableLabels.updated_on.value, DateTime, default=datetime.now, onupdate=datetime.now),
)

