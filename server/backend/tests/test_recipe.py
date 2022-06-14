import requests

BASE = "http://127.0.0.1:5000/"

recipe = {
    'email': 'rion@example.com',
    'title': "Nether dip",
    'provenance': "Rion's cursed spellbook",
    'ingredients': [
        {
			'name': 'Soy sauce',
			'properties': {
				'quantity_numerator': 1,
				'quantity_denominator': 1,
				'unit': 'gr',
				'prep': 'Bottled'
			}
		},
        {
			'name': 'Ketchup',
			'properties': {
				'quantity_numerator': 1,
				'quantity_denominator': 1,
				'unit': 'gr',
				'prep': 'Bottled'
			}
		}
	],
    'instructions': ['Mix everything together.', 'Eat with doritos.']
}
print(recipe)
response = requests.post(BASE + "addrecipe", json=recipe)
print(response.json())