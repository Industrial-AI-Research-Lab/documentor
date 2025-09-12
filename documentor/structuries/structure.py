from collections.abc import Hashable
from dataclasses import dataclass, field
from itertools import chain
from typing import Optional

import pandas as pd

from .fragment import Fragment, HeaderFragment


@dataclass(frozen=True)
class StructureNode:
    """Node of a document hierarchy.

    Attributes:
        children: Child nodes. An empty list marks a leaf.
        value: Associated fragment or ``None`` for synthetic roots.
    """

    children: list["StructureNode"] = field(default_factory=list)
    value: Fragment | None = None

    @property
    def fragments(self) -> list[Fragment]:
        """Return all leaf fragments within this subtree.

        Returns:
            list[Fragment]: Collected leaf fragments.
        """

        if not self.children:
            return [self.value] if self.value is not None else []
        return list(chain.from_iterable(c.fragments for c in self.children))

    def structure(self, level: int = 0) -> list[tuple[Fragment, int]]:
        """Return ``(fragment, level)`` pairs for the subtree.

        Args:
            level (int, optional): Starting level for this node. Defaults to ``0``.

        Returns:
            list[tuple[Fragment, int]]: Fragment and its hierarchy level.
        """

        ans = [(self.value, level)] if self.value is not None else []
        if self.children:
            ans += list(chain.from_iterable(c.structure(level + 1) for c in self.children))
        return ans


@dataclass(frozen=True)
class DocumentStructure:
    """Hierarchical structure of document fragments.

    The class precomputes various relations between fragments to provide
    ``O(1)`` access to neighbours, parents, children and other metadata.

    Attributes:
        root: Root node of the hierarchy.
    """

    root: StructureNode
    _id_to_node: dict[str, StructureNode] = field(init=False, repr=False)
    _id_to_parent: dict[str, Optional[str]] = field(init=False, repr=False)
    _id_to_children: dict[str, list[str]] = field(init=False, repr=False)
    _content_to_id: dict[Hashable, str] = field(init=False, repr=False)
    _id_to_prev: dict[str, Optional[str]] = field(init=False, repr=False)
    _id_to_next: dict[str, Optional[str]] = field(init=False, repr=False)
    _id_to_level: dict[str, int] = field(init=False, repr=False)
    _obj_to_id: dict[int, str] = field(init=False, repr=False)

    @classmethod
    def from_level_pairs(
        cls, pairs: list[tuple[int, Fragment]]
    ) -> "DocumentStructure":
        """Create a ``DocumentStructure`` from ``(level, fragment)`` pairs.

        The input must list fragments in reading order with their hierarchy
        levels starting from ``0``. If multiple fragments are provided at level
        ``0``, they will be attached to an empty top-level node.

        Args:
            pairs: Sequence of ``(level, fragment)`` tuples describing the
                hierarchy.

        Returns:
            DocumentStructure: Constructed hierarchy.

        Raises:
            ValueError: If ``pairs`` is empty or levels are inconsistent.
        """

        if not pairs:
            raise ValueError("pairs cannot be empty")

        idx = 0
        roots: list[StructureNode] = []
        while idx < len(pairs):
            node, idx = cls._parse_pairs(pairs, idx, 0)
            roots.append(node)

        root = roots[0] if len(roots) == 1 else StructureNode(children=roots)
        return cls(root)

    @staticmethod
    def _parse_pairs(
        pairs: list[tuple[int, Fragment]], idx: int, expected_level: int
    ) -> tuple[StructureNode, int]:
        """Recursive helper for :meth:`from_level_pairs`.

        Args:
            pairs: Sequence being parsed.
            idx: Current index in ``pairs``.
            expected_level: Level expected for the current fragment.

        Returns:
            tuple[StructureNode, int]: Constructed node and next index.

        Raises:
            ValueError: If hierarchy levels are inconsistent.
        """

        if idx >= len(pairs):
            raise ValueError("unexpected end of pairs")
        level, fragment = pairs[idx]
        if level != expected_level:
            raise ValueError("invalid level sequence")
        idx += 1
        children: list[StructureNode] = []
        while idx < len(pairs) and pairs[idx][0] > expected_level:
            next_level = pairs[idx][0]
            if next_level != expected_level + 1:
                raise ValueError("invalid level jump")
            child, idx = DocumentStructure._parse_pairs(pairs, idx, expected_level + 1)
            children.append(child)
        return StructureNode(value=fragment, children=children), idx

    def __post_init__(self) -> None:
        """Build helper mappings for constant-time lookups."""

        id_to_node: dict[str, StructureNode] = {}  # fragment id -> node
        id_to_parent: dict[str, Optional[str]] = {}  # fragment id -> parent id
        id_to_children: dict[str, list[str]] = {}  # fragment id -> child ids
        content_to_id: dict[Hashable, str] = {}  # fragment value -> id
        id_to_prev: dict[str, Optional[str]] = {}  # fragment id -> previous id
        id_to_next: dict[str, Optional[str]] = {}  # fragment id -> next id
        id_to_level: dict[str, int] = {}  # fragment id -> level
        obj_to_id: dict[int, str] = {}  # object identity -> fragment id

        def traverse(
            node: StructureNode, parent_id: Optional[str], level: int
        ) -> Optional[str]:
            """Populate lookup tables by walking the tree."""

            node_id: Optional[str] = None
            if node.value is not None:
                node_id = node.value.id or str(id(node.value))
                id_to_node[node_id] = node
                id_to_parent[node_id] = parent_id
                id_to_children[node_id] = []
                id_to_level[node_id] = level
                obj_to_id[id(node.value)] = node_id
                try:
                    content_to_id.setdefault(node.value.value, node_id)
                except TypeError:
                    pass
                id_to_prev[node_id] = None
                id_to_next[node_id] = None

            if node.children:
                prev_child_id: Optional[str] = None
                for child in node.children:
                    child_id = traverse(child, node_id, level + 1)
                    if child_id is None:
                        continue
                    if node_id is not None:
                        id_to_children[node_id].append(child_id)
                    if prev_child_id is not None:
                        id_to_next[prev_child_id] = child_id
                        id_to_prev[child_id] = prev_child_id
                    prev_child_id = child_id
                if prev_child_id is not None:
                    id_to_next[prev_child_id] = None

            return node_id

        traverse(self.root, None, 0)

        object.__setattr__(self, "_id_to_node", id_to_node)
        object.__setattr__(self, "_id_to_parent", id_to_parent)
        object.__setattr__(self, "_id_to_children", id_to_children)
        object.__setattr__(self, "_content_to_id", content_to_id)
        object.__setattr__(self, "_id_to_prev", id_to_prev)
        object.__setattr__(self, "_id_to_next", id_to_next)
        object.__setattr__(self, "_id_to_level", id_to_level)
        object.__setattr__(self, "_obj_to_id", obj_to_id)

    @property
    def structure(self) -> list[tuple[Fragment, int]]:
        """Return a linear representation of the hierarchy.

        Returns:
            list[tuple[Fragment, int]]: Fragment and level pairs.
        """

        return self.root.structure()

    @property
    def fragments(self) -> list[Fragment]:
        """Return all leaf fragments in the structure.

        Returns:
            list[Fragment]: Leaf fragments of the document.
        """

        return self.root.fragments

    def _resolve_id(self, fragment: Fragment | str) -> Optional[str]:
        """Get internal fragment identifier.

        Args:
            fragment: Fragment instance or its string identifier.

        Returns:
            Optional[str]: Fragment identifier if the fragment is known,
            otherwise ``None``.
        """

        if isinstance(fragment, str):
            return fragment if fragment in self._id_to_node else None
        if fragment.id and fragment.id in self._id_to_node:
            return fragment.id
        return self._obj_to_id.get(id(fragment))

    def get_fragment_by_id(self, fragment_id: str) -> Optional[Fragment]:
        """Retrieve a fragment by its identifier.

        Args:
            fragment_id: Identifier of the fragment.

        Returns:
            Optional[Fragment]: Fragment with the given identifier or ``None``.
        """

        node = self._id_to_node.get(fragment_id)
        return node.value if node else None

    def get_fragment_by_content(self, content: Hashable) -> Optional[Fragment]:
        """Find a fragment by its ``value`` field.

        Args:
            content: Fragment value to search for.

        Returns:
            Optional[Fragment]: Found fragment or ``None`` if absent.
        """

        fragment_id = self._content_to_id.get(content)
        return self.get_fragment_by_id(fragment_id) if fragment_id else None

    def previous(self, fragment: Fragment | str) -> Optional[Fragment]:
        """Return the previous fragment on the same hierarchy level.

        Args:
            fragment: Fragment instance or its identifier.

        Returns:
            Optional[Fragment]: Previous fragment or ``None`` if there is no one.
        """

        fragment_id = self._resolve_id(fragment)
        if fragment_id is None:
            return None
        prev_id = self._id_to_prev.get(fragment_id)
        return self.get_fragment_by_id(prev_id) if prev_id else None

    def next(self, fragment: Fragment | str) -> Optional[Fragment]:
        """Return the next fragment on the same hierarchy level.

        Args:
            fragment: Fragment instance or its identifier.

        Returns:
            Optional[Fragment]: Next fragment or ``None`` if it is the last one.
        """

        fragment_id = self._resolve_id(fragment)
        if fragment_id is None:
            return None
        next_id = self._id_to_next.get(fragment_id)
        return self.get_fragment_by_id(next_id) if next_id else None

    def parent(self, fragment: Fragment | str) -> Optional[Fragment]:
        """Return the parent fragment of ``fragment``.

        Args:
            fragment: Fragment instance or its identifier.

        Returns:
            Optional[Fragment]: Parent fragment or ``None`` if at root level.
        """

        fragment_id = self._resolve_id(fragment)
        if fragment_id is None:
            return None
        parent_id = self._id_to_parent.get(fragment_id)
        return self.get_fragment_by_id(parent_id) if parent_id else None

    def children(self, fragment: Fragment | str) -> list[Fragment]:
        """Return child fragments of ``fragment``.

        Args:
            fragment: Fragment instance or its identifier.

        Returns:
            list[Fragment]: Direct child fragments.

        Raises:
            ValueError: If ``fragment`` is not part of the structure.
        """

        fragment_id = self._resolve_id(fragment)
        if fragment_id is None:
            raise ValueError("Fragment not found in structure")
        children_ids = self._id_to_children.get(fragment_id, [])
        return [self._id_to_node[cid].value for cid in children_ids]

    def hierarchy(self) -> pd.DataFrame:
        """Return a ``pandas.DataFrame`` describing the hierarchy.

        The dataframe contains columns: ``id``, ``parent_id`` and ``level``.

        Returns:
            pandas.DataFrame: Hierarchy representation.
        """

        rows = [
            {
                "id": fid,
                "parent_id": self._id_to_parent[fid],
                "level": self._id_to_level[fid],
                "fragment": self._id_to_node[fid].value,
            }
            for fid in self._id_to_node
        ]
        return pd.DataFrame(rows)

    def is_leaf(self, fragment: Fragment | str) -> bool:
        """Check whether ``fragment`` has no children.

        Args:
            fragment: Fragment instance or its identifier.

        Returns:
            bool: ``True`` if ``fragment`` is a leaf.

        Raises:
            ValueError: If ``fragment`` is not part of the structure.
        """

        fragment_id = self._resolve_id(fragment)
        if fragment_id is None:
            raise ValueError("Fragment not found in structure")
        return len(self._id_to_children.get(fragment_id, [])) == 0

    def is_header(self, fragment: Fragment | str) -> bool:
        """Check whether ``fragment`` is a ``HeaderFragment``.

        Args:
            fragment: Fragment instance or its identifier.

        Returns:
            bool: ``True`` if ``fragment`` is a header fragment.
        """

        frag = fragment if isinstance(fragment, Fragment) else self.get_fragment_by_id(fragment)
        return isinstance(frag, HeaderFragment)

    def get_level(self, fragment: Fragment | str) -> int:
        """Return hierarchy level of ``fragment``.

        Args:
            fragment: Fragment instance or its identifier.

        Returns:
            int: Zero-based level within the hierarchy.

        Raises:
            ValueError: If ``fragment`` is not part of the structure.
        """

        fragment_id = self._resolve_id(fragment)
        if fragment_id is None:
            raise ValueError("Fragment not found in structure")
        return self._id_to_level[fragment_id]
