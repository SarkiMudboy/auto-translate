# encoding: utf-8

from docx import Document

class Doc:

	def __init__(self):
		self.document = Document()

	def get_doc(self):
		return self.document

	def create_table(self):
		self.table = self.document.add_table(rows=0, cols=2, style='Table Grid')
		return self.table

	def add_to_table(self, lang_text, trans):
		data_row = self.table.add_row().cells

		data_row[0].text = lang_text
		data_row[1].text = trans

	def save(self, filename):

		# save to file
		self.document.save(f"{filename}.docx")






