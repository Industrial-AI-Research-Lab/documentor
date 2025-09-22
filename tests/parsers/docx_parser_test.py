import pytest
from pathlib import Path
from unittest.mock import patch
from documentor.processing.parsers.docx_parser import DocxParser


@patch('documentor.processing.parsers.docx_parser.DOCX_SUPPORT', True)
def test_docx_parser_initialization():
    """Test initialization of DocxParser."""
    parser = DocxParser()
    assert '.docx' in parser.supported_extensions()


@patch('documentor.processing.parsers.docx_parser.DOCX_SUPPORT', True)
def test_docx_parser_unsupported_extension(tmp_path):
    """Test error handling for unsupported extensions."""
    parser = DocxParser()
    test_file = tmp_path / "test.txt"
    test_file.write_text("content", encoding="utf-8")
    
    with pytest.raises(ValueError, match="Unsupported file extension"):
        parser.parse(test_file)


@patch('documentor.processing.parsers.docx_parser.DOCX_SUPPORT', True)
def test_docx_parser_file_not_found():
    """Test error handling for non-existent files."""
    parser = DocxParser()
    
    with pytest.raises(FileNotFoundError):
        parser.parse(Path("non_existent.docx"))


@patch('documentor.processing.parsers.docx_parser.DOCX_SUPPORT', True)
def test_docx_parser_not_a_file(tmp_path):
    """Test error handling when path is not a file."""
    parser = DocxParser()
    
    with pytest.raises(ValueError, match="Path is not a file"):
        parser.parse(tmp_path)  # tmp_path is a directory
