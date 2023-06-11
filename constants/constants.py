"""General constants module for ranah app

If the app grows larger, it'd probably make sense to split
this module into several modules within a (sub)package
"""

# TODO: clean this file up a bit, some names are misleading,
# also back-patching definitions should have same type for both Canvas

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