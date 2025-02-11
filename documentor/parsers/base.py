from abc import abstractmethod
from typing import Iterator

from langchain_core.document_loaders import BaseBlobParser as LangChainBaseBlobParser
from langchain_core.documents import Document
from langchain_core.documents.base import Blob

from documentor.parsers.extensions import Extension


class BaseBlobParser(LangChainBaseBlobParser):
    """
    BaseParser - Abstract base class for all parsers.
    """
    _extensions: set[Extension]

    @classmethod
    def extensions(cls) -> set[Extension]:
        """
        Returns the file extension associated with the parser.

        Returns:
            set[Extension]: The file extension associated with the parser.
        """
        return cls._extensions

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """kwargs
        Parses the raw data from a Blob object into one or more Document objects.

        Args:
            blob (Blob): A Blob object containing the raw data to be parsed.

        Returns:
            Document: A Document object containing the parsed data.
        """
        raise NotImplementedError("Subclasses must implement lazy_parse method")
