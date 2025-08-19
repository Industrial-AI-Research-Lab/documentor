import pytest
from pathlib import Path
from langchain_core.documents.base import Blob
from documentor.parsers.excel_parser import ExcelBlobParser

@pytest.fixture
def sample_excel_blob_for_formulas(data_dir):
    """
    Fixture for providing a test Excel file containing formulas.
    """
    test_file_path = Path(f"{data_dir}/test_excel.xlsx")
    with open(test_file_path, "rb") as f:
        return Blob(data=f.read(), path=test_file_path)

def test_parse_formulas(sample_excel_blob_for_formulas, data_dir):
    """
    Checks that the parser correctly extracts formulas from the test Excel file.
    """
    parser = ExcelBlobParser()
    documents = list(parser.lazy_parse(sample_excel_blob_for_formulas))

    formula_documents = [doc for doc in documents if "Formula:" in doc.page_content]
    with open(f"{data_dir}/formula_documents.txt.txt", "w", encoding="utf-8") as f:
        for doc in formula_documents:
            f.write(f"{doc.page_content}\n")

    assert len(formula_documents) > 0, "Expected formulas in the test file."

    for doc in formula_documents:
        assert "=" in doc.page_content, "In the document with the formula, the character '=' is expected."
