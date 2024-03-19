import pytest

from documentor.types.excel.document import SheetDocument
from documentor.types.excel.classifier import SheetClassifier
from tests.document.excel.parameters import CLASSIFIER_INIT_PARAMS


@pytest.mark.parametrize('params', CLASSIFIER_INIT_PARAMS)
def test_init_classifier(params):
    classifier = SheetClassifier(**params)
    assert isinstance(classifier, SheetClassifier)

def test_classify_fragments():
    pass

def test_print_result():
    pass

