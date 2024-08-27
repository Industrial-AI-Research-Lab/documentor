import pandas as pd
import pytest


@pytest.fixture
def simple_document() -> pd.DataFrame:
    return pd.DataFrame({
        'value': ['Value', 'Envera'],
        'start_content': ['Value', 'Envera'],
        'relative_id': [25, 103],
        'type': ['str', 'str'],
        'row': [6, 10],
        'column': [5, 7],
        'length': [5, 6],
        'vertically_merged': [False, False],
        'horizontally_merged': [False, False],
        'font_selection': [True, False],
        'top_border': [True, False],
        'bottom_border': [False, False],
        'left_border': [False, True],
        'right_border': [False, False],
        'color': ['00000000', '00000000'],
        'font_color': [0, 0],
        'is_formula': [False, False],
        'row_type': [1, 2],
        'ground_truth': ['Category', 'Client_title'],
        'label': [1, 2]
    })


@pytest.fixture
def new_simple_params() -> tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series,
                                 pd.Series, pd.Series, pd.Series, pd.Series, pd.Series,
                                 pd.Series, pd.Series, pd.Series, pd.Series, pd.Series,
                                 pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    value = pd.Series(['Value', 'Envera']),
    start_content = pd.Series(['Value', 'Envera'])
    relative_id = pd.Series([25, 103])
    type = pd.Series(['str', 'str'])
    row = pd.Series([6, 10])
    column = pd.Series([5, 7])
    length = pd.Series([5, 6])
    vertically_merged = pd.Series([False, False])
    horizontally_merged = pd.Series([False, False])
    font_selection = pd.Series([True, False])
    top_border = pd.Series([True, False])
    bottom_border = pd.Series([False, False])
    left_border = pd.Series([False, True])
    right_border = pd.Series([False, False])
    color = pd.Series(['00000000', '00000000'])
    font_color = pd.Series([0, 0])
    is_formula = pd.Series([False, False])
    row_type = pd.Series([1, 2])
    ground_truth = pd.Series(['Category', 'Client_title'])
    label = pd.Series([1, 2])
    return value, start_content, relative_id, type, row, column, length, vertically_merged, horizontally_merged, \
        font_selection, top_border, bottom_border, left_border, right_border, color, font_color, is_formula, row_type, \
        ground_truth, label
