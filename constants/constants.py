"""General constants module for ranah app

If the app grows larger, it'd probably make sense to split
this module into several modules within a (sub)package
"""

from enum import StrEnum, IntEnum, auto


class NotebookTabLabels(StrEnum):
    new_nutrition_table = 'Nova nutritivna tablica'
    all_nutrition_tables = 'Sve nutritivne tablice',
    consumed_food = 'Konzumirana hrana',
    new_meal_template = 'Novi predložak objeda',
    stored_meal_templates = 'Svi predlošci objedâ',


class MealTemplatesTableLabels(StrEnum):
    table_name = 'meal_templates'
    template_id = 'template_id'
    name = 'name'
    content = 'content'
    tally_row = 'tally_row'
    created_on = 'created_on'
    updated_on = 'updated_on'


class MealTemplatesTableColumnsOrder(IntEnum):
    template_id = auto(0)
    name = auto()
    content = auto()
    tally_row = auto()
    created_on = auto()
    updated_on = auto()


NORMATIVE = 100


NUTRITION_LABELS_NUMERIC_DEFAULT = .0
DB_SCHEMA_NUMERIC_PRECISION = 10
DB_SCHEMA_NUMERIC_SCALE = 4


# TODO: clean this file up a bit, some names are misleading,
# also back-patching definitions should have same type for both Canvas

# TODO: consider using Enum types here for the definitions

# TODO: clean this operand -> it mixes values from two different tabs(create food and stored food)
text_constants = {
        'topic_lbl': 'Nutritivne vrijednosti na 100 grama/miliLitara artikla',
        'calory_lbl': 'Kalorije',
        'fat_lbl': 'Masti',
        'sat_fat_lbl': 'Zasićene masti',
        'carb_lbl': 'Ugljikohidrati',
        'sugar_lbl': 'Šećeri',
        'protein_lbl': 'Bjelančevine',
        'fiber_lbl': 'Vlakna',
        'food_name_lbl': 'Ime',
        'create_btn': 'Kreiraj',
        'food_weight': 'Masa',
        'food_price_lbl': 'Cijena',
        'food_created_on': 'Kreirano',
        'food_updated_on': 'Ažurirano',
    }


# back-patching between definitions of `nutrition_facts_labels` database schema and application codebase
nutrition_table_map = {
    'label_id': 0,
    'label_name': 1,
    'calories': 2,
    'fat': 3,
    'saturated_fat': 4,
    'carbs': 5,
    'sugars': 6,
    'fiber': 7,
    'proteins': 8,
    'price': 9,
    'created_on': 10,
    'updated_on': 11,
}


nutrition_table_headers = {
    '#': '#',
    'label_name': 'Ime',
    'calories': 'Kalorije',
    'fat': 'Masti',
    'saturated_fat': 'Zasićene masti',
    'carbs': 'Ugljikohidrati',
    'sugars': 'Šećeri',
    'fiber': 'Vlakna',
    'proteins': 'Bjelančevine',
    'price': 'Cijena',
    'created_on': 'Kreirano',
    'updated_on': 'Ažurirano',
}


# back-patching between definitions of `consumed_food_items` database schema and application codebase
consumed_food_map = {
    'food_id': 0,
    'food_name': 1,
    'food_weight': 2,
    'calories': 3,
    'fat': 4,
    'saturated_fat': 5,
    'carbs': 6,
    'sugars': 7,
    'fiber': 8,
    'proteins': 9,
    'price': 10,
    'created_on': 11,
}


consumed_food_headers = {
    '#': '#',
    'food_name': 'Ime',
    'food_weight': 'Masa',
    'calories': 'Kalorije',
    'fat': 'Masti',
    'saturated_fat': 'Zasićene masti',
    'carbs': 'Ugljikohidrati',
    'sugars': 'Šećeri',
    'fiber': 'Vlakna',
    'proteins': 'Bjelančevine',
    'price': 'Cijena',
    'created_on': 'Konzumirano',
}


consumed_food_timestamp_map = {
    'year': 'Godina',
    'month': 'Mjesec',
    'day': 'Dan',
    'hour': 'Sat',
    'minute': 'Minuta',
}


# back-patching between definitions of `meal_templates` database schema and application codebase
meal_templates_headers_map = {
    'food_id': 0,
    'food_name': 1,
    'food_weight': 2,
    'calories': 3,
    'fat': 4,
    'saturated_fat': 5,
    'carbs': 6,
    'sugars': 7,
    'fiber': 8,
    'proteins': 9,
    'price': 10,
    'created_on': 11,
    'updated_on': 12,
}


meal_templates_headers = {
    '#': '#',
    'food_name': 'Ime',
    'food_weight': 'Masa',
    'calories': 'Kalorije',
    'fat': 'Masti',
    'saturated_fat': 'Zasićene masti',
    'carbs': 'Ugljikohidrati',
    'sugars': 'Šećeri',
    'fiber': 'Vlakna',
    'proteins': 'Bjelančevine',
    'price': 'Cijena',
    'created_on': 'Kreirano',
    'updated_on': 'Ažurirano',
}

