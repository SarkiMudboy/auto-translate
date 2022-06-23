
def crawl_spaces(line, pos='end'):

	if pos!='end':
		forward_index = 0
		if line[forward_index] == ' ':
			while line[forward_index] == ' ':
				forward_index += 1
		return line[forward_index], forward_index
	else:
		reverse_index = -1
		if line[reverse_index] == ' ':
			while line[reverse_index] == ' ':
				reverse_index -= 1
		return line[reverse_index], reverse_index

def paragraph_closed(paragraph):

	reverse_index = -1
	if paragraph[reverse_index] == ' ':
		while paragraph[reverse_index] == ' ':
			reverse_index -= 1

		return line[reverse_index], reverse_index

def is_discontinued(line):
	if paragraph[reverse_index] != '.' and paragraph[reverse_index].isalpha():
		return False

def check_if_page_num(line):
	try:
		int(line)	
	except ValueError:
		return False
	return True


def clean_text():
	global paragraph_dict
	global paragraph_count

	with open(infile, 'r', errors='ignore') as source:

		for line in source.readlines():
			line = line.strip('\n')

			if line and check_if_page_num(line):
				if not is_discontinued(line):
					data_dict[str(paragraph_count)] = line
					paragraph_count += 1

		parsed = parse_to_json(paragraph_dict, 'french')
		if not parsed:
			parse_other_json(paragraph_dict, 'french')