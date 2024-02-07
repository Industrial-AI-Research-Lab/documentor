from wikipedia2vec import Wikipedia2Vec


class Wiki2VecModel:
    model: Wikipedia2Vec

    def __init__(self, path, *args, **kwargs):
        self.model = Wikipedia2Vec.load(path)

    def vectorize(self, word):
        return self.model.get_word_vector(word)
