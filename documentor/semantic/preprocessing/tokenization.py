from typing import List

from documentor.structuries.document import Document

from .base import BaseSemanticModel

from wikipedia2vec import Wikipedia2Vec


class Wiki2VecTokenization(BaseSemanticModel):
    def __init__(self, model_path: str):
        """
        Initialize the Wiki2VecTokenization class by loading the Wiki2Vec model.

        :param model_path: Path to the pre-trained Wiki2Vec model file.
        """
        self.model = Wikipedia2Vec.load(model_path)

    def __call__(self, document: Document, *args, **kwargs) -> list[list[float]]:
        """
        Convert the document into a list of vectors using the Wiki2Vec model.

        :param document: A Document object containing the text to be vectorized.
        :return: A list of vectors corresponding to each word in the document.
        """
        fragments = document.build_fragments()
        vectors = [self.get_word_vector(fragment.value) for fragment in fragments]

        return vectors

    def get_word_vector(self, word: str) -> list[float] | None:
        """
          Retrieve the vector representation of a word from the Wiki2Vec model.

          :param word: The word to convert into a vector.
          :return: The vector of the word or None if the word is not found in the model.
          """
        try:
            word_entity = self.model.get_word(word)
            if word_entity:
                return word_entity.vector.tolist()
            else:
                return None
        except KeyError:
            return None
