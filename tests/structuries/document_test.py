import pandas as pd

from documentor.structuries.document import Document
from documentor.structuries.fragment import TextFragment


def init_document(simple_document: pd.DataFrame) -> tuple[Document, pd.DataFrame]:
    data = simple_document
    document = Document(data)
    return document, data


def test_document_initialization(simple_document):
    document, data = init_document(simple_document)

    assert (document.value == data['value']).all()
    assert (document.ground_truth == data['ground_truth']).all()
    assert (document.label == data['label']).all()
    assert (document.vector == data['vector']).all()
    assert (document.tokens == data['tokens']).all()
    assert (document.token_vectors == data['token_vectors']).all()


def test_build_fragments(simple_document):
    document, data = init_document(simple_document)

    fragments = document.build_fragments()

    assert len(fragments) == 2
    assert isinstance(fragments[0], TextFragment)
    assert fragments[0].value == 'value1'
    assert fragments[1].value == 'value2'


def test_iter_rows(simple_document):
    document, data = init_document(simple_document)

    rows = list(document.iter_rows())

    assert len(rows) == 2
    assert rows[0][0] == 0
    assert rows[0][1].value == 'value1'
    assert rows[1][0] == 1
    assert rows[1][1].value == 'value2'


def test_to_df(simple_document):
    document, data = init_document(simple_document)

    df = document.to_df()

    assert df.equals(data)


def test_properties(simple_document, new_simple_params):
    document, data = init_document(simple_document)
    label, vector, tokens, token_vectors = new_simple_params

    document.label = label
    document.vector = vector
    document.tokens = tokens
    document.token_vectors = token_vectors

    assert (document.label == label).all()
    assert (document.vector == vector).all()
    assert (document.tokens == tokens).all()
    assert (document.token_vectors == token_vectors).all()
