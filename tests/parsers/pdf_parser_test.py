import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from documentor.processing.parsers.pdf_parser import PdfParser


@pytest.fixture
def mock_ocr_config():
    """Create a mock OCR config for testing."""
    config = Mock()
    
    # Mock dots_ocr_config
    dots_config = Mock()
    dots_config.base_url = "http://test.com"
    dots_config.api_key = "test_key"
    dots_config.model_name = "test_model"
    config.dots_ocr_config = dots_config
    
    # Mock qwen_config
    qwen_config = Mock()
    qwen_config.base_url = "http://test.com"
    qwen_config.api_key = "test_key"
    qwen_config.model_name = "test_model"
    config.qwen_config = qwen_config
    
    return config


@patch('documentor.processing.parsers.pdf_parser.PDF_SUPPORT', True)
def test_pdf_parser_initialization(mock_ocr_config):
    """Test initialization of PdfParser."""
    parser = PdfParser(mock_ocr_config)
    assert '.pdf' in parser.supported_extensions()


@patch('documentor.processing.parsers.pdf_parser.PDF_SUPPORT', True)
def test_pdf_parser_unsupported_extension(tmp_path, mock_ocr_config):
    """Test error handling for unsupported extensions."""
    parser = PdfParser(mock_ocr_config)
    test_file = tmp_path / "test.txt"
    test_file.write_text("content", encoding="utf-8")
    
    with pytest.raises(ValueError, match="Unsupported file extension"):
        parser.parse(test_file)


@patch('documentor.processing.parsers.pdf_parser.PDF_SUPPORT', True)
def test_pdf_parser_file_not_found(mock_ocr_config):
    """Test error handling for non-existent files."""
    parser = PdfParser(mock_ocr_config)
    
    with pytest.raises(FileNotFoundError):
        parser.parse(Path("non_existent.pdf"))


@patch('documentor.processing.parsers.pdf_parser.PDF_SUPPORT', True)
def test_pdf_parser_not_a_file(tmp_path, mock_ocr_config):
    """Test error handling when path is not a file."""
    parser = PdfParser(mock_ocr_config)
    
    with pytest.raises(ValueError, match="Path is not a file"):
        parser.parse(tmp_path)  # tmp_path is a directory
