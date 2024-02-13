from natasha import (Segmenter, MorphVocab, Doc)
from documentor.abstract.document import Document

segmenter = Segmenter()
morph_vocab = MorphVocab()


def lemmatize(document: Document, *args, **kwargs):
    """
    Lemmatize text
    :param text:
    :type text: str
    :return: list of lemmatized words
    :rtype: list
    """

    for fragment in document.fragments:
        doc = Doc(fragment.data)
        doc.segment(segmenter)
        doc.tag_set(morph_vocab)

        for token in doc.tokens:
            token.lemmatize(morph_vocab)

        fragment.lemas = [word.lemma for word in doc.tokens]
