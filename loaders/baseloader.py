from typing import Union, Iterator
from pathlib import Path
from abc import ABC, abstractmethod
from documentor.structuries.document import Document


class BaseLoader(ABC):
    """
    Base parent class for all loaders   
    """
    @abstractmethod
    def __init__(self, file_path: Union[str, Path], **kwargs):
        """
        Base initialization of all loaders
        :param file_path: a required parameter with the path in the file system from where you want to load
                          or by which the required type of loader can be determined
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
