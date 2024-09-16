from .base import BaseSemanticModel
from documentor.structuries.document import Document

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsNERTagger,
    NewsSyntaxParser
)
from pymorphy2 import MorphAnalyzer as PymorphyAnalyzer
from razdel import tokenize
import pandas as pd


class NatashaSpellChecker(BaseSemanticModel):
    def __init__(self):
        """
        Initialize necessary components of Natasha for spell checking.
        """
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        self.pymorphy_analyzer = PymorphyAnalyzer()

    def __call__(self, document: Document, *args, **kwargs) -> Document:
        """
        Checks the spelling of the document text and suggests corrections.

        :param document: A Document object containing the text.
        :return: Corrected text.
        """
        corrected_text = []

        tokens = tokenize(document.build_fragments())

        for token in tokens:
            word = token.text
            if not self.is_correct(word):
                correction = self.get_correction(word)
                if correction:
                    corrected_text.append(correction)
                else:
                    corrected_text.append(word)
            else:
                corrected_text.append(word)

        return Document(pd.DataFrame(corrected_text))

    def is_correct(self, word: str) -> bool:
        """
        Checks if the word is spelled correctly.

        :param word: The word to check.
        :return: True if the word is correct, otherwise False.
        """
        parsed_word = self.pymorphy_analyzer.parse(word)
        for parse in parsed_word:
            if parse.is_known:
                return True
        return False

    def get_correction(self, word: str) -> str:
        """
        Returns the most likely correction for the given word.

        :param word: The word to correct.
        :return: The corrected word.
        """
        suggestions = self.pymorphy_analyzer.parse(word)
        if suggestions:
            best_suggestion = suggestions[0]
            return best_suggestion.normal_form
        return word
