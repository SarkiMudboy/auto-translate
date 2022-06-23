import json
import time
import translate
from translate import translate_text
from googletrans import Translator
from handle_word import Doc
from json.decoder import JSONDecodeError
from itertools import islice 

paragraph_count = 0
language_data_dict = {}

def split_dict(data, SIZE=500):

    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}


def handle_lengthy_text(text_string):

	n = 5000

	if len(text_string) > n:

		chunks = [text_string[i:i+n] for i in range(0, len(text_string), n)]
		
		return chunks

	return False

def handle_translation(text, translator, source_lang, target_lang, doc):

	global language_data_dict, paragraph_count

	translated_text = translate_text(text, translator, source_lang, target_lang)

	doc.add_to_table(text, translated_text)

	language_data_dict[str(paragraph_count)] = [text, translated_text]
	paragraph_count += 1

	return doc

def test(lang_file):
	with open(lang_file) as json_file:
		data = json.load(json_file)

		return data


def automate(language_json_file):

	global paragraph_count, language_data_dict

	output = {}
	output_document = Doc()
	table = output_document.create_table()

	chunk_loop_count = 2
	
	with open(language_json_file, 'r', encoding='utf-8', errors='ignore') as json_file:

		try:
			extracted_data = json.load(json_file)
		except JSONDecodeError:
			extracted_data = test(language_json_file)

		dict_chunk_list = []

		for dict_chunk in split_dict(extracted_data):

			dict_chunk_list.append(dict_chunk)

		for chunk_to_tranlate in dict_chunk_list:

			translator = Translator()

			for key, text in chunk_to_tranlate.items():

				if text:
				
					chunks = handle_lengthy_text(text)

					if chunks:

						for chunk in chunks:

							output_document = handle_translation(chunk, translator, 'german', 'english', output_document)
					else:

						output_document = handle_translation(text, translator, 'german', 'english', output_document)
				

			output_document.save('trans_german_0'+str(chunk_loop_count))
			print('document saved!')

			output_document = Doc()
			table = output_document.create_table()

			chunk_loop_count += 1
			time.sleep(5 * 60)

automate('german-02.json')






