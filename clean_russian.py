import re
from scripts import parse_to_json, parse_other_json

crylic_pattern = re.compile(r'[\u0400-\u04FF]')
footnote_pattern = re.compile(r'^[•|*]+[\s]*(-|•)')
broken_word_pattern = re.compile(r"[\u0400-\u04FF][­][\s][\u0400-\u04FF]")

data_dict = dict()
paragraph_count = 0
footnote_count = 0
tracking = False

append_line = {
	'append': False,
	'spaced':False,
	'index': None
	}

def handle_broken_words(line):
	match = broken_word_pattern.findall(line)
	if match:
		for word in match:
			resewn_word = word.replace('­ ', '')
			line = line.replace(word, resewn_word)
	return line

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

def handle_footnotes(line):

	global paragraph_count, footnote_count, tracking, data_dict

	match = footnote_pattern.search(line)
	last_character, index = crawl_spaces(line)
	char_match = crylic_pattern.search(last_character)
	end_char = ['-', ',']

	if last_character in end_char:
		if last_character == '-':
			line = line[:index]

	line = handle_broken_words(line)

	if tracking:

		if not char_match:
			tracking = False

		data_dict[f'footnote{footnote_count}'] += line

		return True

	if match:

		tracking = True

		if not char_match:
			tracking = False

		footnote_count += 1
		data_dict[f'footnote{footnote_count}'] = line

		return True

	return False


def clean_text(line):

	global data_dict
	global append_line

	append = False

	line = handle_broken_words(line)

	if append_line['append'] and paragraph_count > 0:

		last_entry = list(data_dict.keys())[-1]

		if 'footnote' in last_entry:
			last_entry = list(data_dict.keys())[-2]

		if append_line['spaced']:
			data_dict[last_entry] += ' ' + line
		else:
			hyphen_index = append_line['index']
			data_dict[last_entry] = data_dict[last_entry][:hyphen_index]
			data_dict[last_entry] += line
		append = True   

	last_character, index = crawl_spaces(line)
	match = crylic_pattern.search(last_character)

	if last_character == '-' or last_character != '.':

		if last_character == '-':
			append_line['spaced'] = False
			append_line['index'] = index
		elif match:
			append_line['spaced'] = True
			append_line['index'] = None

		append_line['append'] = True

	else:
		append_line = {
		'append': False,
		'spaced':False,
		'index': None
		}

	return append


def parse_text(infile):

	global paragraph_count, data_dict

	with open(infile, 'r', encoding="utf-8") as source:

		for line in source.readlines():
			line = line.strip('\n')

			if line != '' and not handle_footnotes(line):

				if not clean_text(line):
					line = handle_broken_words(line)
					data_dict[str(paragraph_count)] = line
					paragraph_count += 1

		parsed = parse_to_json(data_dict, 'russian')
		if not parsed:
			parse_other_json(data_dict, 'russian')

if __name__ == '__main__':
	infile = './tr-texts/Nevsky no pages numbers.txt'
	parse_text(infile)