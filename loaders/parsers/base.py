from abc import ABC, abstractmethod
from langchain_core.documents import Document
from pathlib import Path
from typing import Iterator

class BaseParser(ABC):
    """
    BaseParser - Abstract base class for all parsers.
    """
    @abstractmethod
    def __init__(self, 
                 file_path: str|Path, 
                 **kwargs):
        """
        Initializes the base functionality of all parsers.

        Args:
            file_path (str | Path): Required parameter specifying the file system path where data
                will be loaded from or used to determine the appropriate parser type.
        """
        pass
       
    @abstractmethod
    def parse(self, file_path: str|Path, **kwargs) -> Iterator[Document]:
        """
        Parses the file at the given path and returns a Document object.

        Args:
            file_path (str | Path): The path to the file to be parsed.
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
