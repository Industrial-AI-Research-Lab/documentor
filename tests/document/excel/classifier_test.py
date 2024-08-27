import pytest
import pandas as pd

from documentor.types.excel.document import SheetDocument
from documentor.types.excel.classifier import SheetClassifier
from tests.document.excel.parameters import CLASSIFIER_INIT_PARAMS


@pytest.mark.parametrize('params', CLASSIFIER_INIT_PARAMS)
def test_init_classifier(params):
    classifier = SheetClassifier(**params)
    assert isinstance(classifier, SheetClassifier)


def test_classify_fragments():
    classifier = SheetClassifier()
    doc = SheetDocument(pd.read_csv('data/hot_list_parsed.csv', index_col='Unnamed: 0'))
    labels, doc = classifier.classify_fragments(doc)
    assert (labels == doc.to_df()['label']).all()


def test_print_result():
    classifier = SheetClassifier()
    doc = SheetDocument(pd.read_csv('data/hot_list_parsed.csv', index_col='Unnamed: 0'))
    labels, doc = classifier.classify_fragments(doc)

    classifier.print_result(doc)
    assert True
