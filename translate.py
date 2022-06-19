import googletrans
from googletrans import Translator

languages = googletrans.LANGUAGES
# print(languages)

def translate_text(text, translator, source_language, target_language):

	sl = [v for k, v in languages.items() if v == source_language.lower()]
	tl = [v for k, v in languages.items() if v == target_language.lower()]

	result = translator.translate(text, src=sl[0], dest=tl[0])

	return result.text
