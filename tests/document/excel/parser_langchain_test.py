import pytest
from documentor.formats.excel.parser import SheetLangChainParser
from langchain_core.documents import Document
import os

# Путь к тестовому файлу Excel
TEST_EXCEL_FILE = 'C:/Users/alexh/py_prog/excel/documentor/tests/document/excel/data/Global_Hot_List.xlsx'

@pytest.fixture
def setup_excel_file():
    # Убедитесь, что тестовый файл существует
    assert os.path.exists(TEST_EXCEL_FILE), f"Test file {TEST_EXCEL_FILE} does not exist."

@pytest.mark.usefixtures("setup_excel_file")
def test_parse_file_creates_documents():
    parser = SheetLangChainParser()
    documents = parser.parse_file(TEST_EXCEL_FILE)
    
    # Проверяем, что возвращается список объектов Document
    assert isinstance(documents, list)
    assert all(isinstance(doc, Document) for doc in documents)

    # Проверяем, что каждый документ содержит ожидаемые метаданные
    for doc in documents:
        assert 'sheet_name' in doc.metadata
        assert 'file_path' in doc.metadata
        assert 'sheet_index' in doc.metadata

@pytest.mark.usefixtures("setup_excel_file")
def test_parse_file_handles_invalid_file():
    parser = SheetLangChainParser()
    
    with pytest.raises(Exception) as excinfo:
        parser.parse_file('invalid/path/to/file.xlsx')
    
    assert "The specified file does not exist or is unavailable." in str(excinfo.value)
