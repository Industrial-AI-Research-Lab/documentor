from semantic.models.wiki2vec import WikiWord2VecModel, BaseSemanticModel
from structuries.fragment import Fragment
from structuries.document import Document


def tokenize(document: Document, model: BaseSemanticModel):

    for fragment in document.build_fragments():
        fragment.tokens = [model.encode(word) for word in fragment.data]
