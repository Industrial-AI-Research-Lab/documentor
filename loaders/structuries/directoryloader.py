from typing import Union, Iterator
from pathlib import Path
from loaders.structuries.base import BaseLoader
from overrides import overrides
from langchain_core.documents import Document

class DirectoryLoader(BaseLoader):
    """
    Loader for directory
    """
    def __init__(self, file_path: Union[str, Path], **kwargs):
        super().__init__(file_path, **kwargs)
        self.file_path = file_path

    @overrides
    def lazy_load(self) -> Iterator[Document]:
        """
        Lazy loading of documents
        """
        pass


    @property
    @overrides
    def logs(self) -> dict[str, list[str]]:
        """
        Logs of the DirectoryLoader
        """
        return dict()


