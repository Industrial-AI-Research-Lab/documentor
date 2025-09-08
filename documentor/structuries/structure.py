from abc import ABC, abstractmethod
from collections.abc import Hashable
from dataclasses import dataclass
from itertools import chain
from typing import Optional

import pandas as pd

from documentor.structuries.fragment import Fragment
from structuries.fragment import HeaderFragment


@dataclass(frozen=True)
class StructureNode:
    """
    Class for nodes with elements of the hierarchical structure of a document.
    """
    children: list['StructureNode'] | None = None
    value: Fragment | None = None

    @property
    def fragments(self) -> list[Fragment]:
        """
        Get all leaf fragments of the node and its children.

        Returns:
            list[Fragment]: List of fragments.
        """
        ans = []
        if self.children is None:
            ans = [self.value] if self.value is not None else []
        else:
            ans = list(chain(c.fragments for c in self.children))
        return ans

    def structure(self, level: int = 0) -> list[tuple[Fragment, int]]:
        """
        Get all fragments and their levels in the document structure.
        Args:
            level: int = 0 - current level

        Returns:
            structure: list[tuple[Fragment, int]] - list of tuples with fragment and level

        """
        ans = [(self.value, level)] if self.value is not None else []
        if self.children:
            ans += list(chain(c.structure(level + 1) for c in self.children))
        return ans


@dataclass(frozen=True)
class DocumentStructure:
    root: StructureNode

    @property
    def structure(self) -> list[tuple[Fragment, int]]:
        return self.root.structure()

    def fragments(self) -> list[Fragment]:
        return self.root.fragments

    def previous(self, fragment: Fragment | str) -> Optional[Fragment]:
        """
        Find the previous fragment (or fragment id) in the document in the current hierarchy level.
        Returns None if the fragment is the first one in the hierarchy.
        """
        pass

    def next(self, fragment: Fragment | str) -> Optional[Fragment]:
        """
        Find the next fragment (or fragment id) in the document in the current hierarchy level.
        Returns None if the fragment is the last one in the hierarchy.
        Args:
            fragment:

        Returns:

        """
        pass

    def get_fragment_by_id(self, fragment_id: str) -> Optional[Fragment]:
        pass

    def get_fragment_by_content(self, content: Hashable) -> Optional[Fragment]:
        pass

    def parent(self, fragment: Fragment | str) -> Optional[Fragment]:
        pass

    def children(self, fragment: Fragment | str) -> list[Fragment]:
        pass

    def hierarchy(self):
        pass

    def is_leaf(self, fragment: Fragment | str) -> bool:
        pass

    def is_header(self, fragment: Fragment | str) -> bool:
        pass

    def get_level(self, fragment: Fragment | str) -> int:
        pass
