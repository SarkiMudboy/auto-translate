import json

def parse_to_json(dictionary, file_name):

	with open(file_name + '.json', 'w') as outfile:
		json.dump(dictionary, outfile, indent=4)
		print(f"Your file has been saved at {file_name}.json!")