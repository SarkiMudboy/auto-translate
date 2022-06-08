import re
import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

paragraph_count = 0
data_dict = {}
append_line = {
	'append': False,
	'spaced': False,
	'index': None
}
tracking = False
footnote_count = 0


def print_text(data):

	with open('german parsed text.txt', 'w') as f:

		for key, value in data.items():

			f.write(key + ' : ' + value + '\n')

		f.close()

def is_roman_number(num):

    pattern = re.compile(r"""   
                                ^M{0,3}
                                (CM|CD|D?C{0,3})?
                                (XC|XL|L?X{0,3})?
                                (IX|IV|V?I{0,3})?$
            """, re.VERBOSE)

    if re.match(pattern, num):
        return True

    return False


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

	global footnote_count
	global tracking

	stripped_line = line.strip(' ')
	if is_roman_number(stripped_line):
		tracking = False
		return True
	else:

		first_character, _ = crawl_spaces(line, pos='start')

		if tracking:
			last_character, index = crawl_spaces(line)
			if last_character == '-':
				line = line[:index]
				data_dict[f'footnote{footnote_count}'] += line
			else:
				data_dict[f'footnote{footnote_count}'] += ' ' + line
			return True

		elif first_character == '•' or first_character == '"':
			if not tracking:
				footnote_count += 1
				data_dict[f'footnote{footnote_count}'] = line
				tracking = True

			return True

	return False



def clean_up(line):

	global data_dict
	global append_line

	append = False



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

	if last_character == '-' or last_character != '.':

		if last_character == '-':
			append_line['spaced'] = False
			append_line['index'] = index
		elif last_character.islower():
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

	global paragraph_count
	global data_dict

	# with open(infile) as file:
	with open(infile, 'r', errors='ignore', encoding='utf-8') as source:
		for line in source.readlines():
			line = line.strip('\n')
			if line != '':
				if not handle_footnotes(line):
					cleaned = clean_up(line)
					if not cleaned:
						data_dict[str(paragraph_count)] = line
						paragraph_count += 1
		# print_text(data_dict)
		for key, value in data_dict.items():
			print(key + ': ' + value)


if __name__ == '__main__':
	infile = './tr-texts/Kritzman Die heroische Periode der grossen russischen Revolution TXT 1.txt'
	parse_text(infile)