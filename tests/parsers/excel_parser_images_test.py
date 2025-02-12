import pytest
import openpyxl
from io import BytesIO
from pathlib import Path
from langchain_core.documents.base import Blob
from documentor.parsers.excel_parser import ExcelBlobParser
import os
from PIL import Image

def load_test_excel():
    """Loads the test Excel file."""
    test_file_path = Path("tests/parsers/data/test_excel.xlsx")
    with open(test_file_path, "rb") as f:
        return Blob(data=f.read(), path=test_file_path)

@pytest.fixture
def sample_excel_blob():
    """Fixture for providing the test Excel file."""
    return load_test_excel()

def test_parse_excel(sample_excel_blob):
    """Checks the parsing of textual data from the Excel file."""
    parser = ExcelBlobParser()
    documents = list(parser.lazy_parse(sample_excel_blob))
    
    assert len(documents) > 0, "There should be at least one document"
    assert any(";" in doc.page_content for doc in documents), "Data should be in CSV format"

def test_extract_images(sample_excel_blob, tmp_path):
    """Checks the extraction of images from the third sheet of the test Excel file."""
    parser = ExcelBlobParser(parse_images=True)
    
    current_dir = Path.cwd()
    try:
        os.chdir(tmp_path)
        list(parser.lazy_parse(sample_excel_blob))
        image_files = list(tmp_path.glob("*.png"))
        assert len(image_files) > 0, "Images should be extracted"
        
        for img_file in image_files:
            print(img_file.name)
            assert "Лист3" in img_file.name, "The image file name should match the third sheet"
    finally:
        os.chdir(current_dir)

def test_show_extracted_images(sample_excel_blob, tmp_path):
    """
    Test to demonstrate the extracted images.
    Saves the images and their information to a file.
    """
    parser = ExcelBlobParser()
    
    output_dir = tmp_path / "extracted_images"
    output_dir.mkdir(exist_ok=True)
    
    project_root = Path.cwd()
    results_dir = project_root / "tests" / "parsers" / "data"
    results_dir.mkdir(exist_ok=True, parents=True)
    
    current_dir = Path.cwd()
    try:
        os.chdir(output_dir)
        list(parser.lazy_parse(sample_excel_blob))
        image_files = list(output_dir.glob("*.png"))
        permanent_dir = results_dir / "extracted_images"
        permanent_dir.mkdir(exist_ok=True, parents=True)
        for img_file in image_files:
            permanent_path = permanent_dir / img_file.name
            img = Image.open(img_file)
            img.save(permanent_path)
    finally:
        os.chdir(current_dir)

if __name__ == "__main__":
    pytest.main()

# do not pay attention on false test results
