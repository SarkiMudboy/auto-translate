'''Obtains filepath and file language and runs the clean
and automate scripts'''

import fix
import json
from automate import automate


if __name__ == '__main__':

	# asks for filepath and file language
	filepath = input('Enter file path: ')

	language = input('File language: ')

	# cleans the file to prepare it for translation

	print('cleaning...')
	parsed_json_file = fix.clean_text(filepath, language)

	# translate
	print('translating...')
	automate(parsed_json_file, language)
