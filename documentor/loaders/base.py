from typing import Iterator
from pathlib import Path
from abc import ABC, abstractmethod
from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader as LangChainBaseLoader


class BaseLoader(LangChainBaseLoader, ABC):
    """
    BaseLoader - Abstract base class for all loaders.

    Attributes:
        file_path (str | Path): A path to the file or directory from which data will be loaded.
    """
    file_path: str | Path

    @abstractmethod
    def __init__(self, file_path: str | Path, **kwargs):
        """
        Initializes the base functionality of all loaders.

        Args:
            file_path (str | Path): Required parameter specifying the file system path where data
                will be loaded from or used to determine the appropriate loader type.
        """
        pass

    @abstractmethod
    def lazy_load(self) -> Iterator[Document]:
        """
        Lazy loading of documents
        """
        pass

    @property
    @abstractmethod
    def logs(self) -> dict[str, list[str]]:
        """
        Attribute with logs saved during the loading process
        """
        pass
