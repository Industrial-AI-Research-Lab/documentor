from typing import Iterator

from langchain_core.documents import Document
from langchain_core.documents.base import Blob

from documentor.loaders.logger import Logger
from documentor.parsers.base import BaseBlobParser
from documentor.parsers.extensions import DocExtension


class TextBlobParser(BaseBlobParser):
    """
    Parser for text blobs.

    Attributes:
        batch_lines (int): The number of lines which is one Document.
            0 value means that whole text blob is one Document.
        _extension (set[DocExtension]): The set of file extensions associated with the parser. Not to be modified.
    """
    batch_lines = 0
    _extension = {DocExtension.txt}

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
                "file_type": file_type
            }
        )

    def _build_document(self, content: str, line_number: int, blob: Blob) -> Document:
        """
        Internal helper to remove repeated argument setup for _create_document.
        """
        file_name = blob.path.name if blob.path else None
        source = str(blob.path) if blob.path else None
        file_type = blob.path.suffix if blob.path else None
        return self._create_document(content, line_number, file_name, source, file_type)

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """
        Lazy parsing of text blobs.

        Args:
            blob (Blob): A Blob object containing the text data.

        Yields:
            Document: A Document object containing the parsed data.
        """
        try:
            text = blob.as_string()
            if self.batch_lines == 0:
                yield self._build_document(text, 0, blob)
            else:
                # Разбиваем текст на строки с сохранением переносов
                lines = text.splitlines(keepends=True)
                buffer = []
                line_count = 0
                
                for line_number, line in enumerate(lines):
                    buffer.append(line)
                    line_count += 1
                    
                    if line_count == self.batch_lines:
                        yield self._build_document(''.join(buffer), line_number - line_count + 1, blob)
                        buffer = []
                        line_count = 0

                if buffer:
                    start_line = len(lines) - len(buffer)
                    yield self._build_document(''.join(buffer), start_line, blob)

        except Exception as e:
            raise Exception(f"An error occurred: {e}") from e

