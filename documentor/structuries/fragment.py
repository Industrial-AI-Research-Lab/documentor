from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import UnionType
from typing import Any, Optional

from overrides import overrides

from documentor.structuries.custom_types import LabelType


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
    value: str

    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of a fragment's value.

        Returns:
            str: Value of the fragment.
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """
        Get parameters of the fragment.

        Returns:
            dict[str, Any]: Parameters of the fragment.
        """
        pass

    @classmethod
    @abstractmethod
    def param_types_dict(cls) -> dict[str, type | UnionType]:
        """
        Get types of parameters of the fragment.

        Returns:
            dict[str, type | UnionType]: Types out of parameters of the fragment.
        """
        pass


@dataclass
class Fragment(FragmentInterface):
    """
    Simple implementation of FragmentInterface for text fragments that have only value.

    Args:
        value (str): Value of the fragment.
        label (LabelType | None, optional): Label of the fragment from classification. Defaults to None.
    """
    value: Any
    label: LabelType | None = None
    page: Optional[str] = None


    @overrides
    def __str__(self) -> str:
        return str(self.value)

    @overrides
    def to_dict(self) -> dict[str, Any]:
        return {field: getattr(self, field) for field in self.__annotations__.keys()}

    @classmethod
    @overrides
    def param_types_dict(cls) -> dict[str, type | UnionType]:
        return {param: param_type for param, param_type in cls.__annotations__.items()}
