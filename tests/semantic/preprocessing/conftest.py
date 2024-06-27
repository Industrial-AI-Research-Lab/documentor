import pytest
import pandas as pd

from documentor.structuries.document import Document
from documentor.semantic.models.morphology import NatashaSemanticModel
from documentor.semantic.models.wiki2vec import WikiWord2VecModel
from tests.semantic.preprocessing.const import SENTENCE_EXAMPLE, VECTORIZATION_EXAMPLE


@pytest.fixture
def tokenization_model():
    return NatashaSemanticModel()


@pytest.fixture
def vectorization_model() -> WikiWord2VecModel:
    model = WikiWord2VecModel()
    model.load_weights('tests/semantic/preprocessing/data/ruwiki_20180420_300d.pkl')
    return model


@pytest.fixture
def semantic_document():
    data = pd.DataFrame({
        'value': SENTENCE_EXAMPLE.value,
        'ground_truth': None,
        'label': None,
        'vector': None,
        'tokens': None,
        'token_vectors': None
    })
    return Document(data)


@pytest.fixture
def vectorize_example():
    return VECTORIZATION_EXAMPLE


@pytest.fixture
def tokenization_example():
    return SENTENCE_EXAMPLE.tokens
