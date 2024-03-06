import pytest
import pandas as pd

from documentor.structuries.document import Document
from documentor.semantic.models.morphology import NatashaSemanticModel
from documentor.semantic.models.wiki2vec import WikiWord2VecModel

@pytest.fixture
def tokenization_model():
    return NatashaSemanticModel()

@pytest.fixture
def semantic_document():
    data = pd.DataFrame({
        'value': ['утка Утки уток', 'красивый красивая красивое'],
        'ground_truth': None,
        'label': None,
        'vector': None,
        'tokens': None,
        'token_vectors': None
    })
    return Document(data)
