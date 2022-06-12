import json
import translate
from translate import translate_text
from googletrans import Translator

paragraph_count = 0
data_dict = {}

def automate(lang_file):

	global paragraph_count, data_dict

	output = {}
	
	with open(lang_file) as json_file:
		data = json.load(json_file)

		translator = Translator()
		for key, text in data.items():

			translated_text = translate_text(text, translator, 'french', 'english')
			print(translated_text)
			data_dict[str(paragraph_count)] = translated_text
			paragraph_count += 1

		# print(data_dict)

automate('results.json')





