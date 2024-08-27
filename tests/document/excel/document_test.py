import pandas as pd
import pytest

from documentor.types.excel.document import SheetDocument
from documentor.types.excel.fragment import SheetFragment
from tests.document.excel.parameters import DOCUMENT_PATH_PARAMETRIZER


def init_document(simple_document: pd.DataFrame) -> tuple[SheetDocument, pd.DataFrame]:
    data = simple_document
    document = SheetDocument(data)
    return document, data


@pytest.mark.parametrize('path, expected_columns', DOCUMENT_PATH_PARAMETRIZER)
def test_document_initialization_from_file(path, expected_columns):
    document = SheetDocument(pd.read_csv(path, index_col='Unnamed: 0'))
    assert (document.to_df().columns == expected_columns).all()


def test_document_initialization(simple_document):
    document, data = init_document(simple_document)

    assert (document.to_df().value == data['value']).all()
    assert (document.to_df().start_content == data['start_content']).all()
    assert (document.to_df().relative_id == data['relative_id']).all()
    assert (document.to_df().type == data['type']).all()
    assert (document.to_df().row == data['row']).all()
    assert (document.to_df().column == data['column']).all()
    assert (document.to_df().length == data['length']).all()
    assert (document.to_df().vertically_merged == data['vertically_merged']).all()
    assert (document.to_df().horizontally_merged == data['horizontally_merged']).all()
    assert (document.to_df().font_selection == data['font_selection']).all()
    assert (document.to_df().top_border == data['top_border']).all()
    assert (document.to_df().bottom_border == data['bottom_border']).all()
    assert (document.to_df().left_border == data['left_border']).all()
    assert (document.to_df().right_border == data['right_border']).all()
    assert (document.to_df().color == data['color']).all()
    assert (document.to_df().font_color == data['font_color']).all()
    assert (document.to_df().is_formula == data['is_formula']).all()
    assert (document.to_df().row_type == data['row_type']).all()
    assert (document.to_df().ground_truth == data['ground_truth']).all()
    assert (document.to_df().label == data['label']).all()


def test_build_fragments(simple_document):
    document, data = init_document(simple_document)

    fragments = document.build_fragments

    assert len(fragments) == 2
    assert isinstance(fragments[0], SheetFragment)
    assert fragments[0].value == 'Value'
    assert fragments[1].value == 'Envera'


def test_iter_rows(simple_document):
    document, data = init_document(simple_document)

    rows = list(document.iter_rows())

    assert len(rows) == 2
    assert rows[0][0] == 0
    assert rows[0][1].value == 'Value'
    assert rows[1][0] == 1
    assert rows[1][1].value == 'Envera'
