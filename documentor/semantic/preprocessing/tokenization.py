from semantic.models.wiki2vec import WikiWord2VecModel, BaseSemanticModel
from abstract.fragment import Fragment
from abstract.document import Document


def tokenize(document: Document, model: BaseSemanticModel):

    for fragment in document.fragments:
        fragment.tokens = [model.encode(word) for word in fragment.data]

