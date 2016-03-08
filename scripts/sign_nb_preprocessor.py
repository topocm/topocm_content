import nbformat
from nbconvert.preprocessors import Preprocessor
from nbformat.sign import NotebookNotary

class SignNBPreprocessor(Preprocessor):
    
    def preprocess(self, nb, resources):
    	if not NotebookNotary().check_signature(nb):
    		# If notebook is not signed (trusted), sign it.
    		NotebookNotary().sign(nb)
    	return nb, resources
