# imports the googletrans library

import googletrans
from googletrans import Translator

# gets the available languages
languages = googletrans.LANGUAGES

def translate_text(text, translator, source_language, target_language):
	'''retreives source language(sl) and target language(tl) and
	runs googletrans translate function, returns the translated text'''

	sl = [v for k, v in languages.items() if v == source_language.lower()]
	tl = [v for k, v in languages.items() if v == target_language.lower()]

	result = translator.translate(text, src=sl[0], dest=tl[0])

	return result.text
