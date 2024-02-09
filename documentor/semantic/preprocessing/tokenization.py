from semantic.models.wiki2vec import WikiWord2VecModel, BaseSemanticModel
from abstract.fragment import Fragment


def get_words_embedding(sentece: str | list[str] | Fragment, model: BaseSemanticModel):
    if isinstance(sentece, str):
        words = sentece.split()
    if isinstance(sentece, list):
        words = sentece
    if isinstance(sentece, Fragment):
        words = Fragment.data
    else:
        raise ValueError('sentence must be a string or a list of strings or Fragment')

    for word in words:
        yield model.encode(word)
