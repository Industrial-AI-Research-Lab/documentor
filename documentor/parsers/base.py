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
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """kwargs
        Parses the raw data from a Blob object into one or more Document objects.

        Args:
            blob (Blob): A Blob object containing the raw data to be parsed.

        Returns:
            Document: A Document object containing the parsed data.
        """
        pass
