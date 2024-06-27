from documentor.semantic.models.wiki2vec import BaseSemanticModel
from documentor.structuries.fragment import Fragment
from documentor.structuries.document import Document


def tokenize(document: Document, model: BaseSemanticModel):
    """
    Method whe receive a Document object and model based on BaseSemanticModel
    and appends vectors to the Document object
    :param document: Document for tokenization
    :type document: Document
    :param model: Embedding model
    :type model: WikiWord2VecModel
    :return: None
    """
    document.token_vectors = [model.encode(word) for row in document.tokens.tolist() for word in row]
