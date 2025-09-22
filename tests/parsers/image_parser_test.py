import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from documentor.processing.parsers.image_parser import ImageParser


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


@patch('documentor.processing.parsers.image_parser.DotsOCRClient')
@patch('documentor.processing.parsers.image_parser.QwenClient')
def test_image_parser_initialization(mock_qwen_client, mock_dots_client, mock_ocr_config):
    """Test initialization of ImageParser."""
    parser = ImageParser(mock_ocr_config)
    supported_extensions = parser.supported_extensions()
    assert '.png' in supported_extensions
    assert '.jpg' in supported_extensions
    assert '.jpeg' in supported_extensions


@patch('documentor.processing.parsers.image_parser.DotsOCRClient')
@patch('documentor.processing.parsers.image_parser.QwenClient')
def test_image_parser_unsupported_extension(mock_qwen_client, mock_dots_client, tmp_path, mock_ocr_config):
    """Test error handling for unsupported extensions."""
    parser = ImageParser(mock_ocr_config)
    test_file = tmp_path / "test.txt"
    test_file.write_text("content", encoding="utf-8")
    
    with pytest.raises(ValueError, match="Unsupported file extension"):
        parser.parse(test_file)


@patch('documentor.processing.parsers.image_parser.DotsOCRClient')
@patch('documentor.processing.parsers.image_parser.QwenClient')
def test_image_parser_file_not_found(mock_qwen_client, mock_dots_client, mock_ocr_config):
    """Test error handling for non-existent files."""
    parser = ImageParser(mock_ocr_config)
    
    with pytest.raises(FileNotFoundError):
        parser.parse(Path("non_existent.png"))


@patch('documentor.processing.parsers.image_parser.DotsOCRClient')
@patch('documentor.processing.parsers.image_parser.QwenClient')
def test_image_parser_not_a_file(mock_qwen_client, mock_dots_client, tmp_path, mock_ocr_config):
    """Test error handling when path is not a file."""
    parser = ImageParser(mock_ocr_config)
    
    with pytest.raises(ValueError, match="Path is not a file"):
        parser.parse(tmp_path)  # tmp_path is a directory
