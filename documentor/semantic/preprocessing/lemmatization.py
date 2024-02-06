from natasha import (Segmenter, MorphVocab, Doc)


segmenter = Segmenter()
morph_vocab = MorphVocab()


class Lemmatizer:
    """
    Text preprocessing handler.
    """

    @staticmethod
    def lemmatize(text, *args, **kwargs):
        """
        Lemmatize text
        :param text:
        :type text: str
        :return: list of lemmatized words
        :rtype: list
        """
        doc = Doc(text)
        doc.segment(segmenter)
        doc.tag_set(morph_vocab)
        for token in doc.tokens:
            token.lemmatize(morph_vocab)

        return [word.lemma for word in doc.tokens]
