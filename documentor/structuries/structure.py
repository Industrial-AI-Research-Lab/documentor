from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import pandas as pd

from documentor.structuries.fragment import TextFragment


@dataclass(frozen=True)
class StructureNode(ABC):
    """
    Class for nodes with elements of the hierarchical structure of a document.
    """
    _children: Optional[list['StructureNode']] = None
    _parents: Optional[list['StructureNode']] = None
    _value: Optional[pd.Series] = None
    _fragment: Optional[TextFragment] = None

    @property
    @abstractmethod
    def next(self) -> Optional['StructureNode']:
        """
        Returns the next hierarchical structure node on the same level.

        Returns:
            next hierarchical structure node
        """
        pass

    @property
    @abstractmethod
    def previous(self) -> Optional['StructureNode']:
        """
        Returns the previous hierarchical structure node on the same level.

        Returns:
            previous hierarchical structure node
        """
        pass

    @property
    @property
    @abstractmethod
    def fragments(self) -> list[TextFragment]:
        """
        Get all fragments of the node and its children.

        Returns:
            list[TextFragment]: List of fragments.
        """
        pass

    @property
    def children(self) -> Optional[list['StructureNode']]:
        """
        Get children nodes of the node if the node has children. Otherwise, return None.

        Returns:
            list[StructureNode] | None: Children of the node or None.
        """
        if self._children is None:
            return None
        return self._children

    @property
    def value(self) -> Optional[TextFragment]:
        return self._value


@dataclass(frozen=True)
class DocumentStructure:
    root: StructureNode
