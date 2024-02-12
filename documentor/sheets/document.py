from abc import ABC
from typing import Iterator

import pandas as pd

from documentor.abstract.document import Document, StructureNode
from documentor.abstract.fragment import Fragment
from documentor.sheets.fragment import SheetFragment


class DocumentParsingException(Exception):
    """
    Exception for errors while parsing document from csv.
    """
    pass


class SheetDocument(Document):
    """

    """
    doc_df = pd.DataFrame(columns=['Content', 'Start_content', 'Relative_Id', 'Type', 'Row', 'Column',
                                   'Length', 'Vertically_merged', 'Horizontally_merged', 'Font_selection', 'Top_border',
                                   'Bottom_border', 'Left_border', 'Right_border', 'Color', 'Is_Formula'])

    def __init__(self, df: pd.DataFrame):
        self.doc_df = df

    @property
    def fragments(self) -> list[SheetFragment]:
        """
        List of fragments of Document.

        :return: list of fragments
        :rtype: list[Fragment]
        """
        return self.doc_df.to_list()

    def iter_all(self) -> Iterator[Fragment]:
        """
        Iterate over all fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[Fragment]
        """
        for fragment in self.fragments:
            yield fragment

    def iter_all_str(self) -> Iterator[str]:
        """
        Iterate over all values of fragments of the Document.

        :return: the document fragments
        :rtype: Iterator[str]
        """
        for fragment in self.fragments:
            yield fragment.__str__()

    def to_df(self) -> pd.DataFrame:
        """
        Convert Document to pandas DataFrame.

        :return: pandas DataFrame with data about fragments
        :rtype: pd.DataFrame
        """
        return self.doc_df


class SheetStructureNode(StructureNode):
    """
    Class for nodes with elements of hierarchical structure of document.
    """
    _children: list['StructureNode'] | None = None

    @property
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
