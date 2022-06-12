import json

def parse_to_json(dictionary):

	with open('results.json', 'w') as outfile:
		json.dump(dictionary, outfile, indent=4)
		print("Your file has been saved at results.json!")