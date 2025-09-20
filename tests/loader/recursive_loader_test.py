from documentor.loaders.recursive_loader import RecursiveLoader

def test_recursive_loader_simple_file(tmp_path):
    """
    Checks basic loading of a text file into an array of documents.
    """
    # Create a test file
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Hello World\nThis is a test", encoding="utf-8")

    # Initialize RecursiveLoader
    loader = RecursiveLoader(
        path=str(tmp_path),
        extension=["txt"],
        is_recursive=True,
        use_unzip=False
    )

    # Load documents
    documents = list(loader.lazy_load())

    # Verify results
    assert len(documents) == 2, "Expected 2 lines from the text file"
    assert documents[0].page_content.strip() == "Hello World"
    assert documents[1].page_content.strip() == "This is a test"
    assert len(loader.logs["info"]) > 0, "Expected a log about file loading"
    assert "Reading file:" in loader.logs["info"][0]


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

    # Initialize RecursiveLoader with zip_loader support
    loader = RecursiveLoader(
        path=str(tmp_path),
        extension=["zip"],
        is_recursive=True,
        use_unzip=True
    )

    # Load documents
    documents = list(loader.lazy_load())

    # Verify results
    assert len(documents) == 2, "Expected 2 lines from the file inside the zip"
    assert documents[0].page_content.strip() == "Hello from zip"
    assert documents[1].page_content.strip() == "Another line"
    assert "Processing ZIP archive:" in loader.logs["info"][0]


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
    loader = RecursiveLoader(
        path=str(tmp_path),
        extension=["txt"],
        is_recursive=False,
        use_unzip=False
    )

    documents = list(loader.lazy_load())
    assert len(documents) == 1, "Expected to load only 1 file with txt extension"
    assert documents[0].page_content.strip() == "Sample text"
    log_info = loader.logs["info"]
    # Check that there is no attempt to read readme.md in the logs
    assert all("readme.md" not in message for message in log_info)

def test_recursive_loader_empty_directory(tmp_path):
    """
    Checks that no documents are loaded when the directory is empty.
    """
    # Do not create any files in tmp_path, leaving the directory empty
    loader = RecursiveLoader(
        path=str(tmp_path),
        extension=["txt", "md", "zip"],
        is_recursive=True,
        use_unzip=True
    )
    documents = list(loader.lazy_load())
    assert len(documents) == 0, "Expected no documents when the directory is empty"
    assert not loader.logs["info"], "Expected no informational log entries when the directory is empty"

def test_recursive_loader_multiple_files(tmp_path):
    """
    Checks the loader's operation when there are multiple files of different types.
    """
    # Create several files of different types
    txt_file = tmp_path / "file1.txt"
    txt_file.write_text("Content of TXT file", encoding="utf-8")

    md_file = tmp_path / "file2.md"
    md_file.write_text("Content of MD file", encoding="utf-8")

    # Specify that we are interested in files with txt and md extensions
    loader = RecursiveLoader(
        path=str(tmp_path),
        extension=["txt", "md"],
        is_recursive=False,
        use_unzip=False
    )
    documents = list(loader.lazy_load())

    # Verify that both files were loaded
    assert len(documents) == 2, "Expected to load two documents"
    assert any("Content of TXT file" in doc.page_content for doc in documents), "TXT document not found"
    assert any("Content of MD file" in doc.page_content for doc in documents), "MD document not found"

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
    loader = RecursiveLoader(
        path=str(tmp_path),
        extension=["txt"],
        is_recursive=True,
        use_unzip=False
    )
    documents = list(loader.lazy_load())
    assert len(documents) == 1, "Expected to load one file from the nested directory"
    assert "Text inside subdirectory" in documents[0].page_content, "File from subdirectory was not loaded"

def test_recursive_loader_several_zips(tmp_path):
    """
    Checks the operation of the recursive loader if there are several ZIP archives in the directory.
    """
    import zipfile

    # Create the first archive
    zip_path_1 = tmp_path / "archive1.zip"
    with zipfile.ZipFile(zip_path_1, "w") as zf:
        zf.writestr("inside1.txt", "Content of the first archive\nSecond line")

    # Create the second archive
    zip_path_2 = tmp_path / "archive2.zip"
    with zipfile.ZipFile(zip_path_2, "w") as zf:
        zf.writestr("inside2.txt", "Content of the second archive")

    loader = RecursiveLoader(
        path=str(tmp_path),
        extension=["zip"],
        is_recursive=True,
        use_unzip=True
    )
    documents = list(loader.lazy_load())
    # The first archive contains 2 lines, the second - 1 line => total 3 documents
    assert len(documents) == 3, "Expected to load three lines from two different zip archives"

    # Verify that each line is present
    contents = [doc.page_content.strip() for doc in documents]
    assert "Content of the first archive" in contents[0], "Content of the first archive not found"
    assert "Second line" in contents[1], "Second line from the first archive not found"
    assert "Content of the second archive" in contents[2], "Content of the second archive not found"

def test_recursive_loader_mixed_content(tmp_path):
    """
    Checks the operation of RecursiveLoader when the directory contains:
      - Several regular files (.txt, .md)
      - Subdirectories with other files
      - Zip archives containing files
    """
    import zipfile

    # Create TXT and MD files in the root directory
    txt_file_1 = tmp_path / "sample1.txt"
    txt_file_1.write_text("Content of the first TXT file\nSecond line", encoding="utf-8")

    md_file_1 = tmp_path / "sample1.md"
    md_file_1.write_text("Content of the first MD file", encoding="utf-8")

    # Create a subdirectory and place another TXT file there
    sub_dir = tmp_path / "nested_folder"
    sub_dir.mkdir()
    txt_file_2 = sub_dir / "sample2.txt"
    txt_file_2.write_text("Content of the second TXT file\nAnother line", encoding="utf-8")

    # Create a nested zip archive with several text files inside
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("inside_zip_1.txt", "Data from the first file in the archive\nSecond line inside the archive")
        zf.writestr("inside_zip_2.md", "Data from the MD file in the archive")

    # Import RecursiveLoader (local import for the test is allowed)
    from documentor.loaders.recursive_loader import RecursiveLoader

    # Initialize RecursiveLoader for all interested extensions, including zip, and recursive traversal
    loader = RecursiveLoader(
        path=str(tmp_path),
        extension=["txt", "md", "zip"],
        is_recursive=True,
        use_unzip=True
    )

    # Load documents and verify results
    documents = list(loader.lazy_load())

    # Expect:
    # 2 lines from sample1.txt
    # 1 line from sample1.md
    # 2 lines from sample2.txt
    # 2 lines from inside_zip_1.txt
    # 1 line from inside_zip_2.md
    # Total: 2 + 1 + 2 + 2 + 1 = 8 documents
    assert len(documents) == 8, f"Expected 8 documents, got {len(documents)}."

    # Verify the presence of expected lines
    page_contents = [doc.page_content.strip() for doc in documents]
    assert any("Content of the first TXT file" in content for content in page_contents), \
        "Data from the first TXT file not found."
    assert any("Content of the second TXT file" in content for content in page_contents), \
        "Data from the second TXT file not found."
    assert any("Content of the first MD file" in content for content in page_contents), \
        "Data from the MD file in the root not found."
    assert any("Second line inside the archive" in content for content in page_contents), \
        "Second line from inside_zip_1.txt not found."
    assert any("Data from the MD file in the archive" in content for content in page_contents), \
        "MD file inside the archive not found."

    # Verify logs
    logs_info = loader.logs["info"]
    assert any("Reading file:" in msg for msg in logs_info), "Expected log about reading files."
    assert any("Processing ZIP archive:" in msg for msg in logs_info), "Expected log about processing ZIP archive."
