import re

from .base import BaseEstimator
from documentor.structuries.document import Document
from natasha import (Segmenter, MorphVocab, Doc, NewsEmbedding, NewsMorphTagger)


class NatashaEstimator(BaseEstimator):
    """
    Class wrapper for natasha language library
    """

    def __init__(self, *args, **kwargs):
        self.doc: Doc | None = None
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.word_pattern = re.compile(r'^[a-zA-Zа-яА-ЯёЁ]+$')

    def normalization(self, target: Document, *args, **kwargs) -> :
        self.doc = Doc(target)

        self.doc.segment(self.segmenter)
        self.doc.tag_morph(self.morph_tagger)
        lemmas = [token.lemmatize(self.morph_vocab)
                  for token in self.doc.tokens]


    def __call__(self, target: Document, *args, **kwargs):
        self.doc = Doc(Document.value)
