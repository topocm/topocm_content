import nbformat
from nbconvert.preprocessors import Preprocessor

class HtmlLinksPreprocessor(Preprocessor):

	def preprocess_cell(self, cell, resources, index):
		if cell['cell_type'] == 'markdown':
			cell['source'] = cell['source'].replace('.ipynb','.html')
		return cell, resources