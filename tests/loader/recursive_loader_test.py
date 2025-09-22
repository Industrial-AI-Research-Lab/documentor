import pytest
from pathlib import Path
from documentor.processing.loaders.recursive_loader import RecursiveDocumentLoader
from documentor.processing.parsers.txt_parser import TxtParser


def test_recursive_loader_simple_file(tmp_path):
    """
    Checks basic loading of a text file into a document.
    """
    # Create a test file
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello World\nThis is a test", encoding="utf-8")

    # Initialize RecursiveDocumentLoader with TxtParser
    parser_registry = {".txt": TxtParser()}
    
    loader = RecursiveDocumentLoader(
        parser_registry=parser_registry,
        extract_archives=False
    )

    # Load documents
    documents = list(loader.load_directory(tmp_path, recursive=False))

    # Verify results - should have 1 document with 2 fragments
    assert len(documents) == 1, "Expected 1 document"
    document = documents[0]
    assert len(document.fragments()) == 2, "Expected 2 fragments"
    
    fragments = document.fragments()
    assert str(fragments[0]) == "Hello World"
    assert str(fragments[1]) == "This is a test"


def test_recursive_loader_zip(tmp_path):
    """
    Checks loading content from a zip archive.
    """
    import zipfile

    # Create a test zip archive
    zip_path = tmp_path / "test_archive.zip"
    text_content = "Hello from zip\nAnother line"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("file_inside.txt", text_content)

    # Initialize RecursiveDocumentLoader with ZIP support
    loader = RecursiveDocumentLoader(
        extract_archives=True
    )

    # Load documents
    documents = list(loader.load_directory(tmp_path, recursive=False))

    # Verify results - should have documents for the ZIP archive
    # The loader creates both the ZIP archive document and processes files inside
    assert len(documents) >= 1, "Expected at least 1 document for ZIP archive"
    
    # Check that we have a ZIP archive document
    zip_docs = [doc for doc in documents if "ZIP archive: test_archive.zip" in str(doc.fragments()[0])]
    assert len(zip_docs) == 1, "Expected exactly 1 ZIP archive document"


def test_recursive_loader_unsupported_extension(tmp_path):
    """
    Checks that files with unsupported extensions are not loaded.
    """
    # Create files with different extensions
    txt_file = tmp_path / "test_file.txt"
    txt_file.write_text("Sample text", encoding="utf-8")
    md_file = tmp_path / "readme.md"
    md_file.write_text("Markdown content", encoding="utf-8")

    # Load only txt files
    parser_registry = {".txt": TxtParser()}
    loader = RecursiveDocumentLoader(
        parser_registry=parser_registry,
        extract_archives=False
    )

    documents = list(loader.load_directory(tmp_path, recursive=False))
    assert len(documents) == 1, "Expected to load only 1 file with txt extension"
    assert str(documents[0].fragments()[0]) == "Sample text"


def test_recursive_loader_empty_directory(tmp_path):
    """
    Checks that no documents are loaded when the directory is empty.
    """
    # Do not create any files in tmp_path, leaving the directory empty
    loader = RecursiveDocumentLoader(extract_archives=False)
    documents = list(loader.load_directory(tmp_path, recursive=True))
    assert len(documents) == 0, "Expected no documents when the directory is empty"


def test_recursive_loader_multiple_files(tmp_path):
    """
    Checks the loader's operation when there are multiple files of different types.
    """
    # Create several files of different types
    txt_file = tmp_path / "file1.txt"
    txt_file.write_text("Content of TXT file", encoding="utf-8")

    # Create another txt file
    txt_file2 = tmp_path / "file2.txt"
    txt_file2.write_text("Content of second TXT file", encoding="utf-8")

    # Initialize loader for txt files
    parser_registry = {".txt": TxtParser()}
    loader = RecursiveDocumentLoader(
        parser_registry=parser_registry,
        extract_archives=False
    )

    documents = list(loader.load_directory(tmp_path, recursive=False))

    # Verify that both files were loaded
    assert len(documents) == 2, "Expected to load two documents"
    
    # Check content
    contents = [str(doc.fragments()[0]) for doc in documents]
    assert "Content of TXT file" in contents
    assert "Content of second TXT file" in contents


def test_recursive_loader_subdirectories(tmp_path):
    """
    Checks the loader's operation when recursive traversal of subdirectories is required.
    """
    # Create a subdirectory and a file inside it
    sub_dir = tmp_path / "subfolder"
    sub_dir.mkdir()
    sub_file = sub_dir / "nested.txt"
    sub_file.write_text("Text inside subdirectory", encoding="utf-8")

    # Run the loader with recursive traversal
    parser_registry = {".txt": TxtParser()}
    loader = RecursiveDocumentLoader(
        parser_registry=parser_registry,
        extract_archives=False
    )
    
    documents = list(loader.load_directory(tmp_path, recursive=True))
    assert len(documents) == 1, "Expected to load one file from the nested directory"
    assert "Text inside subdirectory" in str(documents[0].fragments()[0])


def test_recursive_loader_file_not_found():
    """
    Checks error handling when directory doesn't exist.
    """
    loader = RecursiveDocumentLoader(extract_archives=False)
    
    with pytest.raises(FileNotFoundError):
        list(loader.load_directory(Path("non_existent_directory"), recursive=True))


def test_recursive_loader_single_file(tmp_path):
    """
    Checks loading a single file directly.
    """
    # Create a test file
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Single file content", encoding="utf-8")

    # Initialize loader
    parser_registry = {".txt": TxtParser()}
    loader = RecursiveDocumentLoader(
        parser_registry=parser_registry,
        extract_archives=False
    )

    # Load single file
    document = loader.load_file(test_file)

    # Verify results
    assert len(document.fragments()) == 1
    assert str(document.fragments()[0]) == "Single file content"
    assert document.metadata.name == "test_file.txt"