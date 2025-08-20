from itertools import zip_longest
from typing import Iterator

from langchain_core.documents import Document
from langchain_core.documents.base import Blob

from documentor.parsers.base import BaseBlobParser
from documentor.parsers.extensions import DocExtension
from documentor.parsers.config import ParsingSchema


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
    _available_parsing_schemas = {ParsingSchema.lines, ParsingSchema.full}

    def __init__(self, batch_lines: int = 0, **kwargs) -> None:
        """
        Initialize TextBlobParser.

        Args:
            batch_lines (int): Number of lines per Document. 0 means whole text.
        """
        # Validate batch_lines
        if not isinstance(batch_lines, int):
            raise ValueError("batch_lines must be an integer")
        if batch_lines < 0:
            raise ValueError("batch_lines must be non-negative")
        self.batch_lines = batch_lines
        super().__init__(**kwargs)

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
            # If batch_lines is 0, return the whole text as a single document
            if self.batch_lines == 0:
                yield self._build_document(text, 0, blob)
                return

            # Otherwise, split by lines into batches of size batch_lines
            lines = text.splitlines(keepends=True)
            for start in range(0, len(lines), self.batch_lines):
                batch = lines[start:start + self.batch_lines]
                content = ''.join(batch)
                yield self._build_document(content, start, blob)
        except Exception as e:
            raise Exception(f"An error occurred: {e}") from e
