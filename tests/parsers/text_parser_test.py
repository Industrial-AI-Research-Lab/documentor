import pytest
from pathlib import Path

from documentor.processing.parsers.txt_parser import TxtParser
from documentor.data.structures.fragment.text import ParagraphFragment


def create_test_file(content: str, file_path: Path) -> Path:
    """Helper function for creating a test file."""
    file_path.write_text(content, encoding="utf-8")
    return file_path


def test_text_parser_initialization():
    """Test initialization of TxtParser."""
    # Checking correct initialization
    parser = TxtParser(encoding="utf-8")
    assert parser.encoding == "utf-8"
    assert '.txt' in parser.supported_extensions()

    # Checking the default value
    parser = TxtParser()
    assert parser.encoding == "utf-8"  # Default encoding


def test_parse_whole_text(tmp_path):
    """Test parsing the entire text file."""
    parser = TxtParser()
    test_content = "Line 1\nLine 2\nLine 3"
    test_file = create_test_file(test_content, tmp_path / "test.txt")

    document = parser.parse(test_file)
    
    # Check that we have 3 fragments (one per line)
    assert len(document.fragments()) == 3
    
    # Check fragment content
    fragments = document.fragments()
    assert str(fragments[0]) == "Line 1"
    assert str(fragments[1]) == "Line 2"
    assert str(fragments[2]) == "Line 3"
    
    # Check metadata
    assert document.metadata.name == "test.txt"
    assert document.metadata.file_path == str(test_file)
    assert document.metadata.processing_method == "text_extraction"


def test_parse_empty_text(tmp_path):
    """Test parsing an empty text file."""
    parser = TxtParser()
    test_file = create_test_file("", tmp_path / "empty.txt")

    document = parser.parse(test_file)
    
    # Empty file should result in no fragments
    assert len(document.fragments()) == 0


def test_parse_single_line(tmp_path):
    """Test parsing a single-line text file."""
    parser = TxtParser()
    test_content = "Single line"
    test_file = create_test_file(test_content, tmp_path / "single.txt")

    document = parser.parse(test_file)
    
    assert len(document.fragments()) == 1
    assert str(document.fragments()[0]) == "Single line"


def test_parse_with_empty_lines(tmp_path):
    """Test parsing text with empty lines (should be skipped)."""
    parser = TxtParser()
    test_content = "Line 1\n\nLine 3\n\n\nLine 6"
    test_file = create_test_file(test_content, tmp_path / "with_empty.txt")

    document = parser.parse(test_file)
    
    # Should have 3 fragments (empty lines skipped)
    assert len(document.fragments()) == 3
    fragments = document.fragments()
    assert str(fragments[0]) == "Line 1"
    assert str(fragments[1]) == "Line 3"
    assert str(fragments[2]) == "Line 6"


def test_parse_with_error(tmp_path):
    """Test error handling when parsing."""
    parser = TxtParser()
    
    # Test with non-existent file
    with pytest.raises(FileNotFoundError):
        parser.parse(tmp_path / "non_existent.txt")
    
    # Test with unsupported extension
    test_file = create_test_file("content", tmp_path / "test.doc")
    with pytest.raises(ValueError, match="Unsupported file extension"):
        parser.parse(test_file)


def test_parse_real_file(data_dir):
    """Test parsing a real file."""
    parser = TxtParser()
    test_file_path = Path(f"{data_dir}/test_txt.txt")
    
    # Checking that the file exists
    assert test_file_path.exists(), "Test file not found"
    
    # Parse the file
    document = parser.parse(test_file_path)
    
    # Get the original file content for comparison
    with open(test_file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Get non-empty lines from original content
    original_lines = [line.strip() for line in original_content.splitlines() if line.strip()]
    
    # Check that we have the right number of fragments
    assert len(document.fragments()) == len(original_lines)
    
    # Check that each fragment matches the corresponding line
    fragments = document.fragments()
    for i, fragment in enumerate(fragments):
        assert str(fragment) == original_lines[i]
    
    # Check metadata
    assert document.metadata.name == "test_txt.txt"
    assert document.metadata.file_path == str(test_file_path)
    assert document.metadata.processing_method == "text_extraction"


def test_fragment_properties(tmp_path):
    """Test that fragments have correct properties."""
    parser = TxtParser()
    test_content = "Line 1\nLine 2\nLine 3"
    test_file = create_test_file(test_content, tmp_path / "test.txt")

    document = parser.parse(test_file)
    fragments = document.fragments()
    
    # Check that all fragments are ParagraphFragment instances
    for fragment in fragments:
        assert isinstance(fragment, ParagraphFragment)
        assert hasattr(fragment, 'page')  # Should have page number
        assert hasattr(fragment, 'id')    # Should have ID
