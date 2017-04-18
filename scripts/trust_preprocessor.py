import nbformat
from nbconvert.preprocessors import Preprocessor
from nbformat.sign import NotebookNotary

class TrustPreprocessor(Preprocessor):
    
    def preprocess(self, nb, resources):
        NotebookNotary().sign(nb)
        return nb, resources
