import openpyxl
import pandas as pd
from typing import Iterator
from io import BytesIO
from langchain_core.documents import Document
from langchain_core.documents.base import Blob
from documentor.parsers.base import BaseBlobParser
from documentor.parsers.extensions import DocExtension
from documentor.loaders.logger import Logger



class ExcelBlobParser(BaseBlobParser):
    """
    Parser for Excel files for LangChain.
    Creates a separate Document for each sheet with a text representation of the table
    and saves metadata from the original parser.
    """
    batch_lines = 0

    _extension = {DocExtension.xlsx, DocExtension.xls}


    def __init__(self, batch_lines: int = 0):
        """
        Initialize the TextBlobParser.

        Args:
            batch_lines (int): The number of lines which is one Document.
                0 value means that whole text blob is one Document. Value should be greater than or equal to 0.
            Defaults to 0.
        """
        if not isinstance(batch_lines, int) or batch_lines < 0:
            raise ValueError("batch_lines must be a non-negative integer.")
        self.batch_lines = batch_lines
        self._logs = Logger()
    
    def _create_document(self, content: str, line_number: int, file_name: str, source: str, file_type: str) -> Document:
        """
        Helper method to create a Document object.

        Args:
            content (str): Content of the document.
            line_number (int): Line number in the file.
            file_name (str): Name of the file.
            source (str): Source path or identifier.
            file_type (str): Type of the file.

        Returns:
            Document: The created document.
        """
        # TODO decide which metadata should be used
        return Document(
            page_content=content,
            metadata={
                "line_number": line_number,
                "file_name": file_name,
                "source": source,
                "extension": file_type,
            }
        )
    def _build_document(self, content: str, line_number: int, blob: Blob) -> Document:
        """
        Internal helper to remove repeated argument setup for _create_document.
        
        Args:
            content (str): Content of the document.
            line_number (int): Line number in the file.
            blob (Blob): A Blob object containing the raw data to be parsed.

        Returns:
            Document: A Document object containing the parsed data.
        """
        file_name = blob.path.name if blob.path else None
        source = str(blob.path) if blob.path else None
        file_type = blob.path.suffix if blob.path else None
        return self._create_document(content, line_number, file_name, source, file_type)



    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """
        Creates a list of Document objects from an Excel file, one per sheet.

        Args:
            blob (Blob): Blob object containing Excel file data
        Returns:
            Iterator[Document]: Iterator of Document objects
        Raises:
            Exception: if parsing fails
        """
        try:
            excel_data = BytesIO(blob.data)
            wb = openpyxl.load_workbook(excel_data, data_only=True)
            
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                rows = []
                
                for row in sheet.iter_rows(values_only=True):
                    # Проверяем, содержит ли строка хотя бы одно непустое значение
                    if any(cell is not None and str(cell).strip() != '' for cell in row):
                        row_content = [str(cell) if cell is not None else '' for cell in row]
                        rows.append(row_content)
                
                if rows:  # Создаем документ только если есть данные
                    df = pd.DataFrame(rows)
                    csv_content = df.to_csv(sep=';', index=False, header=False)
                    lines = csv_content.splitlines()

                    if self.batch_lines == 0:
                        yield self._build_document(csv_content, 0, blob)
                    else:
                        buffer = []
                        for line_number, line in enumerate(lines):
                            buffer.append(line)
                            if len(buffer) == self.batch_lines:
                                yield self._build_document("\n".join(buffer), line_number - self.batch_lines + 1, blob)
                                buffer = []
                        if buffer:
                            start_line = len(lines) - len(buffer)
                            yield self._build_document("\n".join(buffer), start_line, blob)

        except Exception as e:
            raise Exception(f"An error occurred while parsing Excel file: {str(e)}") from e
