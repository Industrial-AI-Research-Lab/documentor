from documentor.structuries.document import Document
from .base import BaseSemanticModel


class NLTKNormalization(BaseSemanticModel):

    """
    Normalization text from document via nltk
    """

    def __init__(self):

        ...

    def __call__(self, document: Document, *args, **kwargs):
        ...
