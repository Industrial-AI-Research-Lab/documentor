import pandas as pd

from documentor.structuries.document import Document
from semantic.models.base import BaseSemanticModel


def test_lemmatize(semantic_document, morphology_model):
    document = Document(semantic_document)


    assert (document.tokens == [['утка', 'утка', 'утка'], ['красиво', 'красиво', 'красиво']]).all()
