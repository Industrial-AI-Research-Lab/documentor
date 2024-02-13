from abc import ABC, abstractmethod

from documentor.structuries.document import TextDocument
from documentor.text.fragment import TextFragment


class StructureNode(ABC):
    """
    Class for nodes with elements of hierarchical structure of document.
    """
    _children: list['StructureNode'] | None = None

    @property
    @abstractmethod
    def fragments(self) -> list[TextFragment]:
        """
        Get all fragments of the node and its children.

        :return: list of fragments
        :rtype: list[TextFragment]
        """

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


class StructuredDocument(TextDocument, ABC):
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