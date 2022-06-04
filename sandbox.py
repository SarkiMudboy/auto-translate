import pdf2txt
import os

footnote_index = None
track_footnote = False
footnote = ''
current_page_num = ''


def check_if_page_num(line):
	try:
		int(line)		
	except ValueError:
		return True
	return False

def handle_footnotes(line):
	if track_footnote:
		footnote_array = line.split('.')
		print(footnote_array)

def check_footnote(line):

	global footnote_index

	if track_footnote:
		index=0
		if line[index] == ' ':
			while line[index] == ' ':
				index += 1

		if line[index] == '*':
			print('its asterisk')
			return True

		try:
			integer = int(line[index])
			print('its a num!')
		except ValueError:
			return False

		if integer == (footnote_index + 1):
			footnote_index = index
			return True

	return False



def check_breaks(line):
	if not line.endswith('.'):
		end_chars = ['.', '»', ':'] # write regex to det letter
		reverse_index = -1
		last_character = line[reverse_index]

		if last_character == ' ':
			while last_character == ' ':
				reverse_index -= 1
				last_character = line[reverse_index]

		if last_character not in end_chars:
			return True
	return False

def reflow(infile):

	global track_footnote

	data_dict = {}
	paragraph_string = ''
	paragraph_count = 0

	with open(infile) as source:

		for line in source.readlines():
			line = line.strip('\n')

			if not track_footnote:
				if line != '' and check_if_page_num(line):

					track_footnote = check_breaks(line)
					if track_footnote:
						checked = check_footnote(line)
						if not checked:
							pass
						else: handle_footnotes(line)

					# handle perfect footnote paragraph and check for hidden footnotes
					data_dict[str(paragraph_count)] = line
					paragraph_count += 1
					# print('>>>',line)
			else:
				if line != '' and check_if_page_num(line):
					print('>>>',line)
					opp = line
				if not check_if_page_num(line):
					track_footnote = False

		# print(data_dict)
		# print('footnotes: ', footnote)
		# print(data_dict['2'])

if __name__ == '__main__':
	infile = './tr-texts/test text.txt'
	reflow(infile)