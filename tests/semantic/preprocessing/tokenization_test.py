import pandas as pd

from documentor.structuries.document import Document
from semantic.models.base import BaseSemanticModel
from semantic.preprocessing.tokenization import lemmatize


def lemmatize_document(data: pd.DataFrame, model: BaseSemanticModel) -> Document:

    return Document(data)

def test_lemmatize(semantic_document, tokenization_model):
    document = Document(semantic_document)

    lemmatize(document, tokenization_model)

    assert (document.tokens == [['утка', 'утка', 'утка'], ['красиво', 'красиво', 'красиво']]).all()
