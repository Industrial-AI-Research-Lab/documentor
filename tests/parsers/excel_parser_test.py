import pytest
from pathlib import Path
from langchain_core.documents import Document
from documentor.parsers.excel_parser import ExcelBlobParser
from langchain_core.documents.base import Blob
import openpyxl

def test_excel_parser_with_data(tmp_path):
    """
    Test to verify the correct operation of the ExcelBlobParser with real Excel data
    """
    file_path = tmp_path / "test.xlsx"
    
    # Create a test Excel file
    wb = openpyxl.Workbook()
    ws = wb.active
    ws['A1'] = 'Test'
    ws['B1'] = 'Data'
    ws['A2'] = '123'
    ws['B2'] = '456'
    wb.save(file_path)
    
    with open(file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            path=file_path  # Передаем объект Path напрямую, без преобразования в строку
        )
    
    parser = ExcelBlobParser()
    documents = list(parser.lazy_parse(blob))
    
    # Check basic expectations
    assert len(documents) > 0
    assert all(isinstance(doc, Document) for doc in documents)
    # Check the content
    assert 'Test;Data' in documents[0].page_content
    assert '123;456' in documents[0].page_content

def test_excel_parser_batch_processing(tmp_path):
    """
    Test for batch processing of rows
    """
    file_path = tmp_path / "test.xlsx"
    
    # Create a test Excel file
    wb = openpyxl.Workbook()
    ws = wb.active
    for i in range(1, 6):  # 5 rows of data
        ws[f'A{i}'] = f'Row{i}'
    wb.save(file_path)
    
    with open(file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            path=Path(file_path)
        )
    
    parser = ExcelBlobParser(batch_lines=2)  # Process 2 lines at a time
    documents = list(parser.lazy_parse(blob))
    
    assert len(documents) == 3  # We should get 3 documents (2+2+1 rows)

def test_excel_parser_invalid_file():
    """
    Test scenario when an incorrect file path is specified.
    Expect an OSError when opening a non-existent file.
    """
    parser = ExcelBlobParser()
    blob = Blob(
        data=b"invalid data",
        path=Path("non_existent.xlsx")
    )
    
    with pytest.raises(Exception):
        list(parser.lazy_parse(blob))

def test_excel_parser_complex_data(tmp_path):
    """
    Тест для проверки обработки сложных данных Excel, включая:
    - Множественные листы
    - Разные типы данных
    - Пустые ячейки
    - Форматированный текст
    """
    file_path = tmp_path / "test_complex.xlsx"
    
    # Создаем тестовый Excel файл с несколькими листами
    wb = openpyxl.Workbook()
    
    # Первый лист - разные типы данных
    ws1 = wb.active
    ws1.title = "Sheet1"
    test_data = [
        ["Text", "Number", "Empty", "Date"],
        ["Hello", 42, None, "2024-03-15"],
        ["World", 3.14, "", None],
        [None, 100, "Not Empty", "2024-03-16"]
    ]
    for row_idx, row_data in enumerate(test_data, 1):
        for col_idx, value in enumerate(row_data, 1):
            ws1.cell(row=row_idx, column=col_idx, value=value)
    
    # Второй лист - только текст
    ws2 = wb.create_sheet("Sheet2")
    text_data = [
        ["Name", "Description"],
        ["Product1", "Some description"],
        ["Product2", "Another description"]
    ]
    for row_idx, row_data in enumerate(text_data, 1):
        for col_idx, value in enumerate(row_data, 1):
            ws2.cell(row=row_idx, column=col_idx, value=value)
    
    wb.save(file_path)
    
    # Тестируем парсер
    with open(file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            path=file_path
        )
    
    parser = ExcelBlobParser()
    documents = list(parser.lazy_parse(blob))
    
    # Проверяем результаты
    assert len(documents) == 2  # Должно быть два документа (по одному на лист)
    
    # Проверяем первый лист
    sheet1_content = documents[0].page_content
    assert "Text;Number;Empty;Date" in sheet1_content
    assert "Hello;42" in sheet1_content
    assert "World;3.14" in sheet1_content
    
    # Проверяем второй лист
    sheet2_content = documents[1].page_content
    assert "Name;Description" in sheet2_content
    assert "Product1;Some description" in sheet2_content
    assert "Product2;Another description" in sheet2_content
    
    # Проверяем метаданные
    for doc in documents:
        assert doc.metadata["source"] == str(file_path)
        assert doc.metadata["file_name"] == "test_complex.xlsx"
        assert doc.metadata["extension"] == ".xlsx"

def test_excel_parser_batch_processing_multiple_sheets():
    """
    Тест для проверки пакетной обработки Excel файла с несколькими листами
    """
    file_path = Path("tests/parsers/data/test_excel.xlsx")
    
    with open(file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            path=file_path
        )
    
    parser = ExcelBlobParser(batch_lines=2)
    documents = list(parser.lazy_parse(blob))
    
    # Проверяем результаты
    assert len(documents) > 0
    
    # Проверяем метаданные
    for doc in documents:
        assert doc.metadata["source"] == str(file_path)
        assert doc.metadata["file_name"] == "test_excel.xlsx"
        assert doc.metadata["extension"] == ".xlsx"
    
    # Проверяем содержимое документов
    first_doc = documents[0]
    assert isinstance(first_doc, Document)
    assert len(first_doc.page_content) > 0
    
    # Проверяем, что документы разделены правильно по batch_lines
    for doc in documents:
        content_lines = doc.page_content.strip().split('\n')
        assert len(content_lines) <= 2  # проверяем, что в каждом документе не более 2 строк

def test_excel_parser_real_data():
    """
    Тест для проверки парсинга Excel файла с несколькими листами
    """
    file_path = Path("tests/parsers/data/test_excel.xlsx")
    
    with open(file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            path=file_path
        )
    
    parser = ExcelBlobParser()
    documents = list(parser.lazy_parse(blob))
    
    # Проверяем, что получили документы
    assert len(documents) > 0
    
    # Проверяем, что каждый документ содержит данные
    for doc in documents:
        assert isinstance(doc, Document)
        assert doc.page_content.strip()  # Проверяем, что контент не пустой
        
        # Проверяем метаданные
        assert doc.metadata["source"] == str(file_path)
        assert doc.metadata["file_name"] == "test_excel.xlsx"
        assert doc.metadata["extension"] == ".xlsx"
        assert isinstance(doc.metadata["line_number"], int)

def test_excel_parser_batch_processing_real_data():
    """
    Тест для проверки пакетной обработки Excel файла
    """
    file_path = Path("tests/parsers/data/test_excel.xlsx")
    batch_size = 2
    
    with open(file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            path=file_path
        )
    
    parser = ExcelBlobParser(batch_lines=batch_size)
    documents = list(parser.lazy_parse(blob))
    
    # Проверяем, что получили документы
    assert len(documents) > 0
    
    # Проверяем размер батчей
    for doc in documents:
        content_lines = doc.page_content.strip().split('\n')
        assert len(content_lines) <= batch_size
        
        # Проверяем, что каждая строка содержит данные
        for line in content_lines:
            assert line.strip()
        
        # Проверяем метаданные
        assert doc.metadata["source"] == str(file_path)
        assert doc.metadata["file_name"] == "test_excel.xlsx"
        assert doc.metadata["extension"] == ".xlsx"
        assert isinstance(doc.metadata["line_number"], int)

def test_excel_parser_empty_sheet():
    """
    Тест для проверки обработки пустого листа Excel.
    Парсер должен пропускать пустые листы и не создавать для них документы.
    """
    file_path = Path("tests/parsers/data/test_empty.xlsx")

    # Создаем Excel файл с пустым листом
    wb = openpyxl.Workbook()
    wb.save(file_path)

    with open(file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            path=file_path
        )

    parser = ExcelBlobParser()
    documents = list(parser.lazy_parse(blob))

    # Проверяем, что не получили документов, так как лист пустой
    assert len(documents) == 0

def test_excel_parser_multiple_sheets(tmp_path):
    """
    Тест для проверки обработки файла с несколькими листами
    """
    file_path = tmp_path / "test_multiple.xlsx"
    
    # Создаем Excel файл с двумя листами
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1['A1'] = 'Sheet1 Data'
    
    ws2 = wb.create_sheet("Sheet2")
    ws2['A1'] = 'Sheet2 Data'
    
    wb.save(file_path)
    
    with open(file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            path=file_path
        )
    
    parser = ExcelBlobParser()
    documents = list(parser.lazy_parse(blob))
    
    # Проверяем, что получили два документа
    assert len(documents) == 2
    assert all(isinstance(doc, Document) for doc in documents)
    assert all(doc.page_content.strip() for doc in documents)

def test_print_sheet3_content():
    """
    Тест для вывода содержимого третьего листа Excel файла
    """
    file_path = Path("tests/parsers/data/test_excel.xlsx")
    
    # Открываем файл напрямую через openpyxl для просмотра данных
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet3 = wb["Лист3"]
    
    print("\nСодержимое Лист3:")
    print("-" * 50)
    
    # Выводим все значения из ячеек с координатами
    for row_idx, row in enumerate(sheet3.iter_rows(values_only=True), 1):
        for col_idx, cell in enumerate(row, 1):
            if cell is not None and str(cell).strip():
                col_letter = openpyxl.utils.get_column_letter(col_idx)
                print(f"Ячейка {col_letter}{row_idx}: {cell}")
    
    print("-" * 50)

def test_excel_parser_empty_and_data_sheets():
    """
    Тест для проверки обработки Excel файла с разными типами листов:
    - пустые листы
    - листы с данными
    - листы с пробелами и None значениями
    
    Использует реальный файл test_excel.xlsx
    """
    file_path = Path("tests/parsers/data/test_excel.xlsx")
    
    with open(file_path, 'rb') as f:
        blob = Blob(
            data=f.read(),
            path=file_path
        )
    
    parser = ExcelBlobParser()
    documents = list(parser.lazy_parse(blob))
    
    # Проверяем количество документов
    # Должно быть 4 документа (все листы кроме пустого Лист3)
    assert len(documents) == 4
    
    # Проверяем содержимое каждого документа
    doc_contents = [doc.page_content for doc in documents]
    
    # Проверяем первый лист (числовые данные)
    first_sheet_values = ["1", "2", "3", "4", "5", "6", "7", "8", "blablabla", "4523452"]
    assert any(all(value in content for value in first_sheet_values) for content in doc_contents)
    
    # Проверяем второй лист (буквенные данные)
    second_sheet_values = ["a", "b", "c", "d", "e", "f", "453"]
    assert any(all(value in content for value in second_sheet_values) for content in doc_contents)
    
    # Проверяем четвертый лист (повторяющиеся данные)
    assert any("abcd" in content and "1" in content for content in doc_contents)
    
    # Проверяем пятый лист (разреженные данные)
    assert any("test" in content and "stse" in content for content in doc_contents)
    
    # Проверяем метаданные для всех документов
    for doc in documents:
        assert doc.metadata["source"] == str(file_path)
        assert doc.metadata["file_name"] == "test_excel.xlsx"
        assert doc.metadata["extension"] == ".xlsx"
