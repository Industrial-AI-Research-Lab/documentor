import re

import numpy as np

from documentor.semantic.models.base import BaseSemanticModel

from natasha import (Segmenter, MorphVocab, Doc, NewsEmbedding, NewsMorphTagger)


class NatashaSemanticModel(BaseSemanticModel):
    """Class for lemmatize and stemming using natasha"""

    def __init__(self, model=None):
        """
        Initialize ancillary elements such as segmenter, morphVocab,
        morph tag and word patternt
        """
        super(NatashaSemanticModel, self).__init__()

        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        emb = NewsEmbedding()
        self.morph_tag = NewsMorphTagger(emb)
        self.word_pattern = re.compile(r'^[a-zA-Zа-яА-ЯёЁ]+$')

    def encode(self, data: str, *args, **kwargs) -> list[str] | str:
        """
        Method for lemmatize word or statement
        :param data: statement for lemmatize
        :type data: str
        :param args:
        :param kwargs:
        :return:
        """
        doc = Doc(data)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tag)

        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)

        result = [word.lemma for word in doc.tokens if self.word_pattern.match(word.lemma)]
        return result

    def encode_text(self, text: str, *args, **kwargs) -> list[str] | str:
        """
        Method for lemmatize text with several words
        :param text:
        :param args:
        :param kwargs:
        :return:
        """
        return self.encode(text)

    def encode_word(self, word: str, *args, **kwargs) -> str:
        """
        Method for lemmatize single word
        :param word:
        :param args:
        :param kwargs:
        :return:
        """
        return self.encode(word)
