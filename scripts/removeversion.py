import nbformat
from nbconvert.preprocessors import Preprocessor

class RemoveVersionPreprocessor(Preprocessor):
    
    def preprocess(self, nb, resources):
    	if 'version' in nb.metadata['language_info']:
    		del nb.metadata['language_info']['version']
    	return nb, resources
