import re

footnote_pattern = re.compile(r'(\d+|\*)[\t]+[a-zA-Z«]+')
footnote_index = 1622
footnote_count = 0
tracking = False
data_dict = {}

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
		pass
	return integer

def check_footnotes(string):

	global footnote_index

	footnotes_integers = footnote_pattern.findall(string)
	for integer in footnotes_integers:
		integer = convert_to_integer(integer)
		if integer == (footnote_index+1):
			footnote_index += 1


def handle_footnotes(line):

	global footnote_index
	global footnote_count
	global tracking
	global data_dict

	split = False

	match = footnote_pattern.search(line)

	if match:
		match_text = match.group(0)
		integer = match.group(1)
		integer = convert_to_integer(integer)

		if integer == (footnote_index+1) or integer == "*":

			if integer == (footnote_index+1):
				footnote_index += 1
			if not tracking:
				split = True
			
		splitted_paragraph = line.split(match_text)
		remnant_string = splitted_paragraph[1]
		check_footnotes(remnant_string)

		if split:
			footnote_count += 1
			data_dict[f'footnote{footnote_count}'] = match_text + remnant_string
			tracking = True
			return splitted_paragraph[0]
		elif tracking:
			data_dict[f'footnote{footnote_count}'] += line
			return None
		
	return line


def reflow(infile):

	paragraph_string = ''
	paragraph_count = 0

	with open(infile) as source:

		for line in source.readlines():
			line = line.strip('\n')
			if check_if_page_num(line):	
				line = handle_footnotes(line)
				if line:
					data_dict[str(paragraph_count)] = line
					paragraph_count += 1
			else:
				tracking = False

	print(data_dict)


if __name__ == '__main__':
	infile = './tr-texts/test text.txt'
	reflow(infile)