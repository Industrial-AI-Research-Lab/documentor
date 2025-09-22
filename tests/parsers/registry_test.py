import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from documentor.processing.parsers.registry import ParserRegistry
from documentor.processing.parsers.txt_parser import TxtParser


@pytest.fixture
def mock_ocr_config():
    """Create a mock OCR config for testing."""
    config = Mock()
    config.dots_ocr_config = Mock()
    config.qwen_config = Mock()
    return config


@patch('documentor.processing.parsers.registry.OCRPipelineConfig')
def test_parser_registry_initialization(mock_ocr_config_class):
    """Test initialization of ParserRegistry."""
    mock_config = Mock()
    mock_ocr_config_class.create_default.return_value = mock_config
    
    registry = ParserRegistry()
    assert isinstance(registry, ParserRegistry)
    assert registry.ocr_config is not None


def test_parser_registry_with_custom_config(mock_ocr_config):
    """Test initialization with custom OCR config."""
    registry = ParserRegistry(mock_ocr_config)
    assert registry.ocr_config == mock_ocr_config


@patch('documentor.processing.parsers.registry.OCRPipelineConfig')
def test_parser_registry_get_parser(mock_ocr_config_class):
    """Test getting parser for supported file types."""
    mock_config = Mock()
    mock_ocr_config_class.create_default.return_value = mock_config
    
    registry = ParserRegistry()
    
    # Test with .txt file
    txt_file = Path("test.txt")
    parser = registry.get_parser(txt_file)
    assert parser is not None
    assert isinstance(parser, TxtParser)
    
    # Test with unsupported file type
    unsupported_file = Path("test.xyz")
    parser = registry.get_parser(unsupported_file)
    assert parser is None


@patch('documentor.processing.parsers.registry.OCRPipelineConfig')
def test_parser_registry_can_parse(mock_ocr_config_class):
    """Test checking if file can be parsed."""
    mock_config = Mock()
    mock_ocr_config_class.create_default.return_value = mock_config
    
    registry = ParserRegistry()
    
    # Test with supported file type
    txt_file = Path("test.txt")
    assert registry.can_parse(txt_file) is True
    
    # Test with unsupported file type
    unsupported_file = Path("test.xyz")
    assert registry.can_parse(unsupported_file) is False


@patch('documentor.processing.parsers.registry.OCRPipelineConfig')
def test_parser_registry_supported_extensions(mock_ocr_config_class):
    """Test getting supported extensions."""
    mock_config = Mock()
    mock_ocr_config_class.create_default.return_value = mock_config
    
    registry = ParserRegistry()
    extensions = registry.supported_extensions()
    
    # Only test extensions that don't require external dependencies
    assert '.txt' in extensions
    # Note: PDF, PNG, DOCX parsers may not be available due to missing dependencies


@patch('documentor.processing.parsers.registry.OCRPipelineConfig')
def test_parser_registry_register_parser(mock_ocr_config_class):
    """Test registering custom parser."""
    mock_config = Mock()
    mock_ocr_config_class.create_default.return_value = mock_config
    
    registry = ParserRegistry()
    
    # Create custom parser
    class CustomParser:
        def supported_extensions(self):
            return {'.custom'}
    
    custom_parser = CustomParser()
    registry.register_parser(custom_parser)
    
    # Test that custom parser is now available
    custom_file = Path("test.custom")
    assert registry.can_parse(custom_file) is True
    assert registry.get_parser(custom_file) == custom_parser


@patch('documentor.processing.parsers.registry.OCRPipelineConfig')
def test_parser_registry_parse_file_success(mock_ocr_config_class, tmp_path):
    """Test parsing file successfully."""
    mock_config = Mock()
    mock_ocr_config_class.create_default.return_value = mock_config
    
    registry = ParserRegistry()
    
    # Create test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello World\nTest content", encoding="utf-8")
    
    # Parse file
    document = registry.parse_file(test_file)
    
    # Verify results
    assert document is not None
    assert len(document.fragments()) == 2
    assert str(document.fragments()[0]) == "Hello World"
    assert str(document.fragments()[1]) == "Test content"


@patch('documentor.processing.parsers.registry.OCRPipelineConfig')
def test_parser_registry_parse_file_not_found(mock_ocr_config_class):
    """Test parsing non-existent file."""
    mock_config = Mock()
    mock_ocr_config_class.create_default.return_value = mock_config
    
    registry = ParserRegistry()
    
    with pytest.raises(FileNotFoundError):
        registry.parse_file(Path("non_existent.txt"))


@patch('documentor.processing.parsers.registry.OCRPipelineConfig')
def test_parser_registry_get_parser_info(mock_ocr_config_class):
    """Test getting parser information."""
    mock_config = Mock()
    mock_ocr_config_class.create_default.return_value = mock_config
    
    registry = ParserRegistry()
    info = registry.get_parser_info()
    
    assert isinstance(info, dict)
    assert '.txt' in info
    assert info['.txt'] == 'TxtParser'
