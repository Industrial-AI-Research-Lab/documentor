import pandas as pd
import pytest


@pytest.fixture
def simple_document() -> pd.DataFrame:
    return pd.DataFrame({
        'value': ['value1', 'value2'],
        'ground_truth': ['truth1', 'truth2'],
        'label': ['label1', 'label2'],
        'vector': [[1.1, 1.2], [2.1, 2.2]],
        'tokens': [['t1.1', 't1.2'], ['t2.1', 't2.2']],
        'token_vectors': [[[0.111, 0.112], [0.121, 0.122]], [[0.211, 0.212], [0.221, 0.222]]]
    })


@pytest.fixture
def new_simple_params() -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    label = pd.Series(['new_label1', 'new_label2'])
    vector = pd.Series([[3.1, 3.2], [4.1, 4.2]], )
    tokens = pd.Series([['new_t1.1', 'new_t1.2'], ['new_t2.1', 'new_t2.2']])
    token_vectors = pd.Series([[[0.311, 0.312], [0.321, 0.322]], [[0.411, 0.412], [0.421, 0.422]]])
    return label, vector, tokens, token_vectors
