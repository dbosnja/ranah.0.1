"""General constants module for ranah app

If the app grows larger, it'd probably make sense to split
this module into several modules within a (sub)package
"""

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

