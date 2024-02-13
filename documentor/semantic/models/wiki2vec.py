from documentor.semantic.models.base import BaseSemanticModel
import numpy as np

from wikipedia2vec import Wikipedia2Vec


class WikiWord2VecModel(BaseSemanticModel):
    """
    Represent a wikiword2vec model interface
    """
    def __init__(self):
        super(WikiWord2VecModel, self).__init__()

    def load_weights(self, path, *args, **kwargs):
        """
        Load weights from given path and initialize model
        :param path: path to weights file
        :type path: str
        """
        self.model = Wikipedia2Vec.load(path)

    def encode(self, X: str, *args, **kwargs) -> np.ndarray:
        """
        encode word to vector
        :param X: word to encode
        :type X: str
        :return: vector
        :rtype: np.ndarray
        """
        return self.model.get_word_vector(X)

