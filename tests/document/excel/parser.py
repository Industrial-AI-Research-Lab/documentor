from documentor.types.excel.parser import SheetParser
from documentor.types.excel.document import SheetDocument

from tests.document.excel.parameters import PARSER_WORK_PARAMETRIZER, PARSER_EXCEPTIONS_PARAMETRIZER

import pandas as pd
import pytest


@pytest.mark.parametrize('test_values', PARSER_WORK_PARAMETRIZER)
def test_sheet_parse_file(test_values):
    parser = SheetParser()
    doc = parser.parse_file(**test_values)
    assert type(doc) == SheetDocument
