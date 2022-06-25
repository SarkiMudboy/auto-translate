'''Handles translation automation'''

import sys
import json
import time
import translate
from translate import translate_text
from googletrans import Translator
from handle_word import Doc
from json.decoder import JSONDecodeError
from itertools import islice 

# instantiates the lang dict
paragraph_count = 0
language_data_dict = {}

# list of untranslated dictionary chunks
text_to_translate = []

# overall list
dcl = []



def split_dict(data, SIZE=500):
	'''splits dictionary into 500 elements'''

	it = iter(data)
	for i in range(0, len(data), SIZE):
		yield {k:data[k] for k in islice(it, SIZE)}


def handle_lengthy_text(text_string):
	'''splits the text into 500 words, returns splitted chunks
	if length is longer than n, else return False'''

	n = 5000

	if len(text_string) > n:

		chunks = [text_string[i:i+n] for i in range(0, len(text_string), n)]
		
		return chunks

	return False

def handle_translation(text, translator, source_lang, target_lang, doc):
	'''handles translation and table filling, returns the doc'''

	global language_data_dict, paragraph_count

	# translate
	translated_text = translate_text(text, translator, source_lang, target_lang)

	# add texts to table
	doc.add_to_table(text, translated_text)

	language_data_dict[str(paragraph_count)] = [text, translated_text]
	paragraph_count += 1

	return doc

def test(lang_file):
	'''opens json file without utf-8 encoding, return '''
	with open(lang_file) as json_file:
		data = json.load(json_file)

		return data


def translate_paragraph_texts(chunk_to_tranlate, translator, output_document, language):

	global text_to_translate, dcl

	# iterates the dictionary, retreives each paragraph
	for key, text in chunk_to_tranlate.items():

		if text:

			# spilts lenghty texts into chunks to prevent overloading the translate
			# function, else translate full text
		
			chunks = handle_lengthy_text(text)

			if chunks:

				for chunk in chunks:

					output_document = handle_translation(chunk, translator, language, 'english', output_document)
			else:

				output_document = handle_translation(text, translator, language, 'english', output_document)

	# removes the translated text from texts to be translated
	text_to_translate.remove(chunk_to_tranlate)

	# return the doc
	return output_document


def automate(language_json_file, language):
	'''opens the json file, parse to a python dictionary,
	translates each text, creates and fills up the word doc'''

	global paragraph_count, language_data_dict, text_to_translate

	# instantiates the word document

	output = {}
	output_document = Doc()
	table = output_document.create_table()

	chunk_loop_count = 1
	trials = 0
	
	# open file
	with open(language_json_file, 'r', encoding='utf-8', errors='ignore') as json_file:

		# parse json file into a python dictionary,
		# if a decoding error occurs, reopen the file
		# without enforcing utf-8 encoding

		try:
			extracted_data = json.load(json_file)
		except JSONDecodeError:
			extracted_data = test(language_json_file)

		dict_chunk_list = []

		# splits the dictionary into smaller dictionaries
		for dict_chunk in split_dict(extracted_data):

			dict_chunk_list.append(dict_chunk)

		# sets the overall dictionary list
		text_to_translate = dict_chunk_list[:]

		# iterates over each dict in the chunk list
		for chunk_to_tranlate in dict_chunk_list:

			# initiates the translator class
			translator = Translator()

			'''translates each chunk, if an error occurs it will attempt 4 more
			trials'''
			while text_to_translate and trials < 4:

				try:

					output_document = translate_paragraph_texts(chunk_to_tranlate, translator,
					output_document, language)

				except Exception as e:
					trials += 1
					print('An exception occured: ' + str(e),' Retrying...')
					continue

				trials = 0
				break

			# if chunk translation success...

			if trials == 0:

				# saves the file
				trans_filename = f'trans_{language}_0{str(chunk_loop_count)}'
				output_document.save(trans_filename)
				print(f'{trans_filename} saved!')

				# creates a new document
				output_document = Doc()
				table = output_document.create_table()

				# increases the loop count and delays script for 2 minutes
				chunk_loop_count += 1
				time.sleep(2 * 60)

			else:

				# if not success, stop the script
				break


if __name__ == '__main__':

	source_file = None

	# if script is called from the terminal, 
	# check if extra parameter json file name
	# is provided, else prompt user for filename.

	if len(sys.argv) > 1:
		source_file = sys.argv[1]
	else:
		print("enter the json file name...")

	# if file is provided run automation script
	if source_file:
		lang = source_file.split('.')[0]
		automate(source_file, lang)





