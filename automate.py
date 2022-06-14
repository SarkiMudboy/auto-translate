import json
import translate
from translate import translate_text
from googletrans import Translator
from handle_word import Doc

paragraph_count = 0
data_dict = {}

def automate(lang_file):

	global paragraph_count, data_dict

	output = {}
	output_document = Doc()
	table = output_document.create_table()
	
	with open(lang_file) as json_file:
		data = json.load(json_file)

		translator = Translator()
		for key, text in data.items():

			translated_text = translate_text(text, translator, 'russian', 'english')

			output_document.add_to_table(text, translated_text)

			data_dict[str(paragraph_count)] = [text, translated_text]
			paragraph_count += 1

			if key == '188':
				break

		output_document.save('trans-russian')
		# print(data_dict)

automate('russian.json')





