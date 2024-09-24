from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import pandas as pd

from documentor.structuries.fragment import Fragment


@dataclass(frozen=True)
class StructureNode(ABC):
    """
    Class for nodes with elements of hierarchical structure of document.
    """
    _children: Optional[list['StructureNode']] = None
    _parents: Optional[list['StructureNode']] = None
    _value: Optional[pd.Series] = None

    @property
    @abstractmethod
    def fragments(self) -> list[Fragment]:
        """
        Get all fragments of the node and its children.

        :return: list of fragments
        :rtype: list[TextFragment]
        """
    @property
    def children(self) -> Optional[list['StructureNode']]:
        """
        Get children nodes of the node, if the node has children.
        Otherwise, return None.

        :return: children of the node or None
        :rtype: list[StructureNode] | None
        """
        if self._children is None:
            return None
        return self._children


@dataclass(frozen=True)
class DocumentStructure:
    root: StructureNode

