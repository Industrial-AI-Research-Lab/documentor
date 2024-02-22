import pandas as pd

from documentor.structuries.document import Document
from documentor.structuries.fragment import Fragment


def test_document_initialization():
    data = pd.DataFrame({
        'value': ['value1', 'value2'],
        'ground_truth': ['truth1', 'truth2'],
        'label': ['label1', 'label2'],
        'vector': [['v1.1', 'v1.2'], ['v2.1', 'v2.2']],
        'tokens': [['t1.1', 't1.2'], ['t2.1', 't2.2']],
        'token_vectors': [['tv1.1', 'tv1.2'], ['tv2.1', 'tv2.2']]
    })

    document = Document(data)

    assert (document.value == data['value']).all()
    assert (document.ground_truth == data['ground_truth']).all()
    assert (document.label == data['label']).all()
    assert (document.vector == data['vector']).all()
    assert (document.tokens == data['tokens']).all()
    assert (document.token_vectors == data['token_vectors']).all()


def test_build_fragments():
    data = pd.DataFrame({
        'value': ['value1', 'value2']
    })
    document = Document(data)

    fragments = document.build_fragments()

    assert len(fragments) == 2
    assert isinstance(fragments[0], Fragment)
    assert fragments[0].value == 'value1'
    assert fragments[1].value == 'value2'


def test_iter_rows():
    data = pd.DataFrame({
        'value': ['value1', 'value2']
    })
    document = Document(data)

    rows = list(document.iter_rows())

    assert len(rows) == 2
    assert rows[0][0] == 0
    assert rows[0][1].value == 'value1'
    assert rows[1][0] == 1
    assert rows[1][1].value == 'value2'


def test_to_df():
    data = pd.DataFrame({
        'value': ['value1', 'value2']
    })
    document = Document(data)

    df = document.to_df()

    assert df.equals(data)


def test_properties():
    data = pd.DataFrame({
        'value': ['value1', 'value2'],
        'ground_truth': ['truth1', 'truth2'],
        'label': ['label1', 'label2'],
        'vector': [['v1.1', 'v1.2'], ['v2.1', 'v2.2']],
        'tokens': [['t1.1', 't1.2'], ['t2.1', 't2.2']],
        'token_vectors': [['tv1.1', 'tv1.2'], ['tv2.1', 'tv2.2']]
    })

    document = Document(data)
    document.label = pd.Series(['new_label1', 'new_label2'])
    document.vector = pd.Series([['new_v1.1', 'new_v1.2'], ['new_v2.1', 'new_v2.2']])
    document.tokens = pd.Series([['new_t1.1', 'new_t1.2'], ['new_t2.1', 'new_t2.2']])
    document.token_vectors = pd.Series([['new_tv1.1', 'new_tv1.2'], ['new_tv2.1', 'new_tv2.2']])

    assert document.label.tolist() == ['new_label1', 'new_label2']
    assert document.vector.tolist() == [['new_v1.1', 'new_v1.2'], ['new_v2.1', 'new_v2.2']]
    assert document.tokens.tolist() == [['new_t1.1', 'new_t1.2'], ['new_t2.1', 'new_t2.2']]
    assert document.token_vectors.tolist() == [['new_tv1.1', 'new_tv1.2'], ['new_tv2.1', 'new_tv2.2']]
