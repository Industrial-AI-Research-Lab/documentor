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

    def encode_word(self, word: str, *args, **kwargs) -> np.ndarray | None:
        """
        encode word to vector
        :param word: word to encode
        :type word: str
        :return: vector if word has been found, else None
        :rtype: np.ndarray or None
        """
        try:
            return self._model.get_word_vector(word)
        except KeyError:
            return None
