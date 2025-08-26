"""
Base abstractions for document fragments.

Defines the Fragment abstract base class used by all fragment types.
"""
import dataclasses
from abc import ABC, abstractmethod
from typing import Any


class Fragment(ABC):
    """
    Base class for fragments of any type.

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
    """
    value: Any
    page: str | None = None
    description: str = ""

    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of a fragment's value.

        Returns:
            str: Value of the fragment.
        """
        raise NotImplementedError

    @abstractmethod
    def __dict__(self) -> dict[str, Any]:
        """
        Get parameters of the fragment.

        Returns:
            dict[str, Any]: Parameters of the fragment.
        """
        raise NotImplementedError
