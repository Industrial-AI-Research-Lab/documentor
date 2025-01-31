from typing import Union, Iterator
from pathlib import Path
from overrides import overrides
from langchain_core.documents import Document
from loaders.structuries.base import BaseLoader


class RecursiveLoader(BaseLoader):
    """
    Loader for recursive directory
    """
    def __init__(self, file_path: Union[str, Path], 
                extension: list[str] = [], # Расширения файлов, которые будут загружены 
                recursive: bool = True, 
                zip_loader: bool = False, # Флаг для загрузки zip-файлов
                **kwargs):
        """
        Initialize the RecursiveLoader
        """
        pass

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
        Logs of the RecursiveLoader
        """
        return dict()

