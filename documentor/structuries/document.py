from abc import ABC, abstractmethod
from typing import Iterator

import pandas as pd

from documentor.structuries.fragment import Fragment


class DocumentParsingException(Exception):
    """
    Exception for errors while parsing document from csv.
    """
    pass


class Document(ABC):
    """
    Abstract class for documents of any type. Documents consist of fragments.
    """
    _data: pd.DataFrame

    @abstractmethod
    def build_fragments(self) -> list[Fragment]:
        """
        List of fragments of Document.

        Note: if speed is important, it is preferable to use iter_rows method.

        :return: list of fragments
        :rtype: list[Fragment]
        """
        pass

    def iter_rows(self) -> Iterator[int | pd.Series]:
        """
        Iterate over all fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[int, pd.Series]
        """
        for ind, rows in self._data.iterrows():
            yield ind, rows

    def iter_all_str(self) -> Iterator[str]:
        """
        Iterate over all values of fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[str]
        """
        for fragment in self.fragments:
            yield fragment.__str__()

    @abstractmethod
    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to pandas DataFrame.

        :return: pandas DataFrame with data about fragments
        :rtype: pd.DataFrame
        """
        return self._data.copy()


class StructureNode(ABC):
    """
    Class for nodes with elements of hierarchical structure of document.
    """
    _children: list['StructureNode'] | None = None

    @property
    @abstractmethod
    def fragments(self) -> list[Fragment]:
        """
        Get all fragments of the node and its children.

        :return: list of fragments
        :rtype: list[Fragment]
        """
        pass

    def children(self) -> list['StructureNode'] | None:
        """
        Get children nodes of the node, if the node has children.
        Otherwise, return None.

        :return: children of the node or None
        :rtype: list[StructureNode] | None
        """
        if self._children is None:
            return None
        return self._children


class StructuredDocument(Document, ABC):
    """
    Abstract class for documents with hierarchical structure. Documents hierarchy is represented by tree.
    The document is a root of the tree.
    """
    _root: StructureNode

    @property
    def root(self) -> StructureNode:
        """
        Get root of hierarchical structure of document.

        :return: the root
        :rtype: StructureNode
        """
        return self._root
