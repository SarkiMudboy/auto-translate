import json
import translate
from translate import translate_text
from googletrans import Translator
from handle_word import Doc
from json.decoder import JSONDecodeError 

paragraph_count = 0
data_dict = {}

def split_dict(test_dict, start):

	length = 500

	stop = start + length

	dict_list = list(test_dict.items())

	start_index = None
	stop_index = None

	for index, tup in enumerate(dict_list):
		if str(start) == tup[0]:
			start_index = index
		elif str(stop) == tup[0]:
			stop_index = index

	dict_chunk = dict(dict_list[start_index:stop_index])

	return dict_chunk


def handle_lengthy_text(text_string):

	n = 5000

	if len(text_string) > n:

		chunks = [text_string[i:i+n] for i in range(0, len(text_string), n)]
		
		return chunks

	return False

def handle_translation(text, translator, source_lang, target_lang, doc):

	global data_dict, paragraph_count

	translated_text = translate_text(text, translator, source_lang, target_lang)

	doc.add_to_table(text, translated_text)

	data_dict[str(paragraph_count)] = [text, translated_text]
	paragraph_count += 1

	return doc

def test(lang_file):
	with open(lang_file) as json_file:
		data = json.load(json_file)

		return data


def automate(lang_file):

	global paragraph_count, data_dict

	output = {}
	output_document = Doc()
	table = output_document.create_table()
	
	with open(lang_file, 'r', encoding='utf-8', errors='ignore') as json_file:

		try:
			data = json.load(json_file)
		except JSONDecodeError:
			data = test(lang_file)

		data = split_dict(data, 500)

		translator = Translator()

		for key, text in data.items():
		
			chunks = handle_lengthy_text(text)

			if chunks:

				for chunk in chunks:

					output_document = handle_translation(chunk, translator, 'french', 'english', output_document)
			else:

				output_document = handle_translation(text, translator, 'french', 'english', output_document)
			

		output_document.save('trans_french_02')
		print('document saved!')

automate('french.json')






