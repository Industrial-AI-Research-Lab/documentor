import pytest
from pathlib import Path
from langchain_core.documents.base import Blob

from documentor.parsers.text_parser import TextBlobParser
from documentor.parsers.extensions import DocExtension


def create_test_blob(content: str, source_path: str = "test.txt") -> Blob:
    """Helper function for creating a test Blob."""
    return Blob(
        data=content.encode(),
        mimetype="text/plain",
        source=None,
        path=Path(source_path)  # Now using path instead of source_path
    )


def test_text_parser_initialization():
    """Test initialization of TextBlobParser."""
    # Checking correct initialization
    parser = TextBlobParser(batch_lines=5)
    assert parser.batch_lines == 5
    assert DocExtension.txt in parser._extension

    # Checking the default value
    parser = TextBlobParser()
    assert parser.batch_lines == 0

    # Checking invalid values of batch_lines
    with pytest.raises(ValueError):
        TextBlobParser(batch_lines=-1)
    
    with pytest.raises(ValueError):
        TextBlobParser(batch_lines=1.5)


def test_parse_whole_text():
    """Test parsing the entire text (batch_lines=0)."""
    parser = TextBlobParser()
    test_content = "Line 1\nLine 2\nLine 3"
    blob = create_test_blob(test_content)

    documents = list(parser.lazy_parse(blob))
    assert len(documents) == 1
    assert documents[0].page_content == test_content
    assert documents[0].metadata["line_number"] == 0
    assert documents[0].metadata["file_name"] == "test.txt"
    assert documents[0].metadata["source"] == str(Path("test.txt"))
    assert documents[0].metadata["file_type"] == ".txt"


def test_parse_batched_text():
    """Test parsing text with batch_lines=2."""
    parser = TextBlobParser(batch_lines=2)
    test_content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
    blob = create_test_blob(test_content)

    documents = list(parser.lazy_parse(blob))
    assert len(documents) == 3
    assert documents[0].page_content == "Line 1\nLine 2\n"
    assert documents[1].page_content == "Line 3\nLine 4\n"
    assert documents[2].page_content == "Line 5"

    # Checking line_number
    assert documents[0].metadata["line_number"] == 0
    assert documents[1].metadata["line_number"] == 2
    assert documents[2].metadata["line_number"] == 4


def test_parse_empty_text():
    """Test parsing an empty text."""
    parser = TextBlobParser()
    blob = create_test_blob("")

    documents = list(parser.lazy_parse(blob))
    assert len(documents) == 1
    assert documents[0].page_content == ""


def test_parse_single_line():
    """Test parsing a single-line text with different batch_lines values."""
    test_content = "Single line"
    blob = create_test_blob(test_content)

    # With batch_lines=0
    parser = TextBlobParser()
    documents = list(parser.lazy_parse(blob))
    assert len(documents) == 1
    assert documents[0].page_content == test_content

    # With batch_lines=2
    parser = TextBlobParser(batch_lines=2)
    documents = list(parser.lazy_parse(blob))
    assert len(documents) == 1
    assert documents[0].page_content == test_content


def test_parse_with_error():
    """Test error handling when parsing."""
    parser = TextBlobParser()
    
    # Create a Blob with invalid data
    invalid_blob = Blob(data=None, source=None, source_path=Path("test.txt"))
    
    with pytest.raises(Exception):
        list(parser.lazy_parse(invalid_blob))


def test_metadata_without_source_path():
    """Test document metadata without source_path."""
    parser = TextBlobParser()
    # Create a Blob without a path
    blob = Blob(
        data="Test content".encode(),
        mimetype="text/plain",
        source=None,
        path=None
    )

    documents = list(parser.lazy_parse(blob))
    assert len(documents) == 1
    assert documents[0].metadata["file_name"] is None
    assert documents[0].metadata["source"] is None
    assert documents[0].metadata["file_type"] is None


def test_parse_real_file(data_dir):
    """Test parsing a real file."""
    parser = TextBlobParser()
    test_file_path = Path(f"{data_dir}/test_txt.txt")
    
    # Checking that the file exists
    assert test_file_path.exists(), "Test file not found"
    
    with open(test_file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            mimetype="text/plain",
            source=None,
            path=test_file_path
        )

    # Test parsing the entire file (batch_lines=0)
    documents = list(parser.lazy_parse(blob))
    assert len(documents) == 1
    
    # Get the original file content for comparison
    with open(test_file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Normalize texts for comparison (remove \r\n and trailing spaces)
    parsed_content = documents[0].page_content.replace('\r\n', '\n').rstrip()
    original_content = original_content.replace('\r\n', '\n').rstrip()
    
    # Check that the content matches the original
    assert parsed_content == original_content
    assert len(parsed_content.splitlines()) == len(original_content.splitlines())
    
    # Check metadata
    assert documents[0].metadata["file_name"] == "test_txt.txt"
    assert documents[0].metadata["source"] == str(test_file_path)
    assert documents[0].metadata["file_type"] == ".txt"
    
    # Test parsing the file with batch_lines=3
    parser = TextBlobParser(batch_lines=3)
    documents = list(parser.lazy_parse(blob))
    
    # Combine content of all parts and normalize
    combined_content = ''.join(doc.page_content for doc in documents).replace('\r\n', '\n').rstrip()
    assert combined_content == original_content
    
    # Check the number of lines in each part
    original_lines = original_content.splitlines(keepends=True)
    assert len(documents) == (len(original_lines) + 2) // 3  # rounding up
    
    # Check that line_number is correct for each document
    for i, doc in enumerate(documents):
        assert doc.metadata["line_number"] == i * 3
