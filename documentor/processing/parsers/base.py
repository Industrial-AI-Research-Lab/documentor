from abc import abstractmethod
from typing import Iterator, Optional

from langchain_core.document_loaders import BaseBlobParser as LangChainBaseBlobParser
from langchain_core.documents import Document
from langchain_core.documents.base import Blob

from documentor.parsers.extensions import Extension
from documentor.loaders.logger import LoaderLogger
from documentor.parsers.config import ParsingConfig, ParsingSchema


class BaseBlobParser(LangChainBaseBlobParser):
    """
    Abstract base class for all blob parsers.
    """
    _extensions: set[Extension]
    _available_parsing_schemas: set[ParsingSchema] = set()

    def __init__(self, config: Optional[ParsingConfig] = None, logger: Optional[LoaderLogger] = None, **kwargs) -> None:
        """
        Initialize a parser instance.

        Args:
            config (Optional[ParsingConfig]): Parser configuration with the desired parsing schema and options.
        """
        self.config = config or ParsingConfig()
        if self.config.parsing_schema not in self._available_parsing_schemas:
            raise ValueError(f"Invalid parsing schema: {self.config.parsing_schema}")
        self._logs = logger or LoaderLogger()

    @classmethod
    def extensions(cls) -> set[Extension]:
        """
        Return the set of file extensions associated with this parser.

        Returns:
            set[Extension]: Supported file extensions.
        """
        return cls._extensions

    @abstractmethod
    def _create_document(self, content: str, line_number: int, file_name: str, source: str, file_type: str) -> Document:
        """
        Create a Document object with unified metadata.

        Args:
            content (str): Text content of the document.
            line_number (int): Starting line number within the source.
            file_name (str): Source file name.
            source (str): Full source path or identifier.
            file_type (str): File extension including the leading dot.

        Returns:
            Document: The created document.
        """
        pass

    @abstractmethod
    def _build_document(self, content: str, line_number: int, blob: Blob) -> Document:
        """
        Prepare a Document by deriving metadata from the given Blob.

        Args:
            content (str): Text content of the document.
            line_number (int): Starting line number within the source.
            blob (Blob): Raw data container to be parsed.

        Returns:
            Document: A Document object containing the parsed data.
        """
        pass

    @abstractmethod
    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        """
        Parse the raw data from a Blob into one or more Document objects.

        Args:
            blob (Blob): Raw data container to be parsed.

        Yields:
            Document: Documents produced from the blob.
        """
        raise NotImplementedError("Subclasses must implement lazy_parse method")
