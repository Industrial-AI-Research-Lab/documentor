import re

import numpy as np

from semantic.models.base import BaseSemanticModel

from natasha import (Segmenter, MorphVocab, Doc, NewsEmbedding, NewsMorphTagger)


class NatashaSemanticModel(BaseSemanticModel):
    """Class for lemmatize and stemming using natasha"""

    def __init__(self):
        """
        Initialize ancillary elements such as segmenter, morphVocab,
        morph tag and word patternt
        """

        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        emb = NewsEmbedding()
        self.morph_tag = NewsMorphTagger(emb)
        self.word_pattern = re.compile(r'^[a-zA-Zа-яА-ЯёЁ]+$')

    def load_weights(self, path):
        ...

    def encode(self, X: str, *args, **kwargs) -> list[str]:
        """
        Method for lemmatize word in statmment X
        :param X: statement for lemmatize
        :type X: str
        :param args:
        :param kwargs:
        :return:
        """
        doc = Doc(X)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tag)

        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)

        return [word.lemma for word in doc.tokens if self.word_pattern.match(word.lemma)]

