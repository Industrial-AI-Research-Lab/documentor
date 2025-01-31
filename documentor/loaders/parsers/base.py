from abc import abstractmethod

from langchain_core.document_loaders import BaseBlobParser as LangChainBaseBlobParser
from langchain_core.documents import Document
from typing import Iterator

from langchain_core.documents.base import Blob

from loaders.parsers.extension import BaseFileExtension


class BaseBlobParser(LangChainBaseBlobParser):
    """
    BaseParser - Abstract base class for all parsers.
    """

    @classmethod
    @abstractmethod
    def get_extension(cls) -> BaseFileExtension:
        """
        Returns the file extension associated with the parser.

        Returns:
            BaseFileExtension: The file extension associated with the parser.
        """
        pass

    @abstractmethod
    def lazy_parse(self, blob: Blob, **kwargs) -> Iterator[Document]:
        """
        Parses the raw data from a Blob object into one or more Document objects.

        Args:
            blob (Blob): A Blob object containing the raw data to be parsed.
            **kwargs: Additional keyword arguments for specific parser implementations.

        Returns:
            Document: A Document object containing the parsed data.
        """
        pass

    @abstractmethod
    def logs(self) -> dict[str, list[str]]:
        """
        Returns the logs collected during processing.

        Returns:
            dict[str, list[str]]: A dictionary containing lists of log messages for 'info', 'warning', and 'error'.
        """
        pass
