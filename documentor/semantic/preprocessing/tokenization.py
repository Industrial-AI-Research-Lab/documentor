from documentor.semantic.models.wiki2vec import WikiWord2VecModel, BaseSemanticModel
from documentor.structuries.fragment import Fragment
from documentor.structuries.document import Document


def tokenize(document: Document, model: BaseSemanticModel):
    """
    Get embeddings from document via model
    :param document: Document for tokenization
    :param model: Embedding model
    :return: None
    """
    for fragment in document.build_fragments():
        fragment.tokens = [model.encode(word) for word in fragment.lemmas]
