from enum import Enum
from documentor.structuries.document import Document
from .base import BaseSemanticModel


class NormalizationModelsEnum(Enum):
    natasha = None
    nltk = None


class NormalizationModel(BaseSemanticModel):
    """
    Normalization text from document via open source libs
    """

    def __init__(self, model: NormalizationModelsEnum):

        ...

    def __call__(self, document: Document, *args, **kwargs):
        ...
