import re

from .base import BaseSemanticModel
from documentor.structuries.document import Document
from documentor.structuries.document import Document

from natasha import (Segmenter, MorphVocab, Doc, NewsEmbedding, NewsMorphTagger)
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk import pos_tag


class NLTKNormalization(BaseSemanticModel):

    def __init__(self):
        """
        Initialize the class for lemmatization using NLTK.
        """
        self.lemmatizer = WordNetLemmatizer()

    def __call__(self, document: Document, *args, **kwargs):
        """
        Applies lemmatization to the document's text.

        :param document: A Document object containing the text.
        :return: Lemmatized text.
        """
        tokens = word_tokenize(' '.join([fragment.value for fragment in document.build_fragments()]))

        pos_tags = pos_tag(tokens)

        lemmatized_tokens = [self.lemmatizer.lemmatize(token, self.get_wordnet_pos(pos)) for token, pos in pos_tags]

        return ' '.join(lemmatized_tokens)

    def get_wordnet_pos(self, treebank_tag):
        """
        Converts a part-of-speech tag from Penn Treebank format to WordNet format.

        :param treebank_tag: Part-of-speech tag in Penn Treebank format.
        :return: Corresponding part-of-speech tag in WordNet format.
        """
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN


class NatashaNormalization(BaseSemanticModel):
    def __init__(self, *args, **kwargs):
        """
        Initialize the NatashaNormalization class with necessary components for text normalization.
        """
        self.doc: Doc | None = None
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.word_pattern = re.compile(r'^[a-zA-Zа-яА-ЯёЁ]+$')

    def __call__(self, document: Document, *args, **kwargs):
        """
        Process and normalize the document text using Natasha's morphological tools.

        :param document: A Document object containing the text to be normalized.
        :return: The processed Doc object with tokens and lemmatized forms.
        """
        self.doc = Doc(document)

        self.doc.segment(self.segmenter)
        self.doc.tag_morph(self.morph_tagger)
        [token.lemmatize(self.morph_vocab)
         for token in self.doc.tokens]
        return self.doc
