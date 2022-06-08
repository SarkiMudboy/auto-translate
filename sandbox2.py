import re
import fileinput

footnote_pattern = re.compile(r'(\d+|\*)[\t]+([a-zA-Z]|\«)+')
footnote_index = 0
footnote_count = 0
tracking = False
data_dict = {}


def paragraph_closed(paragraph):

	reverse_index = -1
	if paragraph[reverse_index] == ' ':
		while paragraph[reverse_index] == ' ':
			reverse_index -= 1

	if paragraph[reverse_index] != '.' and paragraph[reverse_index].isalpha():
		return False

	return True


def is_discontinued(line):

	global data_dict

	character = line[0]

	if character.islower():

		last_entry = list(data_dict.keys())[-1]
		entry_paragraph = data_dict[last_entry]
		if 'footnote' not in last_entry and not paragraph_closed(entry_paragraph):
			# print(line)
			data_dict[last_entry] += ' ' + line
			return True

	return False


def print_text(data):

	with open('parsed text.txt', 'w') as f:

		for key, value in data.items():

			f.write(key + ' : ' + value + '\n')

		f.close()

def check_if_page_num(line):
	try:
		int(line)	
	except ValueError:
		return True
	return False


def convert_to_integer(integer):
	try:
		integer = int(integer)		
	except ValueError:
		return False
	return True

def check_footnotes(string):

	global footnote_index

	footnotes_integers = footnote_pattern.findall(string)
	for integer in footnotes_integers:
		integer = convert_to_integer(integer[0])
		if integer == (footnote_index+1):
			footnote_index += 1


def handle_footnotes(line):

	global footnote_index
	global footnote_count
	global tracking
	global data_dict

	split = False
	line = str(line)

	match = footnote_pattern.search(line)

	if match:
		match_text = match.group(0)
		integer = match.group(1)

		if convert_to_integer(integer) or integer == "*":

			if not tracking:
				split = True
			
		splitted_paragraph = line.split(match_text)
		remnant_string = splitted_paragraph[1]


		if split:
			footnote_count += 1
			data_dict[f'footnote{footnote_count}'] = match_text + remnant_string
			tracking = True
			return splitted_paragraph[0]

	if tracking:

		data_dict[f'footnote{footnote_count}'] += line

		return None
		
	return line


def reflow(infile):

	global data_dict
	global tracking
	paragraph_string = ''
	paragraph_count = 0

	with open(infile, 'r', errors='ignore') as source:

		for line in source.readlines():
			line = line.strip('\n')

			if line:
				# print(line[0])
				if check_if_page_num(line):	
					line = handle_footnotes(line)
					if line and not is_discontinued(line):
						data_dict[str(paragraph_count)] = line
						paragraph_count += 1
				else:
					tracking = False

		print_text(data_dict)


if __name__ == '__main__':
	infile = './tr-texts/test text.txt'
	reflow(infile)