"""Base abstractions for document fragments."""

import dataclasses
from abc import ABC, abstractmethod
from typing import Any, Hashable

from .style import BlockStyle


@dataclasses.dataclass
class Fragment(ABC):
    """Base class for fragments of any type.

    Each fragment represents a structural unit of a document.

    Examples of fragments:
    - a table cell
    - a log entry
    - a sentence or paragraph of a document with a string value and parameters.
    - an image in a document

    Attributes:
        value: value of the fragment
        page: page number of the fragment
        description: description of the fragment type for LLM
        id: optional unique identifier of the fragment
        bbox: optional coordinates of the fragment (x1, y1, x2, y2)
        style: block level style of the fragment
    """

    value: Hashable
    page: str | None = None
    description: str = ""
    is_processed: bool = True
    id: str | None = None
    bbox: tuple[int, int, int, int] | None = None
    style: BlockStyle | None = None

    @abstractmethod
    def __str__(self) -> str:
        """String representation of a fragment's value."""
        raise NotImplementedError

    def __dict__(self) -> dict[str, Any]:
        """Get parameters of the fragment."""
        return {
            field.name: getattr(self, field.name)
            for field in dataclasses.fields(self)
        }
