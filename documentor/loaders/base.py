from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, Optional

from langchain_core.document_loaders import BaseLoader as LangChainBaseLoader
from langchain_core.documents import Document

from documentor.loaders.logger import LoaderLogger
from parsers.extension_mapping import ExtensionMapping


class BaseLoader(LangChainBaseLoader, ABC):
    """
    BaseLoader - Abstract base class for all loaders.

    Attributes:
        path (str | Path): A path to the file or directory from which data will be loaded.
    """
    path: str | Path
    _logs: LoaderLogger
    _extension_mapping: ExtensionMapping  # Extension mapping for choosing the correct parser

    @abstractmethod
    def __init__(self, path: str | Path, extension_mapping: Optional[ExtensionMapping] = None, **kwargs):
        """
        Initializes the base functionality of all loaders.

        Args:
            path (str | Path): path to files, or directory, or zip file

        Raises:
            ValueError: If the path is not a string or Path object.
        """
        if extension_mapping is None:
            extension_mapping = ExtensionMapping()
        if isinstance(path, str):
            path = Path(path)

        self._extension_mapping = extension_mapping
        self.path = path
        self._logs = LoaderLogger()

    @abstractmethod
    def lazy_load(self) -> Iterator[Document]:
        """
        Lazy loading interface.

        Subclasses are required to implement this method.

        Returns:
            Generator of documents
        """
        raise NotImplementedError("Subclasses must implement lazy_load method")

    @property
    def logs(self) -> dict[str, list[str]]:
        """
        Attribute with logs saved during the loading process
        """
        return self._logs.get_all_logs()
