from itertools import zip_longest
from typing import Iterator

from langchain_core.documents import Document
from langchain_core.documents.base import Blob

from documentor.parsers.base import BaseBlobParser
from documentor.parsers.extensions import DocExtension
from documentor.parsers.config import ParsingSchema
from documentor.structuries.metadata import Metadata, to_document_metadata


class TextBlobParser(BaseBlobParser):
    """
    Parser for plain-text blobs.

    Attributes:
        batch_lines (int): Number of lines to include in a single Document.
            A value of 0 means the entire text blob is returned as one Document.
        _extension (set[DocExtension]): Supported file extensions. Do not modify at runtime.
    """
    batch_lines = 0
    _extension = {DocExtension.txt}
    _available_parsing_schemas = {ParsingSchema.lines, ParsingSchema.full}

    def __init__(self, batch_lines: int = 0, **kwargs) -> None:
        """
        Initialize a TextBlobParser.

        Args:
            batch_lines (int): Number of lines per Document. 0 means the whole text.
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
        Create a Document with consistent metadata fields.

        Args:
            content (str): Text content of the document.
            line_number (int): Starting line number within the file.
            file_name (str): Name of the file or None.
            source (str): Full source path or identifier or None.
            file_type (str): File extension (e.g., ".txt") or None.

        Returns:
            Document: The created document.
        """
        # Build unified metadata via documentor.structuries.metadata
        meta = Metadata(
            name=file_name,
            extension=file_type,
            source=self._current_blob if hasattr(self, "_current_blob") else None,
            line_number=line_number,
        )
        metadata_dict = to_document_metadata(
            meta,
            extension_key="file_type",  # keep backward compatibility with existing tests
            name_key="file_name",
        )
        # Override source string when explicit source is provided in args
        if source is not None:
            metadata_dict["source"] = source
        return Document(
            page_content=content,
            metadata=metadata_dict,
        )

    def _build_document(self, content: str, line_number: int, blob: Blob) -> Document:
        """
        Build a Document by extracting file-related metadata from the Blob.
        """
        # Save blob to use inside _create_document for Metadata.source
        self._current_blob = blob
        file_name = blob.path.name if blob.path else None
        source = str(blob.path) if blob.path else None
        file_type = blob.path.suffix if blob.path else None
        doc = self._create_document(content, line_number, file_name, source, file_type)
        # Cleanup attribute to avoid accidental reuse
        if hasattr(self, "_current_blob"):
            delattr(self, "_current_blob")
        return doc

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """
        Lazily parse a text blob into one or more Document objects.

        Args:
            blob (Blob): A blob containing the raw text data.

        Yields:
            Document: Parsed document chunks.
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
            cls_name = self.__class__.__name__
            raise Exception(f"{cls_name} failed to parse blob: {e}") from e
