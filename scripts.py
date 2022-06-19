import json

def parse_to_json(dictionary, file_name):

	outfile = open(file_name + '.json', 'w')
	success = True

	try:
		json.dump(dictionary, outfile, indent=4, ensure_ascii=False)
	except UnicodeEncodeError:
		success = False

	if success:
		print(f"Your file has been saved at {file_name}.json!")

	return success
		
	


def parse_other_json(dictionary, file_name):

	print('other one running....')	
	outfile = open(file_name + '.json', 'w')

	json.dump(dictionary, outfile, indent=4)
		
	print(f"Your file has been saved at {file_name}.json!")

