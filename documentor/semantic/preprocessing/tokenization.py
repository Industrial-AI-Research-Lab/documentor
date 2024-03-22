import re

from documentor.structuries.document import Document
from documentor.semantic.models.morphology import BaseSemanticModel


def lemmatize(document: Document, model: BaseSemanticModel, *args, **kwargs):
    """
    Method who receive a document object and model based on BaseSemanticModel
    and appends lemmas to the Document object
    :param document: a Document object which contains data for lemmatize
    :type document: Document
    :model BaseSemanticModel: model for lemmatize
    :type model: BaseSemanticModel
    :return None:
    """

    lemmas = [model.encode(cell) for cell in document.value]
    document.tokens = lemmas
