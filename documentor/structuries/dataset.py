from abc import ABC, abstractmethod
from typing import Iterator

from documentor.structuries.document import TextDocument
from documentor.text.fragment import TextFragment


class Docset(ABC):
    """
    Abstract class for dataset of documents.

    :param in_memory: if True, all documents will be loaded into memory,
    otherwise documents will be loaded on request one by one
    :type in_memory: bool
    """
    in_memory: bool = True

    @property
    @abstractmethod
    def iter_doc(self) -> Iterator[TextDocument]:
        """
        List of documents of dataset.


        :return: of documents
        :rtype: list[TextDocument]
        """
        pass

    def iter_all(self) -> Iterator[TextFragment]:
        """
        Iterate over all fragments of all documents of the dataset.
        :return: all fragments
        :rtype: Iterator[TextFragment]
        """
        for document in self.iter_doc:
            for fragment in document.iter_all():
                yield fragment

    def iter_all_str(self) -> Iterator[str]:
        """
        Iterate over all values of fragments of all documents of the dataset.
        :return: all fragments
        :rtype: Iterator[str]
        """
        for document in self.iter_doc:
            for values in document.iter_all_str():
                yield values
