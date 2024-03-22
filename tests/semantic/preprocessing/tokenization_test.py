import pandas as pd

from documentor.structuries.document import Document
from documentor.semantic.models.base import BaseSemanticModel
from documentor.semantic.preprocessing.tokenization import lemmatize


def test_tokenize(semantic_document, tokenization_model, tokenization_example):
    lemmatize(semantic_document, tokenization_model)
    result_tokens = semantic_document.tokens.values.tolist()[0]
    assert all([result == benchmark for result, benchmark in zip(result_tokens, tokenization_example)])
