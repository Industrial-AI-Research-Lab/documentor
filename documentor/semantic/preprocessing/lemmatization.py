from documentor.structuries.document import Document




def lemmatize(document: Document, *args, **kwargs):
    """
    Lemmatize text
    :param text:
    :type text: str
    :return: list of lemmatized words
    :rtype: list
    """

    for fragment in document.build_fragments():
        doc = Doc(fragment.data)
        doc.segment(segmenter)
        doc.tag_morph(morph_tag)

        for token in doc.tokens:
            token.lemmatize(morph_vocab)

        fragment.lemmas = [word.lemma for word in doc.tokens if word_pattern.match(word.lemma)]
