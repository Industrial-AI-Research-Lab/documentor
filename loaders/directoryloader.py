from typing import Union, Iterator
from loaders.baseloader import BaseLoader
from overrides import overrides


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
        return dict()


