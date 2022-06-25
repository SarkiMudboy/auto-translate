# Cleans the text and saves a json file whose keys are
# the an index of each paragraph and values are the paragraph string

from scripts import parse_to_json, parse_other_json


paragraph_count = 0
paragraph_dict = {}

append_paragraph = {
	'append': False,
	'spaced': False
}


def fetch_last_character(paragraph):
	'''get the last character in a paragraph and returns
	a tuple of the last character and its index in the 
	string'''
	
	reverse_index = -1
	if paragraph[reverse_index] == ' ':
		while paragraph[reverse_index] == ' ':
			reverse_index -= 1

	return paragraph[reverse_index], reverse_index

def check_discontinuation(paragraph):

	'''checks the paragraph string to see if it is deprecated'''

	global append_paragraph

	append_paragraph={'append':False,'spaced':False}

	last_character, index = fetch_last_character(paragraph)

	# if the last character is not a fullstop, it is assumed
	# to be discontinued

	if last_character != '.':

		paragraph = handle_discontinued_paragraphs(paragraph, last_character, index)

	return paragraph


def handle_discontinued_paragraphs(paragraph, last_character, character_index):

	'''checks what type of discontinuity and prepares the next
	paragraph string for cleaning, returns the paragraph string 
	without (-) if the paragraph is deprecated in-word'''

	global append_paragraph

	if last_character and last_character == '-':

		paragraph = paragraph[:character_index]

		append_paragraph['append'] = True
		append_paragraph['spaced'] = False

	else:

		append_paragraph['append'] = True
		append_paragraph['spaced'] = True

	return paragraph


def clean_paragraph(paragraph):
	'''checks and clean each paragraph, returns
	True or False depending on whether the paragraph
	was cleaned'''

	global paragraph_dict

	cleaned = False
	spaced = append_paragraph['spaced']

	append = append_paragraph['append']

	# checks for discontinuation
	paragraph = check_discontinuation(paragraph)

	# if previous paragraph is deprecated, the current paragraph is 
	# appended to the previous dictionary entry

	if append:

		# appends the paragraph with or without a (space)
		# depending whether how the previous paragraph was
		# discontinued

		if spaced:
			paragraph_dict[str(paragraph_count)] += (" " + paragraph)
		else:
			paragraph_dict[str(paragraph_count)] += paragraph

		cleaned = True

	return cleaned


def check_if_page_num(line):

	'''returns True if the line is an integer
	i.e a page number, else returns False'''

	try:
		int(line)	
	except ValueError:
		return False
	return True


def clean_text(infile, language):

	'''opens the text file, reads in line by line
	and checks them for discontinuities'''

	global paragraph_dict
	global paragraph_count

	with open(infile, 'r', errors='ignore') as source:

		for line in source.readlines():

			# strip line of newlines
			paragraph = line.strip('\n')

			# if paragraph is not a page number or an empty string

			if paragraph and not check_if_page_num(paragraph):

				# clean it, if not cleaned, add it normally...
				if not clean_paragraph(paragraph):

					# increases the paragraph index count and adds it to the
					# paragraph dictionary
					paragraph_count += 1
					paragraph_dict[str(paragraph_count)] = paragraph

		# parses the dictionary to a json file
		parsed = parse_to_json(paragraph_dict, language)
		if not parsed:
			parse_other_json(paragraph_dict, language)

		# returns the filename
		return f'{language}.json'

