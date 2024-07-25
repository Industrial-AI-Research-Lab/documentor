from .base import BaseSemanticModel
from documentor.structuries.document import Document


class NatashaSpellChecker(BaseSemanticModel):

    def __init__(self):

        ...

    def __call__(self, document: Document, *args, **kwargs):
        ...
