from abc import ABC, abstractmethod
from typing import Any


class FragmentInterface(ABC):
    """
    Interface for fragments of any type.

    Each fragment represents a structural unit of a document.
    Examples of fragments:
    - a table cell
    - a log entry
    - a sentence or paragraph of a document with a string value and parameters.
    - image in a document
    """
    value: Any
    page: str | None = None

    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of a fragment's value.

        Returns:
            str: Value of the fragment.
        """
        pass

    @abstractmethod
    def __dict__(self) -> dict[str, Any]:
        """
        Get parameters of the fragment.

        Returns:
            dict[str, Any]: Parameters of the fragment.
        """
        pass

    @staticmethod
    @abstractmethod
    def description() -> str:
        """
        Description of the fragment type.

        Returns:
            str: Description of the fragment type.
        """
        pass