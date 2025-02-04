from abc import abstractmethod

from langchain_core.document_loaders import BaseBlobParser as LangChainBaseBlobParser
from langchain_core.documents import Document
from typing import Iterator

from langchain_core.documents.base import Blob

from loaders.parsers.extensions import DocExtension


class BaseParserType:
    """
    BaseParserType - Abstract base class for extensions which can be associated with a parser.
    """

    @classmethod
    @abstractmethod
    def get_extensions(cls) -> set[DocExtension]:
        """
        Returns the file extension associated with the parser.

        Returns:
            set[DocExtension]: The file extension associated with the parser.
        """
        pass

    def is_in(self, extension: str | DocExtension) -> bool:
        """
        Check if the extension is in the set of extensions.

        Args:
            extension (str): The extension to check.

        Returns:
            bool: True if the extension is in the set of extensions, False otherwise.
        """
        return extension in self.get_extensions()


class BaseBlobParser(LangChainBaseBlobParser):
    """
    BaseParser - Abstract base class for all parsers.
    """

    @classmethod
    @abstractmethod
    def get_type(cls) -> BaseParserType:
        """
        Returns the type of the parser. This is used to determine which parser to use for a given file.
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
        pass
