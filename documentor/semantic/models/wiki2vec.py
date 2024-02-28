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
        self._model = Wikipedia2Vec.load(path)

    def encode(self, X: str, *args, **kwargs) -> np.ndarray | None:
        """
        encode word to vector
        :param X: word to encode
        :type X: str
        :return: vector if word has been found, else None
        :rtype: np.ndarray or None
        """
        try:
            return self._model.get_word_vector(X)
        except KeyError:
            return None
