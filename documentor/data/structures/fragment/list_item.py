"""
List item fragment implementation.

Contains:
- ListItemFragment: individual items in bulleted, numbered, or definition lists.
"""

from dataclasses import dataclass
from typing import Any

from .text import TextFragment


@dataclass
class ListItemFragment(TextFragment):
    """
    Implementation for list item fragments representing individual list elements.

    List items are individual elements within ordered, unordered, or definition lists.
    They maintain hierarchical structure and formatting information.

    Attributes:
        value (str): List item text content.
        list_type (str | None): Type of list - 'ordered', 'unordered', 'definition'.
        list_level (int): Hierarchical level within the list structure (0-based).
        marker (str | None): List marker used (e.g., '•', '1.', 'a.', '-', '*').
    """

    list_type: str | None = None
    list_level: int = 0
    marker: str | None = None

    @classmethod
    def description(cls) -> str:
        return "Individual items in bulleted, numbered, or definition lists"

    def __dict__(self) -> dict[str, Any]:
        """Get parameters of the list item fragment."""
        data = super().__dict__()
        data.update({
            "list_type": self.list_type,
            "list_level": self.list_level,
            "marker": self.marker,
        })
        return data
