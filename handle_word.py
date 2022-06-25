# encoding: utf-8

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Inches

class Doc:
	'''Document Class'''

	def __init__(self):

		'''initializes the document'''

		self.document = Document()
		self.object_width = None
		self.change_orientation()

	def get_doc(self):
		'''returns the document instance'''
		return self.document

	def create_table(self):
		'''creates a document table with two columns'''
		self.table = self.document.add_table(rows=0, cols=2, style='Table Grid')
		return self.table

	def add_to_table(self, lang_text, trans):
		'''add data to table'''
		
		data_row = self.table.add_row().cells

		'''adjusts the table width (wide) to fit the 
		landscape mode'''
		self.set_table_width()

		'''adds the text and its translation to the table cells'''
		data_row[0].text = lang_text
		data_row[1].text = trans

	def save(self, filename):

		# save to file
		self.document.save(f"{filename}.docx")

	def change_orientation(self):
		'''changes orientation to landscape'''

		for index in range(len(self.document.sections)):

			section = self.document.sections[index]
			new_height, new_width = section.page_height, section.page_width
			section.orientation = WD_ORIENT.LANDSCAPE
			section.page_width = new_height
			section.page_height = new_width
			self.object_width = (section.page_width / 2)

	def set_table_width(self):
		'''sets the table width'''
		for cell in self.table.rows[-1].cells:
			cell.width = self.object_width







